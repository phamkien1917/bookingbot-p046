"""Tests for the Nha Tot crawl pipeline: prefilter, SQL generation and merging.

The crawl scripts live in database/ rather than src/, so they are loaded by path.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

DATABASE_DIR = Path(__file__).resolve().parents[1] / "database"


def load_script(name: str) -> ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, DATABASE_DIR / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


crawler = load_script("crawler_chotot")
generator = load_script("generate_sql_from_json")
merger = load_script("merge_crawls")


def complete_ad() -> dict:
    """A listing that passes every gate, used as the baseline to mutate."""

    return {
        "list_id": 134000001,
        "subject": "Bán căn hộ 2PN toà A, ban công Đông Nam",
        "body": "Căn hộ 2 phòng ngủ, nội thất cơ bản, sổ hồng riêng, bàn giao ngay." * 2,
        "type": "s",
        "state": "accepted",
        "status": "active",
        "price": 3_200_000_000,
        "size": 68,
        "street_name": "Nguyễn Trãi",
        "ward_name": "Phường Thanh Xuân Trung",
        "area_name": "Quận Thanh Xuân",
        "region_name": "Hà Nội",
        "latitude": 21.0002,
        "longitude": 105.8002,
        "rooms": 2,
        "toilets": 2,
        "floornumber": 12,
        "direction": "Đông Nam",
        "property_legal_document": "Sổ hồng riêng",
        "furnishing_sell": "Nội thất cơ bản",
        "apartment_type": "Chung cư",
        "account_id": 9001,
        "account_name": "Nguyễn Văn A",
        "images": [
            "https://cdn.chotot.com/a.jpg",
            "https://cdn.chotot.com/b.jpg",
            "https://cdn.chotot.com/c.jpg",
        ],
    }


def complete_property() -> dict:
    """A normalized record that generate_sql_from_json accepts."""

    return {
        "property_id": "P_134000001",
        "source": "NHATOT",
        "source_listing_id": 134000001,
        "source_api_url": "https://gateway.chotot.com/v1/public/ad-listing/134000001",
        "listing_type": "SALE",
        "price_period": "TOTAL",
        "property_kind": "APARTMENT",
        "title": "Bán căn hộ 2PN toà A",
        "description": "Căn hộ 2 phòng ngủ, nội thất cơ bản, sổ hồng riêng." * 2,
        "status": "AVAILABLE",
        "price": 3_200_000_000,
        "currency": "VND",
        "area_sqm": 68.0,
        "address": "Số 1 Nguyễn Trãi, Phường Thanh Xuân Trung, Quận Thanh Xuân, Hà Nội",
        "ward": "Phường Thanh Xuân Trung",
        "district": "Quận Thanh Xuân",
        "province": "Hà Nội",
        "latitude": 21.0002,
        "longitude": 105.8002,
        "bedrooms": 2,
        "bathrooms": 2,
        "floor_number": 12,
        "orientation": "Đông Nam",
        "legal_status": "Sổ hồng riêng",
        "furniture_status": "Nội thất cơ bản",
        "apartment_type": "Chung cư",
        "balcony_direction": None,
        "unit_number": None,
        "project_name": None,
        "deposit": None,
        "seller_account_id": "9001",
        "seller_name": "Nguyễn Văn A",
        "seller_is_company": False,
        "seller_rating": None,
        "published_at": "2026-08-30T10:00:00Z",
        "crawled_at": "2026-08-31T06:00:00Z",
        "images": [
            "https://cdn.chotot.com/a.jpg",
            "https://cdn.chotot.com/b.jpg",
            "https://cdn.chotot.com/c.jpg",
        ],
    }


# ── Prefilter: what a missing field costs ────────────────────────────────────


def test_complete_listing_passes_prefilter():
    assert crawler.list_prefilter_issues(complete_ad()) == []


@pytest.mark.parametrize("field", crawler.OPTIONAL_DETAIL_FIELDS)
def test_optional_display_fields_do_not_reject_a_listing(field):
    """Floor, direction, furnishing, toilets and legal doc are nullable columns.

    Requiring them rejected roughly three quarters of the market for fields no
    search filter reads, so their absence must not cost the listing.
    """
    ad = complete_ad()
    del ad[field]
    assert crawler.list_prefilter_issues(ad) == []


@pytest.mark.parametrize(
    "field",
    ["price", "size", "rooms", "latitude", "longitude", "ward_name", "apartment_type"],
)
def test_fields_search_depends_on_are_still_required(field):
    ad = complete_ad()
    del ad[field]
    assert f"missing_{field}" in crawler.list_prefilter_issues(ad)


def test_a_present_but_absurd_floor_is_still_rejected():
    ad = complete_ad()
    ad["floornumber"] = 5000
    assert "invalid_floor_number" in crawler.list_prefilter_issues(ad)


def test_a_present_but_absurd_bathroom_count_is_still_rejected():
    ad = complete_ad()
    ad["toilets"] = 0
    assert "invalid_bathrooms" in crawler.list_prefilter_issues(ad)


def test_listing_below_the_image_floor_is_rejected():
    ad = complete_ad()
    ad["images"] = ad["images"][:2]
    assert "insufficient_images" in crawler.list_prefilter_issues(ad)


@pytest.mark.parametrize(
    ("price", "size", "reason"),
    [
        (3_750_000, 69, "implausible_sale_price"),
        (816_900_000_000, 97, "implausible_sale_price"),
        (130_000_000, 54, "implausible_sale_price_per_sqm"),
    ],
)
def test_mistyped_sale_prices_are_rejected(price, size, reason):
    """One 816 tỷ listing collapses the price bands the results map draws."""
    ad = complete_ad()
    ad["price"] = price
    ad["size"] = size
    assert reason in crawler.list_prefilter_issues(ad)


@pytest.mark.parametrize(("price", "size"), [(1_200_000_000, 45), (60_000_000_000, 300)])
def test_plausible_sale_prices_are_kept(price, size):
    ad = complete_ad()
    ad["price"] = price
    ad["size"] = size
    assert crawler.list_prefilter_issues(ad) == []


def test_rent_listings_skip_the_sale_price_band():
    """A 12 triệu/month rent is not a mistyped sale price."""
    ad = complete_ad()
    ad["type"] = "u"
    ad["price"] = 12_000_000
    assert "implausible_sale_price" not in crawler.list_prefilter_issues(ad)


def test_inactive_listing_is_rejected():
    ad = complete_ad()
    ad["status"] = "rejected"
    assert "status_not_active" in crawler.list_prefilter_issues(ad)


# ── SQL generation ───────────────────────────────────────────────────────────


def test_complete_property_generates_no_issues():
    assert generator.property_issues(complete_property()) == []


@pytest.mark.parametrize(
    "field", ["bathrooms", "floor_number", "orientation", "legal_status", "furniture_status"]
)
def test_generator_accepts_a_missing_nullable_field(field):
    item = complete_property()
    item[field] = None
    assert generator.property_issues(item) == []


def test_missing_nullable_fields_become_sql_null_not_empty_strings():
    item = complete_property()
    item["bathrooms"] = None
    item["floor_number"] = None
    item["orientation"] = None
    item["legal_status"] = None
    statement = generator.property_upsert(item)
    assert ", NULL, NULL, NULL, NULL, " in statement
    assert "''" not in statement.split("VALUES", 1)[1].split("ON CONFLICT", 1)[0]


def test_sql_int_renders_null_and_integers():
    assert generator.sql_int(None) == "NULL"
    assert generator.sql_int(12) == "12"
    assert generator.sql_int(-3) == "-3"


def test_listing_freshness_is_stamped_from_the_crawl_time():
    """A successful detail fetch is the last moment the ad was known live."""
    item = complete_property()
    statement = generator.property_upsert(item)
    assert "last_verified_at" in statement
    assert f"'{item['crawled_at']}'::timestamptz)" in statement


def test_reverification_never_rolls_back_a_newer_sale_check():
    statement = generator.property_upsert(complete_property())
    assert (
        "last_verified_at = GREATEST("
        "properties.last_verified_at, EXCLUDED.last_verified_at)" in statement
    )


def test_generator_still_rejects_a_property_without_bedrooms():
    item = complete_property()
    item["bedrooms"] = None
    assert "missing_bedrooms" in generator.property_issues(item)


def test_generator_rejects_a_non_integer_bathroom_count():
    item = complete_property()
    item["bathrooms"] = 2.5
    assert "invalid_bathrooms" in generator.property_issues(item)


def test_apostrophes_in_seller_supplied_text_are_escaped():
    item = complete_property()
    item["title"] = "Bán căn 'hot' quận 1"
    assert "'Bán căn ''hot'' quận 1'" in generator.property_upsert(item)


# ── Nationwide crawling ──────────────────────────────────────────────────────


def test_region_zero_means_every_province(monkeypatch):
    """region_v2 must be absent, not zero, or the API returns nothing."""
    seen: list[str] = []

    def fake_request_json(url, **_kwargs):
        seen.append(url)
        return {"ads": [], "total": 0}

    monkeypatch.setattr(crawler, "request_json", fake_request_json)
    crawler.crawl_complete_properties(
        target=1,
        max_pages=1,
        batch_size=50,
        region_id=0,
        category_id=1010,
        listing_type="SALE",
        timeout_seconds=1.0,
        retries=0,
        request_delay_seconds=0.0,
    )
    assert seen and "region_v2" not in seen[0]
    assert "cg=1010" in seen[0]


def test_a_named_region_is_still_sent(monkeypatch):
    seen: list[str] = []

    def fake_request_json(url, **_kwargs):
        seen.append(url)
        return {"ads": [], "total": 0}

    monkeypatch.setattr(crawler, "request_json", fake_request_json)
    crawler.crawl_complete_properties(
        target=1,
        max_pages=1,
        batch_size=50,
        region_id=12000,
        category_id=1010,
        listing_type="SALE",
        timeout_seconds=1.0,
        retries=0,
        request_delay_seconds=0.0,
    )
    assert "region_v2=12000" in seen[0]


# ── Merging several passes ───────────────────────────────────────────────────


def test_merge_deduplicates_and_lets_the_later_pass_win(tmp_path):
    first = tmp_path / "national.json"
    second = tmp_path / "hanoi.json"
    first.write_text(
        json.dumps([{"property_id": "P_1", "price": 1}, {"property_id": "P_2", "price": 2}]),
        encoding="utf-8",
    )
    second.write_text(
        json.dumps([{"property_id": "P_2", "price": 99}, {"property_id": "P_3", "price": 3}]),
        encoding="utf-8",
    )

    merged = merger.merge([first, second])

    assert [item["property_id"] for item in merged] == ["P_1", "P_2", "P_3"]
    assert merged[1]["price"] == 99


def test_merge_rejects_a_file_that_is_not_a_list(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"property_id": "P_1"}), encoding="utf-8")
    with pytest.raises(ValueError):
        merger.merge([path])
