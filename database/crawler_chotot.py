"""Crawl and normalize complete apartment listings from Nha Tot.

Only public listing data required by the property catalogue is retained. The
pipeline intentionally does not create fake customers, internal sales users,
or appointments. Listings that miss any strict catalogue field are skipped.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://gateway.chotot.com/v1/public/ad-listing"
DEFAULT_REGION_ID = 12000  # Ha Noi
DEFAULT_CATEGORY_ID = 1010  # Can ho/chung cu
DEFAULT_BATCH_SIZE = 50
DEFAULT_TARGET = 200
DEFAULT_MAX_PAGES = 100
DEFAULT_LISTING_TYPE = "SALE"
MIN_IMAGE_COUNT = 3

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36 XHomeVisitOpsDataCollector/2.0"
)

SALE_PRICE_VND_RANGE = (100_000_000, 200_000_000_000)
SALE_PRICE_PER_SQM_RANGE = (3_000_000, 500_000_000)

LIST_REQUIRED_FIELDS = (
    "list_id",
    "subject",
    "body",
    "type",
    "price",
    "size",
    "street_name",
    "ward_name",
    "area_name",
    "region_name",
    "latitude",
    "longitude",
    "rooms",
    "apartment_type",
    "account_id",
    "account_name",
)

# Every one of these is nullable in the schema and every search filter that
# reads them simply skips rows where they are absent.  Sellers leave them blank
# on most listings, so requiring them threw away the bulk of the market: floor
# and direction alone rejected roughly three quarters of everything scanned.
# A missing value renders as "Đang cập nhật", which is honest; a listing the
# crawler never collected cannot be shown at all.
OPTIONAL_DETAIL_FIELDS = (
    "floornumber",
    "direction",
    "furnishing_sell",
    "toilets",
    "property_legal_document",
)

NORMALIZED_REQUIRED_FIELDS = (
    "property_id",
    "source_listing_id",
    "source_api_url",
    "listing_type",
    "price_period",
    "title",
    "description",
    "price",
    "area_sqm",
    "address",
    "ward",
    "district",
    "province",
    "latitude",
    "longitude",
    "bedrooms",
    "apartment_type",
    "seller_account_id",
    "seller_name",
    "published_at",
    "crawled_at",
    "images",
)


class CrawlError(RuntimeError):
    """Raised when a list page cannot be fetched reliably."""


def has_value(value: Any) -> bool:
    """Return whether an API value is present without rejecting numeric zero."""

    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return bool(value)
    return True


def as_clean_string(value: Any) -> str:
    return " ".join(str(value).split()) if has_value(value) else ""


def as_int(value: Any) -> int | None:
    if isinstance(value, bool) or not has_value(value):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not numeric.is_integer():
        return None
    return int(numeric)


def as_float(value: Any) -> float | None:
    if isinstance(value, bool) or not has_value(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def epoch_millis_to_iso(value: Any) -> str:
    milliseconds = as_int(value)
    if milliseconds is None or milliseconds <= 0:
        return ""
    try:
        timestamp = datetime.fromtimestamp(milliseconds / 1000, timezone.utc)
    except (OverflowError, OSError, ValueError):
        return ""
    return timestamp.isoformat().replace("+00:00", "Z")


def api_parameter(ad_params: Any, key: str) -> str:
    if not isinstance(ad_params, dict):
        return ""
    item = ad_params.get(key)
    if not isinstance(item, dict):
        return ""
    return as_clean_string(item.get("value"))


def request_json(
    url: str,
    *,
    timeout_seconds: float,
    retries: int,
    retry_delay_seconds: float,
) -> dict[str, Any]:
    """Fetch JSON with bounded retry/backoff and explicit UTF-8 decoding."""

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = Request(
            url,
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                if response.status != 200:
                    raise CrawlError(f"HTTP {response.status} for {url}")
                payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict):
                    raise CrawlError(f"Unexpected JSON payload for {url}")
                return payload
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {408, 425, 429, 500, 502, 503, 504}:
                break
            retry_after = exc.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                time.sleep(min(float(retry_after), 30.0))
        except (URLError, TimeoutError, json.JSONDecodeError, CrawlError) as exc:
            last_error = exc

        if attempt < retries:
            time.sleep(retry_delay_seconds * (2**attempt))

    raise CrawlError(f"Failed after {retries + 1} attempts: {url}: {last_error}")


def list_prefilter_issues(ad: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for field in LIST_REQUIRED_FIELDS:
        if not has_value(ad.get(field)):
            issues.append(f"missing_{field}")

    if ad.get("state") != "accepted":
        issues.append("state_not_accepted")
    if ad.get("status") != "active":
        issues.append("status_not_active")
    if ad.get("type") not in {"s", "u"}:
        issues.append("unknown_listing_type")

    price = as_int(ad.get("price"))
    if price is None or price <= 0:
        issues.append("invalid_price")

    area = as_float(ad.get("size"))
    if area is None or area <= 0 or area > 10_000:
        issues.append("invalid_area")

    # Sellers mistype sale prices as monthly rents ("3.75" meaning 3.75 tỷ) and
    # occasionally add a few zeroes. One 816 tỷ listing is enough to collapse the
    # price bands the results map draws from the set it is showing.
    if ad.get("type") == "s" and price and area and area > 0:
        if not SALE_PRICE_VND_RANGE[0] <= price <= SALE_PRICE_VND_RANGE[1]:
            issues.append("implausible_sale_price")
        elif not SALE_PRICE_PER_SQM_RANGE[0] <= price / area <= SALE_PRICE_PER_SQM_RANGE[1]:
            issues.append("implausible_sale_price_per_sqm")

    rooms = as_int(ad.get("rooms"))
    if rooms is None or not 1 <= rooms <= 100:
        issues.append("invalid_bedrooms")

    toilets = as_int(ad.get("toilets"))
    if toilets is not None and not 1 <= toilets <= 100:
        issues.append("invalid_bathrooms")

    floor_number = as_int(ad.get("floornumber"))
    if floor_number is not None and not -20 <= floor_number <= 300:
        issues.append("invalid_floor_number")

    latitude = as_float(ad.get("latitude"))
    longitude = as_float(ad.get("longitude"))
    if latitude is None or not -90 <= latitude <= 90:
        issues.append("invalid_latitude")
    if longitude is None or not -180 <= longitude <= 180:
        issues.append("invalid_longitude")

    title = as_clean_string(ad.get("subject"))
    description = as_clean_string(ad.get("body"))
    if not 5 <= len(title) <= 200:
        issues.append("invalid_title_length")
    if len(description) < 30:
        issues.append("description_too_short")

    images = ad.get("images")
    if not isinstance(images, list) or len(images) < MIN_IMAGE_COUNT:
        issues.append("insufficient_images")

    return sorted(set(issues))


def normalize_detail(
    payload: dict[str, Any],
    *,
    crawled_at: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    ad = payload.get("ad")
    if not isinstance(ad, dict):
        return None, ["missing_detail_ad"]

    issues = list_prefilter_issues(ad)
    ad_params = payload.get("ad_params")

    address = api_parameter(ad_params, "address")
    apartment_type = api_parameter(ad_params, "apartment_type")
    legal_status = api_parameter(ad_params, "property_legal_document")
    orientation = api_parameter(ad_params, "direction")
    furniture_status = api_parameter(ad_params, "furnishing_sell")

    for field_name, value in (
        ("address", address),
        ("apartment_type_label", apartment_type),
    ):
        if not value:
            issues.append(f"missing_{field_name}")

    raw_images = ad.get("images") if isinstance(ad.get("images"), list) else []
    images: list[str] = []
    seen_images: set[str] = set()
    for raw_url in raw_images:
        url = as_clean_string(raw_url)
        if not url.startswith("https://") or url in seen_images:
            continue
        seen_images.add(url)
        images.append(url)
    if len(images) < MIN_IMAGE_COUNT:
        issues.append("insufficient_valid_https_images")

    published_at = epoch_millis_to_iso(
        ad.get("orig_list_time") or ad.get("list_time")
    )
    if not published_at:
        issues.append("missing_published_at")

    if issues:
        return None, sorted(set(issues))

    source_listing_id = as_int(ad.get("list_id"))
    listing_type = "SALE" if ad["type"] == "s" else "RENT"
    source_api_url = f"{API_ROOT}/{source_listing_id}"
    price = as_int(ad["price"])
    area_sqm = as_float(ad["size"])

    normalized = {
        "property_id": f"P_{source_listing_id}",
        "source": "NHATOT",
        "source_listing_id": source_listing_id,
        "source_api_url": source_api_url,
        "listing_type": listing_type,
        "price_period": "TOTAL" if listing_type == "SALE" else "MONTH",
        "property_kind": "APARTMENT",
        "title": as_clean_string(ad["subject"]),
        "description": str(ad["body"]).strip(),
        "status": "AVAILABLE",
        "price": price,
        "currency": "VND",
        "area_sqm": area_sqm,
        "address": address,
        "ward": as_clean_string(ad["ward_name"]),
        "district": as_clean_string(ad["area_name"]),
        "province": as_clean_string(ad["region_name"]),
        "latitude": as_float(ad["latitude"]),
        "longitude": as_float(ad["longitude"]),
        "bedrooms": as_int(ad["rooms"]),
        "bathrooms": as_int(ad.get("toilets")),
        "floor_number": as_int(ad.get("floornumber")),
        "orientation": orientation or None,
        "legal_status": legal_status or None,
        "furniture_status": furniture_status or None,
        "balcony_direction": api_parameter(ad_params, "balconydirection") or None,
        "apartment_type": apartment_type,
        "unit_number": api_parameter(ad_params, "unitnumber") or None,
        "project_name": as_clean_string(ad.get("pty_project_name")) or None,
        "deposit": as_int(ad.get("deposit")),
        "seller_account_id": str(ad["account_id"]),
        "seller_name": as_clean_string(ad["account_name"]),
        "seller_is_company": bool(ad.get("company_ad")),
        "seller_rating": as_float(
            ad.get("average_rating_for_seller")
            if ad.get("average_rating_for_seller") is not None
            else ad.get("average_rating")
        ),
        "published_at": published_at,
        "crawled_at": crawled_at,
        "images": images,
    }
    return normalized, []


def normalized_issues(property_data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field in NORMALIZED_REQUIRED_FIELDS:
        if not has_value(property_data.get(field)):
            issues.append(f"missing_{field}")
    if property_data.get("listing_type") not in {"SALE", "RENT"}:
        issues.append("invalid_listing_type")
    if property_data.get("price_period") not in {"TOTAL", "MONTH"}:
        issues.append("invalid_price_period")
    if as_int(property_data.get("price")) is None or property_data["price"] <= 0:
        issues.append("invalid_price")
    if as_float(property_data.get("area_sqm")) is None or property_data["area_sqm"] <= 0:
        issues.append("invalid_area")
    images = property_data.get("images")
    if not isinstance(images, list) or len(images) < MIN_IMAGE_COUNT:
        issues.append("insufficient_images")
    return sorted(set(issues))


def normalized_text_fingerprint(value: Any) -> str:
    text = as_clean_string(value).casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def semantic_keys(property_data: dict[str, Any]) -> tuple[str, ...]:
    """Build conservative keys for obvious reposts of the same property."""

    title = normalized_text_fingerprint(property_data.get("title"))
    description = normalized_text_fingerprint(property_data.get("description"))
    seller_id = str(property_data.get("seller_account_id", ""))
    digest = hashlib.sha256(f"{title}|{description}".encode("utf-8")).hexdigest()
    seller_description_digest = hashlib.sha256(
        f"{seller_id}|{description}".encode("utf-8")
    ).hexdigest()
    seller_location_specs = "|".join(
        (
            seller_id,
            f"{float(property_data['latitude']):.5f}",
            f"{float(property_data['longitude']):.5f}",
            str(property_data["price"]),
            f"{float(property_data['area_sqm']):.2f}",
            str(property_data["bedrooms"]),
            str(property_data["bathrooms"]),
        )
    )
    return (
        f"title_description:{digest}",
        f"seller_description:{seller_description_digest}",
        f"seller_location_specs:{seller_location_specs}",
    )


def deduplicate_properties(
    properties: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Keep the newest record when conservative semantic keys collide."""

    newest_first = sorted(
        properties,
        key=lambda item: item["published_at"],
        reverse=True,
    )
    seen_keys: set[str] = set()
    unique: list[dict[str, Any]] = []
    removed_codes: list[str] = []
    for item in newest_first:
        keys = semantic_keys(item)
        if any(key in seen_keys for key in keys):
            removed_codes.append(item["property_id"])
            continue
        seen_keys.update(keys)
        unique.append(item)
    return unique, removed_codes


def atomic_write_json(path: Path, data: Any) -> None:
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
        json.dump(data, temporary_file, ensure_ascii=False, indent=2)
        temporary_file.write("\n")
    os.replace(temporary_path, path)


def crawl_complete_properties(
    *,
    target: int,
    max_pages: int,
    batch_size: int,
    region_id: int,
    category_id: int,
    listing_type: str,
    timeout_seconds: float,
    retries: int,
    request_delay_seconds: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    properties: list[dict[str, Any]] = []
    seen_listing_ids: set[int] = set()
    rejection_reasons: Counter[str] = Counter()
    scanned = 0
    detail_requests = 0
    duplicate_listings = 0
    total_available: int | None = None
    crawled_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    for page_index in range(max_pages):
        offset = page_index * batch_size
        query_parameters: dict[str, Any] = {
            "cg": category_id,
            "limit": batch_size,
            "o": offset,
        }
        # Region 0 means nationwide: the API returns every province when
        # region_v2 is absent, so a whole-country crawl needs no province loop.
        if region_id:
            query_parameters["region_v2"] = region_id
        if listing_type != "ALL":
            query_parameters["st"] = "s" if listing_type == "SALE" else "u"
        query = urlencode(query_parameters)
        page_url = f"{API_ROOT}?{query}"
        page = request_json(
            page_url,
            timeout_seconds=timeout_seconds,
            retries=retries,
            retry_delay_seconds=max(request_delay_seconds, 0.25),
        )
        ads = page.get("ads")
        if not isinstance(ads, list):
            raise CrawlError(f"Page at offset {offset} has no ads list")
        if total_available is None:
            total_available = as_int(page.get("total"))
        if not ads:
            break

        for ad in ads:
            scanned += 1
            if not isinstance(ad, dict):
                rejection_reasons["invalid_list_item"] += 1
                continue

            listing_id = as_int(ad.get("list_id"))
            if listing_id is None:
                rejection_reasons["missing_list_id"] += 1
                continue
            if listing_id in seen_listing_ids:
                duplicate_listings += 1
                continue
            seen_listing_ids.add(listing_id)

            prefilter_issues = list_prefilter_issues(ad)
            if prefilter_issues:
                rejection_reasons.update(prefilter_issues)
                continue

            if request_delay_seconds:
                time.sleep(request_delay_seconds)
            detail_requests += 1
            try:
                detail = request_json(
                    f"{API_ROOT}/{listing_id}",
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                    retry_delay_seconds=max(request_delay_seconds, 0.25),
                )
            except CrawlError:
                rejection_reasons["detail_fetch_failed"] += 1
                continue

            normalized, detail_issues = normalize_detail(
                detail,
                crawled_at=crawled_at,
            )
            if detail_issues or normalized is None:
                rejection_reasons.update(detail_issues)
                continue

            final_issues = normalized_issues(normalized)
            if final_issues:
                rejection_reasons.update(final_issues)
                continue

            properties.append(normalized)
            properties, semantic_duplicates = deduplicate_properties(properties)
            if semantic_duplicates:
                rejection_reasons["semantic_duplicate"] += len(semantic_duplicates)
                continue
            print(
                f"Accepted {len(properties)}/{target}: "
                f"{normalized['property_id']} - {normalized['title'][:70]}"
            )
            if target > 0 and len(properties) >= target:
                break

        print(
            f"Page {page_index + 1}: scanned={scanned}, "
            f"detail={detail_requests}, accepted={len(properties)}"
        )
        if target > 0 and len(properties) >= target:
            break
        if total_available is not None and offset + len(ads) >= total_available:
            break
        if request_delay_seconds:
            time.sleep(request_delay_seconds)

    report = {
        "source": "NHATOT",
        "source_api": API_ROOT,
        "crawled_at": crawled_at,
        "region_id": region_id,
        "category_id": category_id,
        "listing_type_filter": listing_type,
        "target_complete_records": target,
        "total_available_reported_by_api": total_available,
        "listings_scanned": scanned,
        "detail_requests": detail_requests,
        "complete_records": len(properties),
        "duplicates_skipped": duplicate_listings,
        "minimum_image_count": MIN_IMAGE_COUNT,
        "strict_required_fields": list(NORMALIZED_REQUIRED_FIELDS),
        "rejection_reason_counts": dict(rejection_reasons.most_common()),
    }
    return properties, report


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Crawl only complete Hanoi apartment listings from Nha Tot."
    )
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument(
        "--region-id",
        type=int,
        default=DEFAULT_REGION_ID,
        help="Chotot region_v2 id; 0 crawls every province.",
    )
    parser.add_argument("--category-id", type=int, default=DEFAULT_CATEGORY_ID)
    parser.add_argument(
        "--listing-type",
        choices=("SALE", "RENT", "ALL"),
        default=DEFAULT_LISTING_TYPE,
        help="SALE is the safe default for the current list_price schema.",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument(
        "--output",
        type=Path,
        default=base_dir / "properties.json",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=base_dir / "crawl_report.json",
    )
    args = parser.parse_args()
    if args.target < 0:
        parser.error("--target must be >= 0; use 0 to scan every available page")
    if args.region_id < 0:
        parser.error("--region-id must be >= 0; use 0 for every province")
    if args.max_pages <= 0 or not 1 <= args.batch_size <= 50:
        parser.error("--max-pages must be > 0 and --batch-size must be 1..50")
    if args.timeout <= 0 or args.retries < 0 or args.delay < 0:
        parser.error("timeout/delay must be non-negative and retries must be >= 0")
    return args


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    properties, report = crawl_complete_properties(
        target=args.target,
        max_pages=args.max_pages,
        batch_size=args.batch_size,
        region_id=args.region_id,
        category_id=args.category_id,
        listing_type=args.listing_type,
        timeout_seconds=args.timeout,
        retries=args.retries,
        request_delay_seconds=args.delay,
    )
    if not properties:
        raise CrawlError("No complete listing passed the strict quality gate")

    output_path = args.output.resolve()
    report_path = args.report.resolve()
    atomic_write_json(output_path, properties)
    areas = [float(item["area_sqm"]) for item in properties]
    prices = [int(item["price"]) for item in properties]
    report["run_status"] = (
        "COMPLETE"
        if args.target == 0 or len(properties) >= args.target
        else "SOURCE_EXHAUSTED_BEFORE_TARGET"
    )
    report["total_images"] = sum(len(item["images"]) for item in properties)
    report["area_sqm"] = {
        "min": min(areas),
        "median": statistics.median(areas),
        "max": max(areas),
    }
    report["price_vnd"] = {
        "min": min(prices),
        "median": statistics.median(prices),
        "max": max(prices),
    }
    report["normalized_output_sha256"] = hashlib.sha256(
        output_path.read_bytes()
    ).hexdigest()
    atomic_write_json(report_path, report)
    print(
        f"Saved {len(properties)} complete listings to {output_path} "
        f"and audit report to {report_path}"
    )


if __name__ == "__main__":
    main()
