from src.services.search_criteria_service import build_search_criteria, extract_search_criteria


def test_booking_phrase_is_not_misclassified_as_land() -> None:
    criteria, _ = extract_search_criteria("Đặt lịch xem căn số 1 vào 14 giờ")
    assert "property_kind" not in criteria


def test_real_land_search_is_still_supported() -> None:
    criteria, _ = extract_search_criteria("Tìm đất nền Quận 9 dưới 3 tỷ")
    assert criteria["property_kind"] == "LAND"
    assert criteria["district"] == "Quận 9"
    assert criteria["max_price"] == 3_000_000_000


def test_follow_up_budget_keeps_previous_location_and_kind() -> None:
    previous = {
        "district": "Quận 7",
        "property_kind": "APARTMENT",
        "max_price": 4_000_000_000,
        "min_bedrooms": 2,
    }
    merged = build_search_criteria("Vậy nới lên 8 tỷ", previous)

    assert merged == {
        "district": "Quận 7",
        "property_kind": "APARTMENT",
        "max_price": 8_000_000_000,
        "min_bedrooms": 2,
    }


def test_explicit_property_kind_correction_wins() -> None:
    previous = {"district": "Quận 7", "property_kind": "LAND"}
    merged = build_search_criteria("Không phải đất, tôi cần căn hộ", previous)
    assert merged["district"] == "Quận 7"
    assert merged["property_kind"] == "APARTMENT"


def test_bare_district_name_replaces_previous_location() -> None:
    previous = {
        "district": "Quận 7",
        "province": "Hồ Chí Minh",
        "property_kind": "APARTMENT",
        "max_price": 8_000_000_000,
        "min_bedrooms": 2,
        "min_area": 50,
    }

    merged = build_search_criteria("tìm nhà dưới 5 tỷ ở thanh xuân", previous)

    assert merged == {
        "district": "Quận Thanh Xuân",
        "max_price": 5_000_000_000,
    }


def test_bare_district_with_province_keeps_both_location_parts() -> None:
    criteria, groups = extract_search_criteria("Tìm căn hộ ở Thanh Xuân Hà Nội")

    assert criteria["district"] == "Quận Thanh Xuân"
    assert criteria["province"] == "Hà Nội"
    assert criteria["property_kind"] == "APARTMENT"
    assert "location" in groups


def test_fresh_search_does_not_silently_apply_saved_area_or_bedrooms() -> None:
    previous = {
        "district": "Quận 7",
        "property_kind": "APARTMENT",
        "min_bedrooms": 3,
        "min_area": 50,
    }

    merged = build_search_criteria("Tìm căn hộ dưới 5 tỷ ở Hà Nội", previous)

    assert merged == {
        "province": "Hà Nội",
        "property_kind": "APARTMENT",
        "max_price": 5_000_000_000,
    }


def test_follow_up_bedroom_filter_still_refines_current_search() -> None:
    previous = {
        "district": "Quận Thanh Xuân",
        "max_price": 5_000_000_000,
    }

    merged = build_search_criteria("3 phòng ngủ", previous)

    assert merged == {**previous, "min_bedrooms": 3}


def test_minimum_price_search_in_hanoi() -> None:
    criteria, groups = extract_search_criteria("Tim nha tren 10 ty o Ha Noi")

    assert criteria == {
        "min_price": 10_000_000_000,
        "province": "Hà Nội",
    }
    assert groups == {"budget", "location"}
