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
EXTERNAL_SELLER_NAMESPACE = uuid.UUID("cd491257-c249-4f2e-92cc-a5a55c4fe773")
DEMO_SALE_USER_IDS = (
    "10000000-0000-0000-0000-000000000002",
    "10000000-0000-0000-0000-000000000008",
    "10000000-0000-0000-0000-000000000009",
)
SOURCE_MEDIA_CAPTION = "Nguồn: Nhà Tốt"
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


def sql_int(value: Any) -> str:
    return "NULL" if value is None else str(int(value))


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
        ("source", 40),
        ("seller_account_id", 100),
        ("seller_name", 200),
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
        if field == "bedrooms" and not value.is_integer():
            issues.append(f"invalid_{field}")

    # Sellers routinely leave these blank. A present value is still checked; an
    # absent one becomes NULL rather than throwing the whole listing away.
    for field, lower, upper in (
        ("bathrooms", 1, 32_767),
        ("floor_number", -32_768, 32_767),
    ):
        value = item.get(field)
        if value is None:
            continue
        if not isinstance(value, int) or isinstance(value, bool):
            issues.append(f"invalid_{field}")
        elif not lower <= value <= upper:
            issues.append(f"invalid_{field}")

    images = item.get("images")
    if not isinstance(images, list) or len(images) < MIN_IMAGE_COUNT:
        issues.append("insufficient_images")
    elif len(images) != len(set(images)):
        issues.append("duplicate_images")
    elif any(not isinstance(url, str) or not url.startswith("https://") for url in images):
        issues.append("invalid_image_url")

    seller_rating = item.get("seller_rating")
    if seller_rating is not None:
        try:
            parsed_rating = float(seller_rating)
        except (TypeError, ValueError):
            issues.append("invalid_seller_rating")
        else:
            if not math.isfinite(parsed_rating) or not 0 <= parsed_rating <= 5:
                issues.append("invalid_seller_rating")

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
        "furniture_status": item.get("furniture_status"),
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


def deterministic_external_seller_uuid(item: dict[str, Any]) -> uuid.UUID:
    return uuid.uuid5(
        EXTERNAL_SELLER_NAMESPACE,
        f"{item['source']}:{item['seller_account_id']}",
    )


def assigned_demo_sale_user_id(item: dict[str, Any]) -> str:
    digest = uuid.uuid5(
        PROPERTY_NAMESPACE,
        f"demo-sale:{item['source']}:{item['source_listing_id']}",
    )
    return DEMO_SALE_USER_IDS[digest.int % len(DEMO_SALE_USER_IDS)]


def external_seller_upsert(item: dict[str, Any]) -> str:
    seller_id = deterministic_external_seller_uuid(item)
    source = str(item["source"])
    seller_key = str(item["seller_account_id"])
    seller_type = "COMPANY" if item.get("seller_is_company") else "UNKNOWN"
    raw_data = json.dumps(
        {
            "source_rating": item.get("seller_rating"),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    seen_at = parse_iso_timestamp(item["crawled_at"])
    rating = (
        "NULL"
        if item.get("seller_rating") is None
        else sql_number(item["seller_rating"], decimals=2)
    )
    return (
        "INSERT INTO external_sellers "
        "(id, source, source_seller_key, source_account_id, display_name, "
        "seller_type, is_company, rating, raw_data, first_seen_at, last_seen_at) VALUES "
        f"({sql_string(seller_id)}, {sql_string(source)}, {sql_string(seller_key)}, "
        f"{sql_string(seller_key)}, {sql_string(item['seller_name'])}, "
        f"{sql_string(seller_type)}, {'TRUE' if item.get('seller_is_company') else 'FALSE'}, "
        f"{rating}, {sql_string(raw_data)}::jsonb, "
        f"{sql_string(seen_at)}::timestamptz, {sql_string(seen_at)}::timestamptz) "
        "ON CONFLICT (source, source_seller_key) DO UPDATE SET "
        "source_account_id = COALESCE(EXCLUDED.source_account_id, external_sellers.source_account_id), "
        "display_name = EXCLUDED.display_name, "
        "seller_type = CASE WHEN EXCLUDED.seller_type = 'UNKNOWN' "
        "THEN external_sellers.seller_type ELSE EXCLUDED.seller_type END, "
        "is_company = EXCLUDED.is_company, "
        "rating = COALESCE(EXCLUDED.rating, external_sellers.rating), "
        "raw_data = external_sellers.raw_data || EXCLUDED.raw_data, "
        "first_seen_at = LEAST(external_sellers.first_seen_at, EXCLUDED.first_seen_at), "
        "last_seen_at = GREATEST(external_sellers.last_seen_at, EXCLUDED.last_seen_at), "
        "updated_at = now();"
    )


def property_external_seller_upsert(item: dict[str, Any]) -> list[str]:
    property_code = sql_string(item["property_id"])
    seen_at = parse_iso_timestamp(item["crawled_at"])
    metadata = json.dumps(
        {"source_api_url": item.get("source_api_url")},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    property_id_sql = (
        f"(SELECT id FROM properties WHERE code = {property_code})"
    )
    seller_id_sql = (
        "(SELECT id FROM external_sellers WHERE "
        f"source = {sql_string(item['source'])} AND "
        f"source_seller_key = {sql_string(str(item['seller_account_id']))})"
    )
    return [
        "UPDATE property_external_sellers SET is_primary = FALSE, updated_at = now() "
        f"WHERE property_id = {property_id_sql} "
        f"AND external_seller_id <> {seller_id_sql} AND is_primary = TRUE;",
        "INSERT INTO property_external_sellers "
        "(property_id, external_seller_id, relationship_type, is_primary, "
        "source_listing_id, source_url, first_seen_at, last_seen_at, metadata) VALUES "
        f"({property_id_sql}, {seller_id_sql}, 'LISTING_POSTER', TRUE, "
        f"{sql_string(item['source_listing_id'])}, "
        f"{sql_string(item['source_api_url'])}, "
        f"{sql_string(seen_at)}::timestamptz, {sql_string(seen_at)}::timestamptz, "
        f"{sql_string(metadata)}::jsonb) "
        "ON CONFLICT (property_id, external_seller_id) DO UPDATE SET "
        "relationship_type = EXCLUDED.relationship_type, is_primary = TRUE, "
        "source_listing_id = EXCLUDED.source_listing_id, "
        "source_url = EXCLUDED.source_url, "
        "first_seen_at = LEAST(property_external_sellers.first_seen_at, EXCLUDED.first_seen_at), "
        "last_seen_at = GREATEST(property_external_sellers.last_seen_at, EXCLUDED.last_seen_at), "
        "metadata = property_external_sellers.metadata || EXCLUDED.metadata, "
        "updated_at = now();",
    ]


def demo_sale_assignment_insert(item: dict[str, Any]) -> str:
    property_code = sql_string(item["property_id"])
    property_id_sql = (
        f"(SELECT id FROM properties WHERE code = {property_code})"
    )
    sale_user_id = sql_string(assigned_demo_sale_user_id(item))
    assigned_at = sql_string(parse_iso_timestamp(item["crawled_at"]))
    return (
        "INSERT INTO property_sale_assignments "
        "(property_id, sale_user_id, is_primary, assigned_at) "
        f"SELECT {property_id_sql}, {sale_user_id}, TRUE, {assigned_at}::timestamptz "
        "WHERE NOT EXISTS (SELECT 1 FROM property_sale_assignments current_assignment "
        f"WHERE current_assignment.property_id = {property_id_sql} "
        "AND current_assignment.is_primary = TRUE AND current_assignment.unassigned_at IS NULL) "
        "ON CONFLICT (property_id, sale_user_id) DO NOTHING;"
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
        "currency, features, published_at, last_verified_at"
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
        f"{int(item['bedrooms'])}, "
        f"{sql_int(item.get('bathrooms'))}, "
        f"{sql_int(item.get('floor_number'))}, "
        f"{sql_string(item.get('orientation'))}, "
        f"{sql_string(item.get('legal_status'))}, "
        f"{sql_number(item['price'], decimals=2)}, "
        f"{sql_string(item['currency'])}, "
        f"{sql_string(features_json)}::jsonb, "
        f"{sql_string(item['published_at'])}::timestamptz, "
        # Fetching the detail endpoint and finding the ad still active is itself
        # a check that the listing is live, so the crawl time is the last
        # verification we can honestly claim.
        f"{sql_string(item['crawled_at'])}::timestamptz"
    )
    updates = (
        "property_kind = EXCLUDED.property_kind, "
        "title = EXCLUDED.title, "
        "description = EXCLUDED.description, "
        "status = CASE WHEN properties.status IN ('DRAFT', 'AVAILABLE') "
        "THEN EXCLUDED.status ELSE properties.status END, "
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
        # GREATEST ignores NULLs, so a sale who verified after this crawl keeps
        # their newer mark and a never-verified row still gets one.
        "last_verified_at = GREATEST("
        "properties.last_verified_at, EXCLUDED.last_verified_at), "
        "updated_at = now()"
    )
    return (
        f"INSERT INTO properties ({columns}) VALUES ({values}) "
        f"ON CONFLICT (code) DO UPDATE SET {updates};"
    )


def media_upsert(item: dict[str, Any], image_url: str, order: int) -> str:
    media_id = deterministic_media_uuid(item, image_url)
    property_code = sql_string(item["property_id"])
    property_id_sql = (
        f"(SELECT id FROM properties WHERE code = {property_code})"
    )
    cover_sql = "FALSE"
    if order == 0:
        cover_sql = (
            "NOT EXISTS (SELECT 1 FROM property_media existing_media "
            f"WHERE existing_media.property_id = {property_id_sql} "
            "AND existing_media.is_cover)"
        )
    return (
        "INSERT INTO property_media "
        "(id, property_id, media_type, url, source, caption, sort_order, is_cover) VALUES "
        f"('{media_id}', "
        f"{property_id_sql}, "
        f"'IMAGE', {sql_string(image_url)}, {sql_string(item['source'])}, "
        f"{sql_string(SOURCE_MEDIA_CAPTION)}, {order}, {cover_sql}) "
        "ON CONFLICT (id) DO UPDATE SET "
        "property_id = EXCLUDED.property_id, "
        "media_type = EXCLUDED.media_type, "
        "url = EXCLUDED.url, "
        "source = EXCLUDED.source, "
        "caption = EXCLUDED.caption, "
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
        "-- External posters are normalized separately from internal login users and sales.",
        "-- New properties receive one deterministic demo sale assignment if none exists.",
        "BEGIN;",
        "SET LOCAL client_encoding = 'UTF8';",
        "",
    ]

    for item in properties:
        lines.append(property_upsert(item))
        lines.append(external_seller_upsert(item))
        lines.extend(property_external_seller_upsert(item))
        lines.append(demo_sale_assignment_insert(item))
        # Reconcile only media imported from this source; preserve internal media.
        lines.append(
            "DELETE FROM property_media WHERE property_id = "
            f"(SELECT id FROM properties WHERE code = {sql_string(item['property_id'])}) "
            f"AND source = {sql_string(item['source'])};"
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
    seller_count = len(
        {
            (str(item["source"]), str(item["seller_account_id"]))
            for item in properties
        }
    )
    print(
        f"Generated {args.output.resolve()} with "
        f"{len(properties)} properties, {seller_count} external sellers, "
        f"{len(properties)} seller links and {media_count} media rows"
    )


if __name__ == "__main__":
    main()
