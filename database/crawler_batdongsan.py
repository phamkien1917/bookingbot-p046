"""Crawl complete public sale listings from Batdongsan.com.vn into PostgreSQL SQL.

The collector deliberately stays within public listing pages.  It does not click
"Hien so", solve CAPTCHA challenges, rotate proxies, log in, or turn external
posters into internal sales users.  Public masked contact data is retained only
as source provenance.

The parser keeps every label/value row from "Dac diem bat dong san" in JSONB and
also normalizes fields used by the application.  Completeness rules differ by
property kind: land is not required to have bedrooms, while apartments are not
required to have frontage or road width.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import html as html_lib
import json
import os
import random
import re
import sys
import time
import unicodedata
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Iterable, Iterator
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import HTTPCookieProcessor, Request, build_opener
from urllib.robotparser import RobotFileParser


BASE_URL = "https://batdongsan.com.vn"
DEFAULT_START_URL = (
    "https://batdongsan.com.vn/ban-dat-phuong-hung-thang-1/"
    "ban-o-goc-canh-nha-o-xa-hoi-bim-bai-chay-ha-long-gia-au-tu-pr46093955"
)
DEFAULT_TARGET = 20
DEFAULT_MAX_PAGES = 5
DEFAULT_DELAY_SECONDS = 3.0
DEFAULT_JITTER_SECONDS = 0.75
MIN_DELAY_SECONDS = 2.0
MIN_IMAGE_COUNT = 3
MAX_HTML_BYTES = 8_000_000
PRICE_PER_SQM_TOLERANCE = Decimal("0.15")
SOURCE_MEDIA_CAPTION = "Nguồn: Batdongsan.com.vn"

PUBLIC_EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+(?![\w.-])",
    re.IGNORECASE,
)
PUBLIC_VN_PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:(?:\+?84)|0)(?:[ .-]?\d){9}(?!\d)",
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

PROPERTY_NAMESPACE = uuid.UUID("5d49deec-86a5-4d33-93ba-46d2596e2353")
MEDIA_NAMESPACE = uuid.UUID("2a9f06d4-147c-42b4-992d-724b25164b31")
EXTERNAL_SELLER_NAMESPACE = uuid.UUID("cd491257-c249-4f2e-92cc-a5a55c4fe773")
DEMO_SALE_USER_IDS = (
    "10000000-0000-0000-0000-000000000002",
    "10000000-0000-0000-0000-000000000008",
    "10000000-0000-0000-0000-000000000009",
)

LISTING_ID_PATTERN = re.compile(r"-pr(?P<id>\d+)(?:[/?#]|$)", re.IGNORECASE)
LISTING_HREF_PATTERN = re.compile(
    r"href=[\"'](?P<href>[^\"']*-pr\d+(?:[/?#][^\"']*)?)[\"']",
    re.IGNORECASE,
)

BLOCK_MARKERS = (
    "<title>just a moment",
    "enable javascript and cookies to continue",
    "window._cf_chl_opt",
)

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class CrawlError(RuntimeError):
    """Raised when a crawl cannot safely produce a trustworthy output."""


class AccessBlocked(CrawlError):
    """Raised when the source asks for CAPTCHA/browser verification."""


@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    parent: Node | None = None
    parts: list[str | Node] = field(default_factory=list)

    @property
    def classes(self) -> set[str]:
        return {value for value in self.attrs.get("class", "").split() if value}


class PageTreeParser(HTMLParser):
    """Small dependency-free HTML tree suitable for label-based extraction."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.stack: list[Node] = [self.root]

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        normalized_tag = tag.lower()
        if normalized_tag == "br":
            self.stack[-1].parts.append("\n")
            return
        node = Node(
            normalized_tag,
            {key.lower(): value or "" for key, value in attrs},
            self.stack[-1],
        )
        self.stack[-1].parts.append(node)
        if normalized_tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == normalized_tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].parts.append(data)


def iter_nodes(node: Node) -> Iterator[Node]:
    for part in node.parts:
        if isinstance(part, Node):
            yield part
            yield from iter_nodes(part)


def raw_node_text(node: Node) -> str:
    values: list[str] = []
    for part in node.parts:
        values.append(raw_node_text(part) if isinstance(part, Node) else part)
    return "".join(values)


def node_text(node: Node, *, preserve_breaks: bool = False) -> str:
    text = html_lib.unescape(raw_node_text(node)).replace("\xa0", " ")
    if preserve_breaks:
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    return " ".join(text.split())


def has_class(node: Node, class_name: str) -> bool:
    return class_name in node.classes


def nodes_with_class(root: Node, *class_names: str) -> list[Node]:
    wanted = set(class_names)
    return [node for node in iter_nodes(root) if node.classes & wanted]


def first_node_with_class(root: Node, *class_names: str) -> Node | None:
    wanted = set(class_names)
    return next((node for node in iter_nodes(root) if node.classes & wanted), None)


def first_descendant_with_class(node: Node, *class_names: str) -> Node | None:
    return first_node_with_class(node, *class_names)


def direct_child_with_class(node: Node, *class_names: str) -> Node | None:
    wanted = set(class_names)
    return next(
        (
            part
            for part in node.parts
            if isinstance(part, Node) and part.classes & wanted
        ),
        None,
    )


def normalize_label(value: Any) -> str:
    text = fold_text(value).replace("²", "2")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def fold_text(value: Any) -> str:
    text = str(value or "").replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return text.lower()


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return bool(value)
    return True


def redact_public_contact(value: Any) -> tuple[str, int]:
    """Remove directly exposed email/phone values from free-form source text."""

    text = str(value or "")
    text, email_count = PUBLIC_EMAIL_PATTERN.subn("[email đã ẩn]", text)
    text, phone_count = PUBLIC_VN_PHONE_PATTERN.subn("[số điện thoại đã ẩn]", text)
    return text, email_count + phone_count


def parse_localized_decimal(value: Any) -> Decimal | None:
    if not has_value(value):
        return None
    match = re.search(r"[-+]?\d[\d\s.,]*", str(value))
    if not match:
        return None
    token = match.group(0).replace(" ", "")
    if "," in token:
        token = token.replace(".", "").replace(",", ".")
    elif token.count(".") > 1:
        token = token.replace(".", "")
    try:
        number = Decimal(token)
    except InvalidOperation:
        return None
    return number if number.is_finite() else None


def parse_measurement(value: Any) -> float | None:
    number = parse_localized_decimal(value)
    return float(number) if number is not None else None


def parse_count(value: Any) -> int | None:
    number = parse_localized_decimal(value)
    if number is None or number != number.to_integral_value():
        return None
    return int(number)


def parse_vnd(value: Any) -> int | None:
    if not has_value(value):
        return None
    normalized = normalize_label(value)
    if "thoa thuan" in normalized or "lien he" in normalized:
        return None
    number = parse_localized_decimal(value)
    if number is None:
        return None
    if "ty" in normalized:
        number *= Decimal(1_000_000_000)
    elif "trieu" in normalized:
        number *= Decimal(1_000_000)
    elif "nghin" in normalized or "ngan" in normalized:
        number *= Decimal(1_000)
    try:
        return int(number.to_integral_value())
    except (ValueError, OverflowError):
        return None


def normalize_orientation(value: Any) -> str | None:
    if not has_value(value):
        return None
    text = " ".join(str(value).split())
    text = re.sub(r"\s*[-–—]\s*", " ", text)
    return " ".join(text.split()) or None


def normalize_iso_timestamp(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip().replace("Z", "+00:00")
    candidate = re.sub(r"(\.\d{6})\d+(?=[+-]\d\d:\d\d$)", r"\1", candidate)
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.isoformat()


def is_valid_iso_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def canonical_listing_url(value: str) -> str:
    parsed = urlparse(value.strip())
    hostname = (parsed.hostname or "").lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    if hostname != "batdongsan.com.vn":
        raise ValueError(f"Unsupported source host: {parsed.hostname!r}")
    path = re.sub(r"/{2,}", "/", parsed.path).rstrip("/")
    if not LISTING_ID_PATTERN.search(path):
        raise ValueError(f"Not a Batdongsan listing URL: {value}")
    return urlunparse(("https", hostname, path, "", "", ""))


def canonical_start_url(value: str) -> str:
    parsed = urlparse(value.strip())
    hostname = (parsed.hostname or "").lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    if hostname != "batdongsan.com.vn":
        raise ValueError(f"Unsupported source host: {parsed.hostname!r}")
    path = re.sub(r"/{2,}", "/", parsed.path).rstrip("/") or "/"
    return urlunparse(("https", hostname, path, "", parsed.query, ""))


def listing_id_from_url(value: str) -> str | None:
    match = LISTING_ID_PATTERN.search(urlparse(value).path)
    return match.group("id") if match else None


def pagination_url(value: str, page_number: int) -> str:
    parsed = urlparse(canonical_start_url(value))
    path = re.sub(r"/p\d+$", "", parsed.path.rstrip("/"), flags=re.IGNORECASE)
    if page_number > 1:
        path += f"/p{page_number}"
    return urlunparse(("https", parsed.netloc, path, "", parsed.query, ""))


def discover_listing_urls(html_text: str, page_url: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for match in LISTING_HREF_PATTERN.finditer(html_text):
        candidate = html_lib.unescape(match.group("href"))
        try:
            normalized = canonical_listing_url(urljoin(page_url, candidate))
        except ValueError:
            continue
        if normalized not in seen:
            seen.add(normalized)
            found.append(normalized)
    return found


def is_challenge_page(html_text: str) -> bool:
    lowered = html_text[:500_000].lower()
    if any(marker in lowered for marker in BLOCK_MARKERS):
        return True
    return (
        "challenge-platform" in lowered
        and "js__product-detail-web" not in lowered
        and "js__product-link-for-product-id" not in lowered
    )


class PublicFetcher:
    def __init__(
        self,
        *,
        timeout_seconds: float,
        retries: int,
        delay_seconds: float,
        jitter_seconds: float,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.delay_seconds = delay_seconds
        self.jitter_seconds = jitter_seconds
        self.last_request_at = 0.0
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))

    def _wait_for_rate_limit(self) -> None:
        elapsed = time.monotonic() - self.last_request_at
        target_delay = self.delay_seconds + random.uniform(0, self.jitter_seconds)
        if elapsed < target_delay:
            time.sleep(target_delay - elapsed)

    def fetch_text(self, url: str) -> str:
        normalized_url = canonical_start_url(url)
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            self._wait_for_rate_limit()
            request = Request(
                normalized_url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.7",
                    "Cache-Control": "no-cache",
                },
            )
            try:
                self.last_request_at = time.monotonic()
                with self.opener.open(request, timeout=self.timeout_seconds) as response:
                    content_length = response.headers.get("Content-Length")
                    if content_length and int(content_length) > MAX_HTML_BYTES:
                        raise CrawlError(f"Response too large: {normalized_url}")
                    payload = response.read(MAX_HTML_BYTES + 1)
                    if len(payload) > MAX_HTML_BYTES:
                        raise CrawlError(f"Response exceeded size limit: {normalized_url}")
                    charset = response.headers.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="replace")
                    if is_challenge_page(text):
                        raise AccessBlocked(
                            "Batdongsan.com.vn returned a browser/CAPTCHA challenge; "
                            "the crawler stopped without bypassing it"
                        )
                    return text
            except AccessBlocked:
                raise
            except HTTPError as exc:
                last_error = exc
                if exc.code in {401, 403}:
                    raise AccessBlocked(
                        f"Batdongsan.com.vn denied automated access with HTTP {exc.code}"
                    ) from exc
                if exc.code not in {408, 425, 429, 500, 502, 503, 504}:
                    break
                retry_after = exc.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(min(float(retry_after), 60.0))
            except (URLError, TimeoutError, OSError, CrawlError) as exc:
                last_error = exc
            if attempt < self.retries:
                time.sleep(min(2**attempt, 10))
        raise CrawlError(
            f"Failed after {self.retries + 1} attempts: {normalized_url}: {last_error}"
        )


def ensure_robots_allowed(
    fetcher: PublicFetcher, urls: Iterable[str]
) -> RobotFileParser:
    robots_url = f"{BASE_URL}/robots.txt"
    robots_text = fetcher.fetch_text(robots_url)
    parser = RobotFileParser(robots_url)
    parser.parse(robots_text.splitlines())
    for url in urls:
        normalized = canonical_start_url(url)
        if not parser.can_fetch(USER_AGENT, normalized):
            raise CrawlError(f"robots.txt does not allow crawling: {normalized}")
    return parser


def ensure_url_allowed(parser: RobotFileParser, url: str) -> None:
    normalized = canonical_start_url(url)
    if not parser.can_fetch(USER_AGENT, normalized):
        raise CrawlError(f"robots.txt does not allow crawling: {normalized}")


def parse_html_tree(html_text: str) -> Node:
    parser = PageTreeParser()
    parser.feed(html_text)
    parser.close()
    return parser.root


def descendant_by_tag(node: Node, tag: str) -> Node | None:
    return next((item for item in iter_nodes(node) if item.tag == tag), None)


def extract_labeled_blocks(
    root: Node,
    *,
    item_classes: tuple[str, ...],
    title_classes: tuple[str, ...],
    value_classes: tuple[str, ...],
    extension_classes: tuple[str, ...] = (),
) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    for item in nodes_with_class(root, *item_classes):
        title_node = first_descendant_with_class(item, *title_classes)
        value_node = first_descendant_with_class(item, *value_classes)
        if title_node is None or value_node is None:
            continue
        title = node_text(title_node)
        value = node_text(value_node)
        if not title or not value:
            continue
        extension = ""
        if extension_classes:
            extension_node = first_descendant_with_class(item, *extension_classes)
            if extension_node is not None:
                extension = node_text(extension_node)
        blocks.append({"label": title, "value": value, "extension": extension})
    return blocks


def blocks_by_label(blocks: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for block in blocks:
        result.setdefault(normalize_label(block["label"]), block)
    return result


def first_block(
    mapping: dict[str, dict[str, str]], *labels: str
) -> dict[str, str] | None:
    for label in labels:
        block = mapping.get(normalize_label(label))
        if block:
            return block
    return None


def extract_meta(root: Node) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in iter_nodes(root):
        if node.tag != "meta":
            continue
        key = node.attrs.get("property") or node.attrs.get("name")
        value = node.attrs.get("content")
        if key and value:
            result[key.lower()] = html_lib.unescape(value).strip()
    return result


def extract_json_ld(root: Node) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for node in iter_nodes(root):
        if node.tag != "script":
            continue
        if node.attrs.get("type", "").lower() != "application/ld+json":
            continue
        try:
            payload = json.loads(raw_node_text(node).strip())
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(payload, dict):
            result.append(payload)
        elif isinstance(payload, list):
            result.extend(item for item in payload if isinstance(item, dict))
    return result


def extract_tracking_product(html_text: str) -> dict[str, Any]:
    match = re.search(
        r"window\.pageTrackingData\s*=.*?JSON\.parse\('(?P<payload>.*?)'\)",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return {}
    try:
        decoded = ast.literal_eval("'" + match.group("payload") + "'")
        payload = json.loads(decoded)
    except (SyntaxError, ValueError, json.JSONDecodeError):
        return {}
    products = payload.get("products") if isinstance(payload, dict) else None
    if isinstance(products, list) and products and isinstance(products[0], dict):
        return products[0]
    return {}


def attribute_key(label: str) -> str | None:
    normalized = normalize_label(label)
    direct = {
        "khoang gia": "source_price_per_sqm",
        "muc gia": "price",
        "gia ban": "price",
        "dien tich": "area_sqm",
        "dien tich su dung": "usable_area_sqm",
        "so phong ngu": "bedrooms",
        "so phong tam": "bathrooms",
        "so phong ve sinh": "bathrooms",
        "so phong tam ve sinh": "bathrooms",
        "so toilet": "bathrooms",
        "so tang": "total_floors",
        "tang": "floor_number",
        "huong nha": "orientation",
        "huong ban cong": "balcony_orientation",
        "mat tien": "frontage_m",
        "duong vao": "road_width_m",
        "phap ly": "legal_status",
        "noi that": "furniture_status",
        "loai hinh": "source_property_type",
        "du an": "project_name",
        "so thua": "parcel_number",
        "to ban do": "map_sheet_number",
        "muc dich su dung": "land_use_purpose",
        "thoi han su dung": "land_use_term",
        "ngay dang": "published_at_text",
        "ngay het han": "expires_at_text",
        "loai tin": "listing_tier",
        "ma tin": "source_listing_id_text",
    }
    return direct.get(normalized)


def normalized_attribute_value(key: str | None, value: str) -> Any:
    if key in {
        "area_sqm",
        "usable_area_sqm",
        "frontage_m",
        "road_width_m",
    }:
        return parse_measurement(value)
    if key in {"bedrooms", "bathrooms", "total_floors", "floor_number"}:
        return parse_count(value)
    if key in {"price", "source_price_per_sqm"}:
        return parse_vnd(value)
    if key in {"orientation", "balcony_orientation"}:
        return normalize_orientation(value)
    return value


def extract_property_kind(url: str, specs: dict[str, dict[str, str]]) -> str | None:
    type_block = first_block(specs, "Loại hình")
    type_text = normalize_label(type_block["value"] if type_block else "")
    path = normalize_label(urlparse(url).path)

    def classify(value: str) -> str | None:
        if "can ho" in value or "chung cu" in value or "tap the" in value:
            return "APARTMENT"
        if re.search(r"\bdat\b|dat nen", value):
            return "LAND"
        if "shophouse" in value or "thuong mai" in value or "nha mat pho" in value:
            return "COMMERCIAL"
        # Batdongsan has a combined category path "biet-thu-lien-ke".  An
        # explicit source label must win over that ambiguous URL fallback.
        if "biet thu" in value:
            return "VILLA"
        if "lien ke" in value or "nha pho lien ke" in value:
            return "TOWNHOUSE"
        if "nha rieng" in value or "nha o" in value:
            return "HOUSE"
        return None

    if type_text:
        explicit_kind = classify(type_text)
        if explicit_kind:
            return explicit_kind
    return classify(path)


def split_address(address: str) -> tuple[str | None, str | None, str | None]:
    parts = [part.strip() for part in address.split(",") if part.strip()]
    if len(parts) < 3:
        return None, None, None
    return parts[-3], parts[-2], parts[-1]


def extract_coordinates(html_text: str) -> tuple[float | None, float | None]:
    patterns = (
        r"latitude\s*:\s*(-?\d+(?:\.\d+)?)\s*,\s*longitude\s*:\s*(-?\d+(?:\.\d+)?)",
        r"\"latitude\"\s*:\s*(-?\d+(?:\.\d+)?)\s*,\s*\"longitude\"\s*:\s*(-?\d+(?:\.\d+)?)",
    )
    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.IGNORECASE)
        if not match:
            continue
        latitude, longitude = float(match.group(1)), float(match.group(2))
        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
            return latitude, longitude
    return None, None


def canonical_media_url(value: str) -> str | None:
    candidate = html_lib.unescape(value).replace("\\/", "/").strip()
    if not candidate.startswith("https://"):
        return None
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    if not (
        host.endswith("batdongsan.com.vn")
        or host.endswith("pgimgs.com")
    ):
        return None
    return urlunparse(("https", parsed.netloc, parsed.path, "", parsed.query, ""))


def extract_media(
    html_text: str,
    meta: dict[str, str],
    source_listing_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    decoded = html_lib.unescape(html_text).replace("\\/", "/")
    image_candidates: list[list[str]] = []
    gallery_fragments: list[str] = []
    listing_id = re.escape(source_listing_id)
    for pattern in (
        rf'"images"\s*:\s*"(?P<images>[^"]+)"(?P<tail>.{{0,50000}}?)'
        rf'"prid"\s*:\s*"?{listing_id}"?',
        rf"\bimages\s*:\s*\"(?P<images>[^\"]+)\"(?P<tail>.{{0,50000}}?)"
        rf"\bprid\s*:\s*\"?{listing_id}\"?",
        rf'"url"\s*:\s*"(?P<images>[^"]*#~[^"]*)"(?P<tail>.{{0,50000}}?)'
        rf'"prid"\s*:\s*"?{listing_id}"?',
    ):
        for match in re.finditer(
            pattern, decoded, flags=re.IGNORECASE | re.DOTALL
        ):
            urls: list[str] = []
            seen: set[str] = set()
            for raw_url in match.group("images").split("#~"):
                normalized = canonical_media_url(raw_url)
                if normalized and normalized not in seen:
                    seen.add(normalized)
                    urls.append(normalized)
            if urls:
                image_candidates.append(urls)
                gallery_fragments.append(match.group(0))

    images = max(image_candidates, key=len) if image_candidates else []
    if not images and meta.get("og:image"):
        cover = canonical_media_url(meta["og:image"])
        if cover:
            images = [cover]

    video_urls: list[str] = []
    seen_videos: set[str] = set()
    for gallery_fragment in gallery_fragments:
        for match in re.finditer(
            r"https://[^\"'<>\s\\]+\.mp4(?:\?[^\"'<>\s\\]+)?",
            gallery_fragment,
            flags=re.IGNORECASE,
        ):
            normalized = canonical_media_url(match.group(0))
            if normalized and normalized not in seen_videos:
                seen_videos.add(normalized)
                video_urls.append(normalized)

    media: list[dict[str, Any]] = []
    for index, url in enumerate(images):
        media.append(
            {
                "type": "IMAGE",
                "url": url,
                "caption": SOURCE_MEDIA_CAPTION,
                "sort_order": index,
                "is_cover": index == 0,
            }
        )

    # These public MP4 links are frequently signed or reject direct playback.
    # Keep them as unverified source metadata instead of broken UI media rows.
    source_videos = [
        {"url": url, "availability": "UNVERIFIED"} for url in video_urls
    ]
    return media, source_videos


def extract_seller(
    root: Node, html_text: str, tracking: dict[str, Any]
) -> dict[str, Any]:
    contact = first_node_with_class(root, "re__contact-name", "js_contact-name")
    seller_name = None
    if contact is not None:
        seller_name = contact.attrs.get("title") or node_text(contact)

    seller_root = contact or root
    candidate = seller_root.parent
    while candidate is not None and candidate.tag != "document":
        # Stop before the scope grows into the full page/related-listing area.
        if len(node_text(candidate)) > 12_000:
            break
        seller_root = candidate
        candidate = candidate.parent

    profile_url = None
    for node in iter_nodes(seller_root):
        href = node.attrs.get("href", "")
        if node.tag == "a" and "guru.batdongsan.com.vn/pa/" in href:
            profile_url = html_lib.unescape(urljoin(BASE_URL, href))
            break

    avatar_url = None
    avatar = first_node_with_class(seller_root, "re__contact-avatar")
    if avatar is not None:
        avatar_url = canonical_media_url(avatar.attrs.get("src", ""))

    details: dict[str, str] = {}
    for node in nodes_with_class(
        seller_root, "agent-deail-infor", "agent-detail-infor"
    ):
        label_node = descendant_by_tag(node, "span")
        value_node = descendant_by_tag(node, "i")
        if label_node is None or value_node is None:
            continue
        label, value = node_text(label_node), node_text(value_node)
        if label and value:
            safe_label, _ = redact_public_contact(label)
            safe_value, _ = redact_public_contact(value)
            details[safe_label] = safe_value

    masked_phone = None
    phone_pattern = re.compile(r"(?:\+?84|0)[\d .-]{5,}\*{2,}")
    for node in iter_nodes(seller_root):
        if "phone" not in " ".join(node.classes).lower():
            continue
        match = phone_pattern.search(node_text(node))
        if match:
            masked_phone = " ".join(match.group(0).split())
            break

    full_text = node_text(seller_root)
    if masked_phone is None:
        match = phone_pattern.search(full_text)
        if match:
            masked_phone = " ".join(match.group(0).split())

    seller_id = tracking.get("createByUser")
    if seller_id is None:
        product_root = first_node_with_class(root, "js__product-detail-web")
        if product_root is not None:
            seller_id = product_root.attrs.get("uid") or None

    normalized_details = {normalize_label(key): value for key, value in details.items()}
    joined_text = next(
        (value for key, value in normalized_details.items() if "tham gia" in key),
        None,
    )
    active_count = None
    for key, value in normalized_details.items():
        if "tin" in key:
            active_count = parse_count(value)
            if active_count is not None:
                break

    return {
        "source_account_id": str(seller_id) if seller_id is not None else None,
        "display_name": seller_name,
        "account_type": (
            "BROKER"
            if "moi gioi chuyen nghiep" in normalize_label(full_text)
            else "UNKNOWN"
        ),
        "profile_url": profile_url,
        "avatar_url": avatar_url,
        "source_verified_flag": bool(tracking.get("verified")),
        "is_professional": (
            "moi gioi chuyen nghiep" in normalize_label(full_text)
            or "pro-agent" in raw_node_text(seller_root).lower()
        ),
        "has_broker_badge": "avatar-badge" in raw_node_text(seller_root),
        "joined_text": joined_text,
        "active_listing_count": active_count,
        "public_phone_masked": masked_phone,
        "has_zalo": bool(re.search(r"\bZalo\b", full_text, re.IGNORECASE)),
        "has_chat": bool(re.search(r"\bChat\b", full_text, re.IGNORECASE)),
        "public_details": details,
    }


def extract_project(root: Node, specs: dict[str, dict[str, str]]) -> dict[str, Any]:
    project_block = first_block(specs, "Dự án")
    project_name = project_block["value"] if project_block else None
    project_url = None
    if project_name:
        target = normalize_label(project_name)
        for node in iter_nodes(root):
            if node.tag != "a" or not node.attrs.get("href"):
                continue
            if target and target in normalize_label(node_text(node)):
                project_url = urljoin(BASE_URL, node.attrs["href"])
                break
    return {
        "name": project_name,
        "url": project_url,
    }


def extract_market_insights(root: Node, html_text: str) -> dict[str, Any]:
    plain_text = " ".join(fold_text(node_text(root)).split())
    annual_change = None
    direction = None
    match = re.search(
        r"(\d+(?:[,.]\d+)?)\s*%\s*gia.{0,100}\b(tang|giam)\b.{0,80}1 nam",
        plain_text,
    )
    if match:
        parsed = parse_measurement(match.group(1))
        if parsed is not None:
            annual_change = parsed if match.group(2) == "tang" else -parsed
            direction = "UP" if annual_change >= 0 else "DOWN"

    years = None
    years_node = first_node_with_class(root, "js__pricing-history-count-of-years")
    if years_node is not None:
        years = parse_count(years_node.attrs.get("value"))

    history_container = first_node_with_class(root, "js__pricing-history")
    history_endpoint = None
    if history_container is not None and history_container.attrs.get("data-url"):
        history_endpoint = urljoin(BASE_URL, history_container.attrs["data-url"])

    return {
        "annual_change_percent": annual_change,
        "annual_change_direction": direction,
        "pricing_history_endpoint_available": bool(
            history_endpoint and "js__encrypted-params" in html_text
        ),
        "pricing_history_fetched": False,
        "pricing_history_years": years,
        "pricing_history_endpoint": history_endpoint,
        "history_points": [],
    }


def extract_listing_metadata(root: Node, source_listing_id: str) -> dict[str, Any]:
    """Read the public footer fields without guessing values from vipType."""

    wanted = {
        "ngay dang": "published_text",
        "ngay het han": "expires_text",
        "loai tin": "listing_tier",
        "ma tin": "listing_id_text",
    }
    result: dict[str, Any] = {}
    for node in iter_nodes(root):
        title_node = direct_child_with_class(node, "title")
        value_node = direct_child_with_class(node, "value")
        if title_node is None or value_node is None:
            continue
        key = wanted.get(normalize_label(node_text(title_node)))
        value = node_text(value_node)
        if key and value:
            result.setdefault(key, value)

    # Some layouts render this footer without stable wrapper classes.  Only
    # accept the fallback when its displayed listing ID matches this page.
    if len(result) < len(wanted):
        plain_text = node_text(root)
        match = re.search(
            r"Ngày\s*đăng\s*(?P<published>\d{2}/\d{2}/\d{4})\s*"
            r"Ngày\s*hết\s*hạn\s*(?P<expires>\d{2}/\d{2}/\d{4})\s*"
            r"Loại\s*tin\s*(?P<tier>.*?)\s*"
            r"Mã\s*tin\s*(?P<listing_id>\d+)",
            plain_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if match and match.group("listing_id") == source_listing_id:
            result.setdefault("published_text", match.group("published"))
            result.setdefault("expires_text", match.group("expires"))
            result.setdefault("listing_tier", " ".join(match.group("tier").split()))
            result.setdefault("listing_id_text", match.group("listing_id"))
    return result


def is_probable_bundle(title: str, description: str) -> bool:
    text = normalize_label(f"{title} {description}")
    signals = (
        "quy can",
        "bang hang",
        "nhieu can",
        "cac can",
        "studio 1pn 2pn",
        "1pn 2pn 3pn",
    )
    return any(signal in text for signal in signals)


def listing_issues(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field_name in (
        "property_id",
        "source_listing_id",
        "source_url",
        "property_kind",
        "title",
        "description",
        "price",
        "price_per_sqm",
        "source_price_per_sqm",
        "area_sqm",
        "address",
        "ward",
        "district",
        "province",
        "latitude",
        "longitude",
        "legal_status",
        "published_at",
        "crawled_at",
        "media",
        "seller",
    ):
        if not has_value(record.get(field_name)):
            issues.append(f"missing_{field_name}")

    if record.get("listing_type") != "SALE":
        issues.append("listing_type_not_sale")
    if record.get("status") != "AVAILABLE":
        issues.append("listing_not_available")
    if record.get("currency") != "VND":
        issues.append("unsupported_currency")
    if record.get("status") not in {
        "DRAFT",
        "AVAILABLE",
        "UNDER_OFFER",
        "SOLD",
        "HIDDEN",
        "MAINTENANCE",
    }:
        issues.append("invalid_status")
    if record.get("property_kind") not in {
        "LAND",
        "APARTMENT",
        "HOUSE",
        "VILLA",
        "TOWNHOUSE",
        "COMMERCIAL",
    }:
        issues.append("unknown_property_kind")

    title = str(record.get("title") or "")
    description = str(record.get("description") or "")
    if not 5 <= len(title) <= 200:
        issues.append("invalid_title_length")
    if len(description) < 30:
        issues.append("description_too_short")
    if is_probable_bundle(title, description):
        issues.append("probable_multi_property_bundle")

    price = record.get("price")
    area = record.get("area_sqm")
    price_per_sqm = record.get("price_per_sqm")
    if not isinstance(price, int) or not 0 < price <= 9_999_999_999_999_999:
        issues.append("invalid_price")
    if not isinstance(area, (int, float)) or not 0 < float(area) <= 9_999_999_999.99:
        issues.append("invalid_area")
    if not isinstance(price_per_sqm, int) or price_per_sqm <= 0:
        issues.append("invalid_price_per_sqm")
    source_price = record.get("source_price_per_sqm")
    if not isinstance(source_price, int) or source_price <= 0:
        issues.append("invalid_source_price_per_sqm")
    if (
        isinstance(price, int)
        and price > 0
        and isinstance(area, (int, float))
        and area > 0
        and isinstance(source_price, int)
        and source_price > 0
    ):
        calculated = Decimal(price) / Decimal(str(area))
        difference = abs(Decimal(source_price) - calculated) / calculated
        if difference > PRICE_PER_SQM_TOLERANCE:
            issues.append("price_per_sqm_mismatch")

    latitude, longitude = record.get("latitude"), record.get("longitude")
    if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
        issues.append("invalid_latitude")
    if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
        issues.append("invalid_longitude")

    length_limits = {
        "property_id": 50,
        "title": 200,
        "ward": 100,
        "district": 100,
        "province": 100,
        "orientation": 32,
        "legal_status": 150,
        "parcel_number": 100,
        "map_sheet_number": 100,
        "land_use_purpose": 150,
        "land_use_term": 150,
    }
    for field_name, maximum in length_limits.items():
        value = record.get(field_name)
        if value is not None and len(str(value)) > maximum:
            issues.append(f"{field_name}_too_long")

    usable_area = record.get("usable_area_sqm")
    if usable_area is not None and (
        not isinstance(usable_area, (int, float))
        or not 0 < float(usable_area) <= 9_999_999_999.99
    ):
        issues.append("invalid_usable_area")
    for field_name in ("frontage_m", "road_width_m"):
        value = record.get(field_name)
        if value is not None and (
            not isinstance(value, (int, float))
            or not 0 < float(value) <= 99_999_999.99
        ):
            issues.append(f"invalid_{field_name}")
    for field_name in ("bedrooms", "bathrooms"):
        value = record.get(field_name)
        if value is not None and (
            not isinstance(value, int) or not 0 <= value <= 32_767
        ):
            issues.append(f"invalid_{field_name}")
    floor_number = record.get("floor_number")
    if floor_number is not None and (
        not isinstance(floor_number, int) or not -32_768 <= floor_number <= 32_767
    ):
        issues.append("invalid_floor_number")
    total_floors = record.get("total_floors")
    if total_floors is not None and (
        not isinstance(total_floors, int) or not 0 <= total_floors <= 32_767
    ):
        issues.append("invalid_total_floors")
    for field_name in ("published_at", "crawled_at", "source_updated_at"):
        value = record.get(field_name)
        if value is not None and not is_valid_iso_timestamp(value):
            issues.append(f"invalid_{field_name}")

    seller = record.get("seller")
    if not isinstance(seller, dict):
        issues.append("invalid_seller")
    else:
        if not has_value(seller.get("display_name")):
            issues.append("missing_seller_name")
        if not has_value(seller.get("public_phone_masked")):
            issues.append("missing_seller_public_phone_masked")
        elif "*" not in str(seller.get("public_phone_masked")):
            issues.append("seller_public_phone_not_masked")
        if not (
            has_value(seller.get("source_account_id"))
            or has_value(seller.get("profile_url"))
        ):
            issues.append("missing_stable_seller_reference")
        seller_key = seller.get("source_account_id") or seller.get("profile_url")
        if seller_key is not None and len(str(seller_key)) > 255:
            issues.append("seller_key_too_long")
        for field_name, maximum in (
            ("source_account_id", 100),
            ("display_name", 200),
            ("public_phone_masked", 50),
            ("joined_text", 100),
        ):
            value = seller.get(field_name)
            if value is not None and len(str(value)) > maximum:
                issues.append(f"seller_{field_name}_too_long")
        active_listing_count = seller.get("active_listing_count")
        if active_listing_count is not None and (
            not isinstance(active_listing_count, int)
            or not 0 <= active_listing_count <= 2_147_483_647
        ):
            issues.append("invalid_seller_active_listing_count")

    image_count = sum(
        1
        for media in record.get("media", [])
        if isinstance(media, dict) and media.get("type") == "IMAGE"
    )
    if image_count < MIN_IMAGE_COUNT:
        issues.append("insufficient_images")
    cover_count = sum(
        1
        for media_item in record.get("media", [])
        if isinstance(media_item, dict) and media_item.get("is_cover") is True
    )
    if cover_count != 1:
        issues.append("invalid_media_cover_count")
    for index, media_item in enumerate(record.get("media", [])):
        if not isinstance(media_item, dict):
            issues.append(f"invalid_media_{index}")
            continue
        if media_item.get("type") not in {
            "IMAGE",
            "VIDEO",
            "FLOOR_PLAN",
            "VIRTUAL_TOUR",
        }:
            issues.append(f"invalid_media_type_{index}")
        if not has_value(media_item.get("url")):
            issues.append(f"missing_media_url_{index}")
        caption = media_item.get("caption")
        if caption is not None and len(str(caption)) > 255:
            issues.append(f"media_caption_too_long_{index}")
        sort_order = media_item.get("sort_order")
        if not isinstance(sort_order, int) or not 0 <= sort_order <= 32_767:
            issues.append(f"invalid_media_sort_order_{index}")

    free_text_values = [title, description]
    free_text_values.extend(
        str(item.get("raw_value") or "")
        for item in record.get("raw_attributes", [])
        if isinstance(item, dict)
    )
    if any(
        PUBLIC_EMAIL_PATTERN.search(value) or PUBLIC_VN_PHONE_PATTERN.search(value)
        for value in free_text_values
    ):
        issues.append("unredacted_public_contact")

    kind = record.get("property_kind")
    if kind == "LAND":
        for field_name in ("frontage_m", "road_width_m", "orientation"):
            if not has_value(record.get(field_name)):
                issues.append(f"missing_land_{field_name}")
    elif kind == "APARTMENT":
        # The public detail card consistently exposes area, price, bedrooms and
        # bathrooms. Floor, furniture and orientation are useful enrichment but
        # are not shown for every otherwise complete listing.
        for field_name in ("bedrooms", "bathrooms"):
            if not has_value(record.get(field_name)):
                issues.append(f"missing_apartment_{field_name}")
    elif kind in {"HOUSE", "VILLA", "TOWNHOUSE"}:
        for field_name in ("bedrooms", "bathrooms", "total_floors"):
            if not has_value(record.get(field_name)):
                issues.append(f"missing_building_{field_name}")
    elif kind == "COMMERCIAL":
        frontage_set = has_value(record.get("frontage_m")) and has_value(
            record.get("road_width_m")
        )
        floors_set = has_value(record.get("total_floors")) and has_value(
            record.get("usable_area_sqm")
        )
        if not (frontage_set or floors_set):
            issues.append("missing_commercial_dimensions")

    return sorted(set(issues))


def parse_listing_html(
    html_text: str,
    source_url: str,
    *,
    crawled_at: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if is_challenge_page(html_text):
        raise AccessBlocked("Cloudflare/browser challenge detected in listing HTML")

    try:
        canonical_url = canonical_listing_url(source_url)
    except ValueError as exc:
        return None, [f"invalid_source_url:{exc}"]
    source_listing_id = listing_id_from_url(canonical_url)
    if source_listing_id is None:
        return None, ["missing_source_listing_id"]

    root = parse_html_tree(html_text)
    meta = extract_meta(root)
    tracking = extract_tracking_product(html_text)
    json_ld = extract_json_ld(root)

    page_listing_ids: set[str] = set()
    tracking_id = tracking.get("productId")
    if tracking_id is not None and str(tracking_id).isdigit():
        page_listing_ids.add(str(tracking_id))
    product_root = first_node_with_class(root, "js__product-detail-web")
    if product_root is not None:
        dom_id = product_root.attrs.get("prid")
        if dom_id and dom_id.isdigit():
            page_listing_ids.add(dom_id)
    for url_key in ("og:url",):
        page_url = meta.get(url_key)
        page_id = listing_id_from_url(page_url) if page_url else None
        if page_id:
            page_listing_ids.add(page_id)
    for item in json_ld:
        for value in (item.get("url"), item.get("@id")):
            page_id = listing_id_from_url(value) if isinstance(value, str) else None
            if page_id:
                page_listing_ids.add(page_id)
    if not page_listing_ids:
        return None, ["missing_page_listing_id"]
    if page_listing_ids != {source_listing_id}:
        found_ids = ",".join(sorted(page_listing_ids))
        return None, [f"source_listing_id_mismatch:{found_ids}"]

    title_node = first_node_with_class(root, "re__pr-title", "js__pr-title")
    title = node_text(title_node) if title_node is not None else meta.get("og:title", "")

    description_node = first_node_with_class(root, "js__pr-description")
    description = (
        node_text(description_node, preserve_breaks=True)
        if description_node is not None
        else meta.get("description", "")
    )
    title, title_redactions = redact_public_contact(title)
    description, description_redactions = redact_public_contact(description)
    privacy_redaction_count = title_redactions + description_redactions

    address_node = first_node_with_class(
        root,
        "re__address-line-1",
        "re__pr-short-description",
        "re__pr-short__address",
    )
    address = node_text(address_node) if address_node is not None else ""
    old_address_node = first_node_with_class(root, "re__address-line-2")
    source_secondary_address = (
        node_text(old_address_node) if old_address_node is not None else None
    )
    ward, district, province = split_address(address)

    short_blocks = extract_labeled_blocks(
        root,
        item_classes=("re__pr-short-info-item", "js__pr-short-info-item"),
        title_classes=("title",),
        value_classes=("value",),
        extension_classes=("ext",),
    )
    spec_blocks = extract_labeled_blocks(
        root,
        item_classes=("re__pr-specs-content-item",),
        title_classes=("re__pr-specs-content-item-title",),
        value_classes=("re__pr-specs-content-item-value",),
    )
    short_map, spec_map = blocks_by_label(short_blocks), blocks_by_label(spec_blocks)

    price_block = first_block(short_map, "Khoảng giá", "Mức giá", "Giá bán")
    area_block = first_block(short_map, "Diện tích") or first_block(
        spec_map, "Diện tích"
    )
    price = parse_vnd(price_block["value"] if price_block else None)
    area_sqm = parse_measurement(area_block["value"] if area_block else None)

    source_price_per_sqm = None
    if price_block:
        source_price_per_sqm = parse_vnd(price_block.get("extension"))
    spec_price_block = first_block(spec_map, "Khoảng giá", "Giá/m²")
    if source_price_per_sqm is None and spec_price_block:
        source_price_per_sqm = parse_vnd(spec_price_block["value"])
    price_per_sqm = (
        int(Decimal(price) / Decimal(str(area_sqm)))
        if isinstance(price, int) and price > 0 and area_sqm and area_sqm > 0
        else None
    )

    raw_attributes: list[dict[str, Any]] = []
    normalized_values: dict[str, Any] = {}
    for block in spec_blocks:
        key = attribute_key(block["label"])
        normalized_value = normalized_attribute_value(key, block["value"])
        safe_label, label_redactions = redact_public_contact(block["label"])
        safe_value, value_redactions = redact_public_contact(block["value"])
        privacy_redaction_count += label_redactions + value_redactions
        raw_attributes.append(
            {
                "label": safe_label,
                "raw_value": safe_value,
                "normalized_key": key,
                "normalized_value": normalized_value,
            }
        )
        if key and has_value(normalized_value):
            normalized_values.setdefault(key, normalized_value)

    property_kind = extract_property_kind(canonical_url, spec_map)
    latitude, longitude = extract_coordinates(html_text)
    seller = extract_seller(root, html_text, tracking)
    media, source_videos = extract_media(html_text, meta, source_listing_id)
    project = extract_project(root, spec_map)
    detail_root = product_root or root
    market_insights = extract_market_insights(detail_root, html_text)
    listing_metadata = extract_listing_metadata(root, source_listing_id)

    published_at = None
    source_updated_at = None
    for item in json_ld:
        item_type = item.get("@type")
        if item_type != "RealEstateListing":
            continue
        published_at = normalize_iso_timestamp(
            item.get("@datePublished") or item.get("datePublished")
        )
        source_updated_at = normalize_iso_timestamp(
            item.get("@dateModified") or item.get("dateModified")
        )
        break

    listing_type = "SALE" if urlparse(canonical_url).path.startswith("/ban-") else None
    expired = bool(tracking.get("expired"))
    status = "HIDDEN" if expired else "AVAILABLE"

    record: dict[str, Any] = {
        "schema_version": "batdongsan-v1",
        "property_id": f"BDS_PR{source_listing_id}",
        "source": "BATDONGSAN_COM_VN",
        "source_listing_id": source_listing_id,
        "source_url": canonical_url,
        "source_category": urlparse(canonical_url).path.split("/")[1],
        "listing_type": listing_type,
        "price_period": "TOTAL",
        "property_kind": property_kind,
        "title": title,
        "description": description,
        "status": status,
        "price": price,
        "price_per_sqm": price_per_sqm,
        "source_price_per_sqm": source_price_per_sqm,
        "currency": "VND",
        "area_sqm": area_sqm,
        "usable_area_sqm": normalized_values.get("usable_area_sqm"),
        "address": address,
        "source_secondary_address": source_secondary_address,
        "ward": ward,
        "district": district,
        "province": province,
        "latitude": latitude,
        "longitude": longitude,
        "bedrooms": normalized_values.get("bedrooms"),
        "bathrooms": normalized_values.get("bathrooms"),
        "floor_number": normalized_values.get("floor_number"),
        "total_floors": normalized_values.get("total_floors"),
        "orientation": normalized_values.get("orientation"),
        "balcony_orientation": normalized_values.get("balcony_orientation"),
        "legal_status": normalized_values.get("legal_status"),
        "furniture_status": normalized_values.get("furniture_status"),
        "frontage_m": normalized_values.get("frontage_m"),
        "road_width_m": normalized_values.get("road_width_m"),
        "parcel_number": normalized_values.get("parcel_number"),
        "map_sheet_number": normalized_values.get("map_sheet_number"),
        "land_use_purpose": normalized_values.get("land_use_purpose"),
        "land_use_term": normalized_values.get("land_use_term"),
        "commercial_subtype": (
            normalized_values.get("source_property_type")
            if property_kind == "COMMERCIAL"
            else None
        ),
        "project": project,
        "seller": seller,
        "media": media,
        "source_videos": source_videos,
        "raw_attributes": raw_attributes,
        "market_insights": market_insights,
        "source_listing_metadata": listing_metadata,
        "privacy": {
            "free_text_contact_redactions": privacy_redaction_count,
            "direct_contact_policy": "MASKED_PUBLIC_PHONE_ONLY",
        },
        "verification": {
            "source_verified": bool(tracking.get("verified")),
            "source_vip_type": tracking.get("vipType"),
        },
        "source_product_type": tracking.get("productType"),
        "published_at": published_at,
        "source_updated_at": source_updated_at,
        "crawled_at": crawled_at,
        "last_seen_at": crawled_at,
    }

    digest_payload = {
        key: value
        for key, value in record.items()
        if key not in {"crawled_at", "last_seen_at", "content_sha256"}
    }
    record["content_sha256"] = hashlib.sha256(
        json.dumps(
            digest_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    issues = listing_issues(record)
    return (None, issues) if issues else (record, [])


def semantic_key(record: dict[str, Any]) -> str:
    seller_id = record.get("seller", {}).get("source_account_id", "")
    payload = "|".join(
        (
            str(seller_id),
            normalize_label(record.get("description")),
            normalize_label(record.get("address")),
            str(record.get("area_sqm")),
            str(record.get("price")),
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def deduplicate_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    by_listing_id: dict[str, dict[str, Any]] = {}
    for record in records:
        by_listing_id[str(record["source_listing_id"])] = record

    by_semantic_key: dict[str, dict[str, Any]] = {}
    removed: list[str] = []
    for record in by_listing_id.values():
        key = semantic_key(record)
        previous = by_semantic_key.get(key)
        if previous is None:
            by_semantic_key[key] = record
            continue
        previous_date = previous.get("published_at") or ""
        current_date = record.get("published_at") or ""
        if current_date > previous_date:
            removed.append(previous["property_id"])
            by_semantic_key[key] = record
        else:
            removed.append(record["property_id"])

    unique = sorted(
        by_semantic_key.values(),
        key=lambda item: (item.get("published_at") or "", item["source_listing_id"]),
        reverse=True,
    )
    return unique, sorted(removed)


def sql_string(value: Any) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def sql_number(value: Any, *, decimals: int | None = None) -> str:
    if value is None:
        return "NULL"
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value: {value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"Non-finite numeric value: {value!r}")
    if decimals is not None:
        number = number.quantize(Decimal(1).scaleb(-decimals))
    return format(number, "f")


def deterministic_property_uuid(record: dict[str, Any]) -> uuid.UUID:
    return uuid.uuid5(
        PROPERTY_NAMESPACE,
        f"{record['source']}:{record['source_listing_id']}",
    )


def deterministic_media_uuid(record: dict[str, Any], media: dict[str, Any]) -> uuid.UUID:
    return uuid.uuid5(
        MEDIA_NAMESPACE,
        f"{record['source']}:{record['source_listing_id']}:{media['type']}:{media['url']}",
    )


def external_seller_key(record: dict[str, Any]) -> str:
    seller = record["seller"]
    account_id = seller.get("source_account_id")
    if has_value(account_id):
        return str(account_id)
    profile_url = seller.get("profile_url")
    if not has_value(profile_url):
        raise ValueError("External seller requires a stable source key")
    parsed = urlparse(str(profile_url))
    canonical_profile = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            "",
            "",
        )
    )
    digest = hashlib.sha256(canonical_profile.encode("utf-8")).hexdigest()
    return f"profile_sha256:{digest}"


def deterministic_external_seller_uuid(record: dict[str, Any]) -> uuid.UUID:
    return uuid.uuid5(
        EXTERNAL_SELLER_NAMESPACE,
        f"{record['source']}:{external_seller_key(record)}",
    )


def assigned_demo_sale_user_id(record: dict[str, Any]) -> str:
    digest = uuid.uuid5(
        PROPERTY_NAMESPACE,
        f"demo-sale:{record['source']}:{record['source_listing_id']}",
    )
    return DEMO_SALE_USER_IDS[digest.int % len(DEMO_SALE_USER_IDS)]


def external_seller_upsert(record: dict[str, Any]) -> str:
    seller = record["seller"]
    seller_uuid = deterministic_external_seller_uuid(record)
    seller_key = external_seller_key(record)
    account_type = str(seller.get("account_type") or "UNKNOWN").upper()
    seller_type = account_type if account_type in {
        "OWNER",
        "BROKER",
        "COMPANY",
        "UNKNOWN",
    } else "UNKNOWN"
    raw_data = json.dumps(
        {
            "has_broker_badge": seller.get("has_broker_badge"),
            "public_details": seller.get("public_details", {}),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    source_account_id = seller.get("source_account_id")
    is_company_sql = "TRUE" if seller_type == "COMPANY" else "NULL"
    seen_at = record["crawled_at"]
    return (
        "INSERT INTO external_sellers "
        "(id, source, source_seller_key, source_account_id, display_name, seller_type, "
        "is_company, source_verified, is_professional, profile_url, avatar_url, "
        "public_phone_masked, joined_text, active_listing_count, has_zalo, has_chat, "
        "raw_data, first_seen_at, last_seen_at) VALUES "
        f"({sql_string(seller_uuid)}, {sql_string(record['source'])}, "
        f"{sql_string(seller_key)}, {sql_string(source_account_id)}, "
        f"{sql_string(seller['display_name'])}, {sql_string(seller_type)}, "
        f"{is_company_sql}, "
        f"{'TRUE' if seller.get('source_verified_flag') else 'FALSE'}, "
        f"{'TRUE' if seller.get('is_professional') else 'FALSE'}, "
        f"{sql_string(seller.get('profile_url'))}, {sql_string(seller.get('avatar_url'))}, "
        f"{sql_string(seller.get('public_phone_masked'))}, "
        f"{sql_string(seller.get('joined_text'))}, "
        f"{sql_number(seller.get('active_listing_count'))}, "
        f"{'TRUE' if seller.get('has_zalo') else 'FALSE'}, "
        f"{'TRUE' if seller.get('has_chat') else 'FALSE'}, "
        f"{sql_string(raw_data)}::jsonb, {sql_string(seen_at)}::timestamptz, "
        f"{sql_string(seen_at)}::timestamptz) "
        "ON CONFLICT (source, source_seller_key) DO UPDATE SET "
        "source_account_id = COALESCE(EXCLUDED.source_account_id, external_sellers.source_account_id), "
        "display_name = EXCLUDED.display_name, "
        "seller_type = CASE WHEN EXCLUDED.seller_type = 'UNKNOWN' "
        "THEN external_sellers.seller_type ELSE EXCLUDED.seller_type END, "
        "is_company = COALESCE(EXCLUDED.is_company, external_sellers.is_company), "
        "source_verified = COALESCE(EXCLUDED.source_verified, external_sellers.source_verified), "
        "is_professional = COALESCE(EXCLUDED.is_professional, external_sellers.is_professional), "
        "profile_url = COALESCE(EXCLUDED.profile_url, external_sellers.profile_url), "
        "avatar_url = COALESCE(EXCLUDED.avatar_url, external_sellers.avatar_url), "
        "public_phone_masked = COALESCE(EXCLUDED.public_phone_masked, external_sellers.public_phone_masked), "
        "joined_text = COALESCE(EXCLUDED.joined_text, external_sellers.joined_text), "
        "active_listing_count = COALESCE(EXCLUDED.active_listing_count, external_sellers.active_listing_count), "
        "has_zalo = COALESCE(EXCLUDED.has_zalo, external_sellers.has_zalo), "
        "has_chat = COALESCE(EXCLUDED.has_chat, external_sellers.has_chat), "
        "raw_data = external_sellers.raw_data || EXCLUDED.raw_data, "
        "first_seen_at = LEAST(external_sellers.first_seen_at, EXCLUDED.first_seen_at), "
        "last_seen_at = GREATEST(external_sellers.last_seen_at, EXCLUDED.last_seen_at), "
        "updated_at = now();"
    )


def property_external_seller_upsert(record: dict[str, Any]) -> list[str]:
    property_code = sql_string(record["property_id"])
    property_id_sql = (
        f"(SELECT id FROM properties WHERE code = {property_code})"
    )
    seller_id_sql = (
        "(SELECT id FROM external_sellers WHERE "
        f"source = {sql_string(record['source'])} AND "
        f"source_seller_key = {sql_string(external_seller_key(record))})"
    )
    seen_at = record["crawled_at"]
    metadata = json.dumps(
        {"source_category": record.get("source_category")},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return [
        "UPDATE property_external_sellers SET is_primary = FALSE, updated_at = now() "
        f"WHERE property_id = {property_id_sql} "
        f"AND external_seller_id <> {seller_id_sql} AND is_primary = TRUE;",
        "INSERT INTO property_external_sellers "
        "(property_id, external_seller_id, relationship_type, is_primary, "
        "source_listing_id, source_url, first_seen_at, last_seen_at, metadata) VALUES "
        f"({property_id_sql}, {seller_id_sql}, 'LISTING_POSTER', TRUE, "
        f"{sql_string(record['source_listing_id'])}, {sql_string(record['source_url'])}, "
        f"{sql_string(seen_at)}::timestamptz, {sql_string(seen_at)}::timestamptz, "
        f"{sql_string(metadata)}::jsonb) "
        "ON CONFLICT (property_id, external_seller_id) DO UPDATE SET "
        "relationship_type = EXCLUDED.relationship_type, is_primary = TRUE, "
        "source_listing_id = EXCLUDED.source_listing_id, source_url = EXCLUDED.source_url, "
        "first_seen_at = LEAST(property_external_sellers.first_seen_at, EXCLUDED.first_seen_at), "
        "last_seen_at = GREATEST(property_external_sellers.last_seen_at, EXCLUDED.last_seen_at), "
        "metadata = property_external_sellers.metadata || EXCLUDED.metadata, "
        "updated_at = now();",
    ]


def demo_sale_assignment_insert(record: dict[str, Any]) -> str:
    property_code = sql_string(record["property_id"])
    property_id_sql = (
        f"(SELECT id FROM properties WHERE code = {property_code})"
    )
    sale_user_id = sql_string(assigned_demo_sale_user_id(record))
    assigned_at = sql_string(record["crawled_at"])
    return (
        "INSERT INTO property_sale_assignments "
        "(property_id, sale_user_id, is_primary, assigned_at) "
        f"SELECT {property_id_sql}, {sale_user_id}, TRUE, {assigned_at}::timestamptz "
        "WHERE NOT EXISTS (SELECT 1 FROM property_sale_assignments current_assignment "
        f"WHERE current_assignment.property_id = {property_id_sql} "
        "AND current_assignment.is_primary = TRUE AND current_assignment.unassigned_at IS NULL) "
        "ON CONFLICT (property_id, sale_user_id) DO NOTHING;"
    )


def record_features(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": record["schema_version"],
        "source": record["source"],
        "source_listing_id": record["source_listing_id"],
        "source_url": record["source_url"],
        "source_category": record["source_category"],
        "source_product_type": record.get("source_product_type"),
        "listing_type": record["listing_type"],
        "price_period": record["price_period"],
        "price_per_sqm": record["price_per_sqm"],
        "source_price_per_sqm": record.get("source_price_per_sqm"),
        "source_secondary_address": record.get("source_secondary_address"),
        "total_floors": record.get("total_floors"),
        "balcony_orientation": record.get("balcony_orientation"),
        "furniture_status": record.get("furniture_status"),
        "commercial_subtype": record.get("commercial_subtype"),
        "project": record.get("project"),
        "seller": record["seller"],
        "source_videos": record.get("source_videos", []),
        "raw_attributes": record["raw_attributes"],
        "market_insights": record["market_insights"],
        "source_listing_metadata": record.get("source_listing_metadata", {}),
        "privacy": record.get("privacy", {}),
        "verification": record["verification"],
        "source_updated_at": record.get("source_updated_at"),
        "crawled_at": record["crawled_at"],
        "last_seen_at": record["last_seen_at"],
        "content_sha256": record["content_sha256"],
    }


def property_upsert(record: dict[str, Any]) -> str:
    property_uuid = deterministic_property_uuid(record)
    features_json = json.dumps(
        record_features(record),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    columns = (
        "id, code, property_kind, title, description, status, address_line, "
        "ward, district, province, latitude, longitude, area_sqm, usable_area_sqm, "
        "bedrooms, bathrooms, floor_number, orientation, legal_status, list_price, "
        "currency, parcel_number, map_sheet_number, land_use_purpose, land_use_term, "
        "frontage_m, road_width_m, features, published_at"
    )
    values = ", ".join(
        (
            sql_string(property_uuid),
            sql_string(record["property_id"]),
            sql_string(record["property_kind"]),
            sql_string(record["title"]),
            sql_string(record["description"]),
            sql_string(record["status"]),
            sql_string(record["address"]),
            sql_string(record["ward"]),
            sql_string(record["district"]),
            sql_string(record["province"]),
            sql_number(record["latitude"], decimals=6),
            sql_number(record["longitude"], decimals=6),
            sql_number(record["area_sqm"], decimals=2),
            sql_number(record.get("usable_area_sqm"), decimals=2),
            sql_number(record.get("bedrooms")),
            sql_number(record.get("bathrooms")),
            sql_number(record.get("floor_number")),
            sql_string(record.get("orientation")),
            sql_string(record.get("legal_status")),
            sql_number(record["price"], decimals=2),
            sql_string(record["currency"]),
            sql_string(record.get("parcel_number")),
            sql_string(record.get("map_sheet_number")),
            sql_string(record.get("land_use_purpose")),
            sql_string(record.get("land_use_term")),
            sql_number(record.get("frontage_m"), decimals=2),
            sql_number(record.get("road_width_m"), decimals=2),
            f"{sql_string(features_json)}::jsonb",
            f"{sql_string(record['published_at'])}::timestamptz",
        )
    )
    updates = ", ".join(
        f"{column} = EXCLUDED.{column}"
        for column in (
            "property_kind",
            "title",
            "description",
            "address_line",
            "ward",
            "district",
            "province",
            "latitude",
            "longitude",
            "area_sqm",
            "usable_area_sqm",
            "bedrooms",
            "bathrooms",
            "floor_number",
            "orientation",
            "legal_status",
            "list_price",
            "currency",
            "parcel_number",
            "map_sheet_number",
            "land_use_purpose",
            "land_use_term",
            "frontage_m",
            "road_width_m",
            "features",
            "published_at",
        )
    )
    return (
        f"INSERT INTO properties ({columns}) VALUES ({values}) "
        f"ON CONFLICT (code) DO UPDATE SET {updates}, "
        "status = CASE WHEN properties.status IN ('DRAFT', 'AVAILABLE') "
        "THEN EXCLUDED.status ELSE properties.status END, updated_at = now();"
    )


def media_insert(record: dict[str, Any], media: dict[str, Any]) -> str:
    media_uuid = deterministic_media_uuid(record, media)
    property_code = sql_string(record["property_id"])
    requested_cover = bool(media.get("is_cover"))
    cover_sql = "FALSE"
    if requested_cover:
        cover_sql = (
            "NOT EXISTS (SELECT 1 FROM property_media existing_media "
            f"WHERE existing_media.property_id = (SELECT id FROM properties WHERE code = {property_code}) "
            "AND existing_media.is_cover)"
        )
    return (
        "INSERT INTO property_media "
        "(id, property_id, media_type, url, source, caption, sort_order, is_cover) VALUES "
        f"({sql_string(media_uuid)}, "
        f"(SELECT id FROM properties WHERE code = {property_code}), "
        f"{sql_string(media['type'])}, {sql_string(media['url'])}, "
        f"{sql_string(record['source'])}, {sql_string(media.get('caption'))}, "
        f"{int(media['sort_order'])}, "
        f"{cover_sql}) "
        "ON CONFLICT (id) DO UPDATE SET "
        "property_id = EXCLUDED.property_id, media_type = EXCLUDED.media_type, "
        "url = EXCLUDED.url, source = EXCLUDED.source, caption = EXCLUDED.caption, "
        "sort_order = EXCLUDED.sort_order, is_cover = EXCLUDED.is_cover;"
    )


def generate_sql(records: list[dict[str, Any]]) -> str:
    if not records:
        raise ValueError("No complete Batdongsan listings to write")
    validation_errors: list[str] = []
    seen_codes: set[str] = set()
    for index, record in enumerate(records):
        issues = listing_issues(record)
        if issues:
            validation_errors.append(
                f"record[{index}] {record.get('property_id', '<unknown>')}: "
                + ", ".join(issues)
            )
        code = record.get("property_id")
        if code in seen_codes:
            validation_errors.append(f"record[{index}] duplicate code: {code}")
        elif isinstance(code, str):
            seen_codes.add(code)
    if validation_errors:
        raise ValueError("Strict validation failed:\n" + "\n".join(validation_errors[:20]))

    lines = [
        "-- Complete public Batdongsan.com.vn property data.",
        "-- Generated by database/crawler_batdongsan.py.",
        "-- External posters are normalized separately from internal login users and sales.",
        "-- New properties receive one deterministic demo sale assignment if none exists.",
        "BEGIN;",
        "SET LOCAL client_encoding = 'UTF8';",
        "",
    ]
    for record in records:
        lines.append(property_upsert(record))
        lines.append(external_seller_upsert(record))
        lines.extend(property_external_seller_upsert(record))
        lines.append(demo_sale_assignment_insert(record))
        lines.append(
            "DELETE FROM property_media WHERE property_id = "
            f"(SELECT id FROM properties WHERE code = {sql_string(record['property_id'])}) "
            f"AND source = {sql_string(record['source'])};"
        )
        for media in record["media"]:
            lines.append(media_insert(record, media))
        lines.append("")
    lines.extend(("COMMIT;", ""))
    return "\n".join(lines)


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
        temporary_file.write(content)
    os.replace(temporary_path, path)


def load_record_checkpoint(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CrawlError(f"Cannot read record checkpoint {path}: {exc}") from exc
    if not isinstance(payload, list):
        raise CrawlError(f"Record checkpoint must contain a JSON list: {path}")

    records: list[dict[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise CrawlError(f"Checkpoint record[{index}] is not an object")
        issues = listing_issues(item)
        if issues:
            raise CrawlError(
                f"Checkpoint record[{index}] failed validation: {', '.join(issues)}"
            )
        records.append(item)
    unique, _ = deduplicate_records(records)
    return unique


def write_record_checkpoint(path: Path, records: list[dict[str, Any]]) -> None:
    unique, _ = deduplicate_records(records)
    atomic_write_text(
        path,
        json.dumps(unique, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def crawl_report(
    records: list[dict[str, Any]],
    rejected: Counter[str],
    removed: list[str],
    *,
    start_urls: list[str],
    resumed_count: int,
    blocked_reason: str | None,
) -> dict[str, Any]:
    seller_keys = {
        (record["source"], external_seller_key(record)) for record in records
    }
    image_counts = [
        sum(1 for media in record["media"] if media.get("type") == "IMAGE")
        for record in records
    ]
    by_kind = Counter(str(record["property_kind"]) for record in records)
    by_province = Counter(str(record["province"]) for record in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "BATDONGSAN_COM_VN",
        "start_urls": start_urls,
        "accepted_count": len(records),
        "resumed_count": resumed_count,
        "unique_seller_count": len(seller_keys),
        "media_count": sum(len(record["media"]) for record in records),
        "image_count": sum(image_counts),
        "minimum_images_per_property": min(image_counts) if image_counts else 0,
        "all_have_masked_seller_phone": all(
            has_value(record["seller"].get("public_phone_masked"))
            and "*" in str(record["seller"].get("public_phone_masked"))
            for record in records
        ),
        "all_have_legal_status": all(
            has_value(record.get("legal_status")) for record in records
        ),
        "all_have_coordinates": all(
            has_value(record.get("latitude")) and has_value(record.get("longitude"))
            for record in records
        ),
        "by_property_kind": dict(sorted(by_kind.items())),
        "by_province": dict(sorted(by_province.items())),
        "rejection_reasons": dict(rejected.most_common()),
        "semantic_reposts_removed": removed,
        "blocked_reason": blocked_reason,
    }


def collect_candidate_urls(
    fetcher: PublicFetcher,
    robots_parser: RobotFileParser,
    start_urls: list[str],
    *,
    max_pages: int,
) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for start_url in start_urls:
        if listing_id_from_url(start_url):
            normalized = canonical_listing_url(start_url)
            if normalized not in seen:
                seen.add(normalized)
                candidates.append(normalized)
            continue
        for page_number in range(1, max_pages + 1):
            page_url = pagination_url(start_url, page_number)
            ensure_url_allowed(robots_parser, page_url)
            html_text = fetcher.fetch_text(page_url)
            page_candidates = discover_listing_urls(html_text, page_url)
            if not page_candidates:
                break
            added = 0
            for candidate in page_candidates:
                if candidate in seen:
                    continue
                seen.add(candidate)
                candidates.append(candidate)
                added += 1
            if added == 0:
                break
            print(
                f"Discovered {len(page_candidates)} listing links from {page_url}",
                file=sys.stderr,
            )
    return candidates


def crawl(
    start_urls: list[str],
    *,
    target: int,
    max_pages: int,
    timeout_seconds: float,
    retries: int,
    delay_seconds: float,
    jitter_seconds: float,
    initial_records: list[dict[str, Any]] | None = None,
    checkpoint: Callable[[list[dict[str, Any]]], None] | None = None,
) -> tuple[list[dict[str, Any]], Counter[str], list[str]]:
    accepted, initial_removed = deduplicate_records(list(initial_records or []))
    if target > 0 and len(accepted) >= target:
        return accepted[:target], Counter(), initial_removed

    normalized_starts = [canonical_start_url(url) for url in start_urls]
    fetcher = PublicFetcher(
        timeout_seconds=timeout_seconds,
        retries=retries,
        delay_seconds=delay_seconds,
        jitter_seconds=jitter_seconds,
    )
    robots_parser = ensure_robots_allowed(fetcher, normalized_starts)
    candidates = collect_candidate_urls(
        fetcher,
        robots_parser,
        normalized_starts,
        max_pages=max_pages,
    )
    if not candidates:
        raise CrawlError("No listing links were discovered")

    crawled_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rejected: Counter[str] = Counter()
    known_listing_ids = {
        str(record["source_listing_id"]) for record in accepted
    }
    for index, listing_url in enumerate(candidates, start=1):
        current_unique, _ = deduplicate_records(accepted)
        if target > 0 and len(current_unique) >= target:
            break
        candidate_id = listing_id_from_url(listing_url)
        if candidate_id in known_listing_ids:
            continue
        try:
            ensure_url_allowed(robots_parser, listing_url)
            html_text = fetcher.fetch_text(listing_url)
            record, issues = parse_listing_html(
                html_text,
                listing_url,
                crawled_at=crawled_at,
            )
        except AccessBlocked as exc:
            rejected["access_blocked"] += 1
            print(f"Stopped on access challenge: {exc}", file=sys.stderr)
            break
        except CrawlError as exc:
            rejected[f"fetch_error:{type(exc).__name__}"] += 1
            print(f"Skipped fetch failure {listing_url}: {exc}", file=sys.stderr)
            continue
        if issues or record is None:
            rejected.update(issues or ["unknown_parse_failure"])
            print(
                f"Rejected {listing_url}: {', '.join(issues or ['unknown'])}",
                file=sys.stderr,
            )
            continue
        accepted.append(record)
        known_listing_ids.add(str(record["source_listing_id"]))
        current_unique, _ = deduplicate_records(accepted)
        if checkpoint is not None:
            checkpoint(current_unique)
        print(
            f"Accepted {len(current_unique)} listing(s); scanned {index}/{len(candidates)}",
            file=sys.stderr,
        )

    unique, removed = deduplicate_records(accepted)
    if target > 0:
        unique = unique[:target]
    return unique, rejected, removed


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=(
            "Crawl complete public Batdongsan.com.vn sale listings and write "
            "an idempotent PostgreSQL SQL file."
        )
    )
    parser.add_argument(
        "urls",
        nargs="*",
        default=[DEFAULT_START_URL],
        help="Detail URL(s) or category URL(s); defaults to the verified land sample.",
    )
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--jitter", type=float, default=DEFAULT_JITTER_SECONDS)
    parser.add_argument(
        "--output",
        type=Path,
        default=base_dir / "005_batdongsan_data.sql",
    )
    parser.add_argument(
        "--records-output",
        type=Path,
        default=base_dir / "batdongsan_records.json",
        help="Validated JSON checkpoint written after every accepted listing.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=base_dir / "batdongsan_crawl_report.json",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Merge new listings with the validated --records-output checkpoint.",
    )
    args = parser.parse_args()
    if args.target < 0:
        parser.error("--target must be >= 0; use 0 for every discovered listing")
    if args.max_pages <= 0:
        parser.error("--max-pages must be > 0")
    if args.timeout <= 0 or args.retries < 0:
        parser.error("--timeout must be > 0 and --retries must be >= 0")
    if args.delay < MIN_DELAY_SECONDS:
        parser.error(f"--delay must be at least {MIN_DELAY_SECONDS} seconds")
    if args.jitter < 0:
        parser.error("--jitter must be >= 0")
    return args


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    records_path = args.records_output.resolve()
    report_path = args.report.resolve()
    initial_records = load_record_checkpoint(records_path) if args.resume else []
    blocked_reason: str | None = None
    try:
        records, rejected, removed = crawl(
            args.urls,
            target=args.target,
            max_pages=args.max_pages,
            timeout_seconds=args.timeout,
            retries=args.retries,
            delay_seconds=args.delay,
            jitter_seconds=args.jitter,
            initial_records=initial_records,
            checkpoint=lambda rows: write_record_checkpoint(records_path, rows),
        )
    except AccessBlocked as exc:
        blocked_reason = str(exc)
        rejected = Counter({"access_blocked": 1})
        removed = []
        records = load_record_checkpoint(records_path) if records_path.exists() else initial_records
        if records:
            print(
                f"Stopped on access challenge; preserving {len(records)} checkpointed listing(s)",
                file=sys.stderr,
            )

    if not records:
        report = crawl_report(
            records,
            rejected,
            removed,
            start_urls=[canonical_start_url(url) for url in args.urls],
            resumed_count=len(initial_records),
            blocked_reason=blocked_reason,
        )
        atomic_write_text(
            report_path,
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        preview = ", ".join(f"{key}={value}" for key, value in rejected.most_common(15))
        raise CrawlError(f"No complete listing passed strict validation. {preview}")

    write_record_checkpoint(records_path, records)
    sql_text = generate_sql(records)
    output_path = args.output.resolve()
    atomic_write_text(output_path, sql_text)
    report = crawl_report(
        records,
        rejected,
        removed,
        start_urls=[canonical_start_url(url) for url in args.urls],
        resumed_count=len(initial_records),
        blocked_reason=blocked_reason,
    )
    atomic_write_text(
        report_path,
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    print(
        f"Saved {len(records)} complete Batdongsan listing(s) to {output_path}",
    )
    print(
        f"Media: {sum(len(record['media']) for record in records)}; "
        f"semantic reposts removed: {len(removed)}",
    )
    print(f"Checkpoint: {records_path}; report: {report_path}")
    if rejected:
        print(
            "Top rejection reasons: "
            + ", ".join(f"{key}={value}" for key, value in rejected.most_common(15))
        )


if __name__ == "__main__":
    main()
