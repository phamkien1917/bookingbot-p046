"""Generate deterministic PostgreSQL seed SQL from normalized crawl data."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


PROPERTY_NAMESPACE = uuid.UUID("6bf8c137-62d3-47b0-82d9-1d77cb62e8cc")
MEDIA_NAMESPACE = uuid.UUID("d42d0bb4-f3e7-4b82-8480-1e97ac225c5e")
MIN_IMAGE_COUNT = 3

REQUIRED_FIELDS = (
    "property_id",
    "source",
    "source_listing_id",
    "source_api_url",
    "listing_type",
    "price_period",
    "property_kind",
    "title",
    "description",
    "status",
    "price",
    "currency",
    "area_sqm",
    "address",
    "ward",
    "district",
    "province",
    "latitude",
    "longitude",
    "bedrooms",
    "bathrooms",
    "floor_number",
    "orientation",
    "legal_status",
    "furniture_status",
    "apartment_type",
    "seller_account_id",
    "seller_name",
    "published_at",
    "crawled_at",
    "images",
)


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return bool(value)
    return True


def sql_string(value: Any) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def sql_number(value: Any, *, decimals: int | None = None) -> str:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value: {value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"Non-finite numeric value: {value!r}")
    if decimals is not None:
        quantum = Decimal(1).scaleb(-decimals)
        number = number.quantize(quantum)
    return format(number, "f")


def parse_iso_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Timestamp must be a non-empty ISO-8601 string")
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO-8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp must contain a timezone: {value!r}")
    return value.strip()


def property_issues(item: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field in REQUIRED_FIELDS:
        if not has_value(item.get(field)):
            issues.append(f"missing_{field}")

    if item.get("listing_type") not in {"SALE", "RENT"}:
        issues.append("invalid_listing_type")
    if item.get("price_period") not in {"TOTAL", "MONTH"}:
        issues.append("invalid_price_period")
    if item.get("property_kind") != "APARTMENT":
        issues.append("invalid_property_kind")
    if item.get("status") != "AVAILABLE":
        issues.append("invalid_status")
    if item.get("currency") != "VND":
        issues.append("invalid_currency")

    for field, max_length in (
        ("property_id", 50),
        ("title", 200),
        ("ward", 100),
        ("district", 100),
        ("province", 100),
        ("orientation", 32),
        ("legal_status", 150),
    ):
        value = item.get(field)
        if isinstance(value, str) and len(value) > max_length:
            issues.append(f"{field}_too_long")

    numeric_rules = (
        ("price", 0, 999_999_999_999_999_999),
        ("area_sqm", 0, 9_999_999_999.99),
        ("latitude", -90, 90),
        ("longitude", -180, 180),
        ("bedrooms", 1, 32_767),
        ("bathrooms", 1, 32_767),
        ("floor_number", -32_768, 32_767),
    )
    for field, lower, upper in numeric_rules:
        try:
            value = float(item.get(field))
        except (TypeError, ValueError):
            issues.append(f"invalid_{field}")
            continue
        if not math.isfinite(value) or not lower <= value <= upper:
            issues.append(f"invalid_{field}")
        if field in {"price", "area_sqm"} and value <= 0:
            issues.append(f"invalid_{field}")
        if field in {"bedrooms", "bathrooms", "floor_number"} and not value.is_integer():
            issues.append(f"invalid_{field}")

    images = item.get("images")
    if not isinstance(images, list) or len(images) < MIN_IMAGE_COUNT:
        issues.append("insufficient_images")
    elif len(images) != len(set(images)):
        issues.append("duplicate_images")
    elif any(not isinstance(url, str) or not url.startswith("https://") for url in images):
        issues.append("invalid_image_url")

    for timestamp_field in ("published_at", "crawled_at"):
        try:
            parse_iso_timestamp(item.get(timestamp_field))
        except ValueError:
            issues.append(f"invalid_{timestamp_field}")

    return sorted(set(issues))


def property_features(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": item["source"],
        "source_listing_id": item["source_listing_id"],
        "source_api_url": item["source_api_url"],
        "listing_type": item["listing_type"],
        "price_period": item["price_period"],
        "apartment_type": item["apartment_type"],
        "furniture_status": item["furniture_status"],
        "balcony_direction": item.get("balcony_direction"),
        "unit_number": item.get("unit_number"),
        "project_name": item.get("project_name"),
        "deposit": item.get("deposit"),
        "seller": {
            "source_account_id": item["seller_account_id"],
            "display_name": item["seller_name"],
            "is_company": bool(item.get("seller_is_company")),
            "rating": item.get("seller_rating"),
        },
        "crawled_at": item["crawled_at"],
    }


def deterministic_property_uuid(item: dict[str, Any]) -> uuid.UUID:
    return uuid.uuid5(
        PROPERTY_NAMESPACE,
        f"{item['source']}:{item['source_listing_id']}",
    )


def deterministic_media_uuid(item: dict[str, Any], image_url: str) -> uuid.UUID:
    return uuid.uuid5(
        MEDIA_NAMESPACE,
        f"{item['source']}:{item['source_listing_id']}:{image_url}",
    )


def property_upsert(item: dict[str, Any]) -> str:
    property_id = deterministic_property_uuid(item)
    features_json = json.dumps(
        property_features(item),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    columns = (
        "id, code, property_kind, title, description, status, address_line, "
        "ward, district, province, latitude, longitude, area_sqm, bedrooms, "
        "bathrooms, floor_number, orientation, legal_status, list_price, "
        "currency, features, published_at"
    )
    values = (
        f"'{property_id}', "
        f"{sql_string(item['property_id'])}, "
        f"{sql_string(item['property_kind'])}, "
        f"{sql_string(item['title'])}, "
        f"{sql_string(item['description'])}, "
        f"{sql_string(item['status'])}, "
        f"{sql_string(item['address'])}, "
        f"{sql_string(item['ward'])}, "
        f"{sql_string(item['district'])}, "
        f"{sql_string(item['province'])}, "
        f"{sql_number(item['latitude'], decimals=6)}, "
        f"{sql_number(item['longitude'], decimals=6)}, "
        f"{sql_number(item['area_sqm'], decimals=2)}, "
        f"{int(item['bedrooms'])}, {int(item['bathrooms'])}, "
        f"{int(item['floor_number'])}, "
        f"{sql_string(item['orientation'])}, "
        f"{sql_string(item['legal_status'])}, "
        f"{sql_number(item['price'], decimals=2)}, "
        f"{sql_string(item['currency'])}, "
        f"{sql_string(features_json)}::jsonb, "
        f"{sql_string(item['published_at'])}::timestamptz"
    )
    updates = (
        "property_kind = EXCLUDED.property_kind, "
        "title = EXCLUDED.title, "
        "description = EXCLUDED.description, "
        "status = EXCLUDED.status, "
        "address_line = EXCLUDED.address_line, "
        "ward = EXCLUDED.ward, "
        "district = EXCLUDED.district, "
        "province = EXCLUDED.province, "
        "latitude = EXCLUDED.latitude, "
        "longitude = EXCLUDED.longitude, "
        "area_sqm = EXCLUDED.area_sqm, "
        "bedrooms = EXCLUDED.bedrooms, "
        "bathrooms = EXCLUDED.bathrooms, "
        "floor_number = EXCLUDED.floor_number, "
        "orientation = EXCLUDED.orientation, "
        "legal_status = EXCLUDED.legal_status, "
        "list_price = EXCLUDED.list_price, "
        "currency = EXCLUDED.currency, "
        "features = EXCLUDED.features, "
        "published_at = EXCLUDED.published_at, "
        "updated_at = now()"
    )
    return (
        f"INSERT INTO properties ({columns}) VALUES ({values}) "
        f"ON CONFLICT (code) DO UPDATE SET {updates};"
    )


def media_upsert(item: dict[str, Any], image_url: str, order: int) -> str:
    media_id = deterministic_media_uuid(item, image_url)
    property_code = sql_string(item["property_id"])
    return (
        "INSERT INTO property_media "
        "(id, property_id, media_type, url, sort_order, is_cover) VALUES "
        f"('{media_id}', "
        f"(SELECT id FROM properties WHERE code = {property_code}), "
        f"'IMAGE', {sql_string(image_url)}, {order}, "
        f"{'TRUE' if order == 0 else 'FALSE'}) "
        "ON CONFLICT (id) DO UPDATE SET "
        "property_id = EXCLUDED.property_id, "
        "media_type = EXCLUDED.media_type, "
        "url = EXCLUDED.url, "
        "sort_order = EXCLUDED.sort_order, "
        "is_cover = EXCLUDED.is_cover;"
    )


def generate_sql(properties: list[dict[str, Any]]) -> str:
    if not properties:
        raise ValueError("Input contains no properties")

    seen_codes: set[str] = set()
    validation_errors: list[str] = []
    for index, item in enumerate(properties):
        if not isinstance(item, dict):
            validation_errors.append(f"record[{index}] is not an object")
            continue
        issues = property_issues(item)
        if issues:
            validation_errors.append(
                f"record[{index}] {item.get('property_id', '<unknown>')}: "
                + ", ".join(issues)
            )
        code = item.get("property_id")
        if code in seen_codes:
            validation_errors.append(f"record[{index}] duplicate code: {code}")
        elif isinstance(code, str):
            seen_codes.add(code)

    if validation_errors:
        preview = "\n".join(validation_errors[:20])
        remainder = len(validation_errors) - 20
        if remainder > 0:
            preview += f"\n... and {remainder} more validation errors"
        raise ValueError(f"Crawl data failed strict validation:\n{preview}")

    lines = [
        "-- Complete Nha Tot property data generated by generate_sql_from_json.py.",
        "-- External seller metadata is provenance only; no fake users or schedules are created.",
        "BEGIN;",
        "SET LOCAL client_encoding = 'UTF8';",
        "",
    ]

    for item in properties:
        lines.append(property_upsert(item))
        # Avoid the partial unique cover index blocking a changed source cover.
        lines.append(
            "UPDATE property_media SET is_cover = FALSE "
            "WHERE property_id = "
            f"(SELECT id FROM properties WHERE code = {sql_string(item['property_id'])}) "
            "AND is_cover = TRUE;"
        )
        for order, image_url in enumerate(item["images"]):
            lines.append(media_upsert(item, image_url, order))
        lines.append("")

    lines.extend(["COMMIT;", ""])
    return "\n".join(lines)


def atomic_write_text(path: Path, text: str) -> None:
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
        temporary_file.write(text)
    os.replace(temporary_path, path)


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate strict, deterministic property SQL from crawl JSON."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=base_dir / "properties.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=base_dir / "004_crawled_data.sql",
    )
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    with args.input.resolve().open("r", encoding="utf-8") as input_file:
        properties = json.load(input_file)
    if not isinstance(properties, list):
        raise ValueError("Input JSON must be a list of normalized properties")

    sql = generate_sql(properties)
    atomic_write_text(args.output.resolve(), sql)
    media_count = sum(len(item["images"]) for item in properties)
    print(
        f"Generated {args.output.resolve()} with "
        f"{len(properties)} properties and {media_count} media rows"
    )


if __name__ == "__main__":
    main()
