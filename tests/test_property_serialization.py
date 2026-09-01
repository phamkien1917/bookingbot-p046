"""What a property looks like by the time the customer sees it.

`serialize_property_item` is the last thing that touches a listing before it
becomes a card in the chat and a line in the prompt the model reasons over. A
mistake here is not a crash — it is a wrong price on screen, or a stale listing
presented as fresh, which is the one thing a grounded system must never do.

These are pure functions over a plain object, so no database is involved.
"""

from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace

import pytest

from src.agents.nodes.inventory_agent import (
    _interleave_properties_by_province,
    _num,
    _price_text,
    serialize_property_item,
)
from src.utils.time import utcnow


class TestNum:
    """Prices and areas arrive from asyncpg as Decimal, which JSON cannot carry."""

    def test_a_decimal_becomes_a_float(self):
        assert _num(Decimal("4500000000.00")) == 4_500_000_000.0

    @pytest.mark.parametrize("value", [None, "", "n/a", object()])
    def test_anything_unusable_becomes_nothing(self, value):
        assert _num(value) is None

    def test_zero_survives(self):
        """0 is a real value; returning None for it would hide a free listing."""
        assert _num(0) == 0.0
        assert _num(Decimal("0")) == 0.0


class TestPriceText:
    @pytest.mark.parametrize(
        "amount,expected",
        [
            (5_000_000_000, "5 tỷ"),
            (4_500_000_000, "4.5 tỷ"),
            (1_000_000_000, "1 tỷ"),
            (850_000_000, "850 triệu"),
            (999_999_999, "1000 triệu"),
        ],
    )
    def test_money_reads_the_way_a_buyer_says_it(self, amount, expected):
        assert _price_text(amount) == expected

    def test_a_missing_price_says_so_instead_of_showing_zero(self):
        """A listing with no price must invite a call, not advertise 0 đồng."""
        assert _price_text(None) == "Liên hệ"


def make_property(**overrides):
    """A Property-shaped object; serialization only reads attributes."""
    base = dict(
        id="11111111-1111-1111-1111-111111111111",
        code="NR-001",
        property_kind=SimpleNamespace(value="APARTMENT"),
        title="Căn hộ 2PN Cầu Giấy",
        description="Căn góc, ban công Đông Nam.",
        status=SimpleNamespace(value="AVAILABLE"),
        address_line="12 Trần Duy Hưng",
        ward="Trung Hoà",
        district="Cầu Giấy",
        province="Hà Nội",
        latitude=Decimal("21.0122"),
        longitude=Decimal("105.7994"),
        area_sqm=Decimal("72.5"),
        bedrooms=2,
        bathrooms=2,
        floor_number=12,
        orientation="Đông Nam",
        legal_status="Sổ đỏ",
        list_price=Decimal("4500000000"),
        currency="VND",
        features={"balcony": True},
        media=[],
        published_at=utcnow(),
        last_verified_at=utcnow(),
    )
    base.update(overrides)
    return SimpleNamespace(**base)


class TestSerializeProperty:
    def test_every_number_comes_out_json_safe(self):
        item = serialize_property_item(make_property())

        for key in ("latitude", "longitude", "area_sqm", "list_price"):
            assert isinstance(item[key], float), f"{key} is not JSON-serialisable"

    def test_a_listing_verified_today_is_not_marked_stale(self):
        item = serialize_property_item(make_property())

        assert item["is_stale"] is False
        assert item["verified_days_ago"] == 0
        assert item["verification_label"]

    def test_an_old_listing_is_marked_stale_rather_than_quietly_shown(self):
        """Freshness is a claim to the customer; it has to track reality."""
        old = utcnow() - timedelta(days=120)
        item = serialize_property_item(make_property(last_verified_at=old, published_at=old))

        assert item["is_stale"] is True
        assert item["verified_days_ago"] >= 120

    def test_the_cover_image_leads_regardless_of_upload_order(self):
        media = [
            SimpleNamespace(
                id="a", media_type="IMAGE", url="second.jpg", caption=None,
                sort_order=0, is_cover=False,
            ),
            SimpleNamespace(
                id="b", media_type="IMAGE", url="cover.jpg", caption=None,
                sort_order=9, is_cover=True,
            ),
        ]
        item = serialize_property_item(make_property(media=media))

        assert item["image"] == "cover.jpg"
        assert item["media"][0]["url"] == "cover.jpg"

    def test_a_listing_with_no_photo_reports_none_rather_than_breaking(self):
        item = serialize_property_item(make_property(media=[]))

        assert item["image"] is None
        assert item["media"] == []


class TestInterleaveByProvince:
    """A nationwide search must not return one city's inventory and stop."""

    def test_results_alternate_between_provinces(self):
        items = [{"province": "Hà Nội", "n": i} for i in range(5)]
        items += [{"province": "Hồ Chí Minh", "n": i} for i in range(5)]

        picked = _interleave_properties_by_province(items, limit=4)

        provinces = [item["province"] for item in picked]
        assert provinces.count("Hà Nội") == 2
        assert provinces.count("Hồ Chí Minh") == 2

    def test_one_province_is_not_padded_with_nothing(self):
        items = [{"province": "Đà Nẵng", "n": i} for i in range(3)]

        assert len(_interleave_properties_by_province(items, limit=10)) == 3

    def test_a_missing_province_is_still_returned(self):
        """A listing with no province is inventory too; dropping it hides stock."""
        items = [{"province": None, "n": 0}, {"province": "Hà Nội", "n": 1}]

        assert len(_interleave_properties_by_province(items, limit=10)) == 2
