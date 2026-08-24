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


def test_region_search_mien_bac() -> None:
    criteria, groups = extract_search_criteria("nhà trên 10 tỷ ở miền bắc")

    assert criteria == {
        "min_price": 10_000_000_000,
        "region": "Miền Bắc",
    }
    assert groups == {"budget", "location"}


def test_region_replaces_previous_province_in_memory() -> None:
    previous = {
        "province": "Hà Nội",
        "min_price": 10_000_000_000,
    }
    merged = build_search_criteria("nhà trên 10 tỷ ở miền bắc", previous)

    assert merged == {
        "region": "Miền Bắc",
        "min_price": 10_000_000_000,
    }


def test_format_criteria_summary_deduplicates_identical_locations() -> None:
    from src.agents.nodes.inventory_agent import format_criteria_summary

    summary = format_criteria_summary({
        "area_or_ward": "Hà Nội",
        "province": "Hà Nội",
        "min_price": 10_000_000_000,
    })
    assert summary == "Hà Nội, từ 10 tỷ"
    assert "Hà Nội, Hà Nội" not in summary


def test_format_criteria_summary_with_region() -> None:
    from src.agents.nodes.inventory_agent import format_criteria_summary

    summary = format_criteria_summary({
        "region": "Miền Bắc",
        "min_price": 10_000_000_000,
    })
    assert summary == "Miền Bắc, từ 10 tỷ"


def test_explicit_requested_quantity() -> None:
    criteria, groups = extract_search_criteria("tìm 2 nhà dưới 5 tỷ ở miền bắc")
    assert criteria["limit"] == 2
    assert criteria["max_price"] == 5_000_000_000
    assert criteria["region"] == "Miền Bắc"
    assert "quantity" in groups

    criteria_word, groups_word = extract_search_criteria("gợi ý ba căn hộ ở Cầu Giấy")
    assert criteria_word["limit"] == 3
    assert criteria_word["district"] == "Quận Cầu Giấy"
    assert criteria_word["property_kind"] == "APARTMENT"
    assert "quantity" in groups_word


def test_bedroom_not_confused_with_quantity() -> None:
    criteria, groups = extract_search_criteria("tìm căn hộ 2 phòng ngủ ở Hà Nội")
    assert "limit" not in criteria
    assert criteria["min_bedrooms"] == 2
    assert criteria["province"] == "Hà Nội"
    assert "quantity" not in groups


def test_interleave_properties_by_province() -> None:
    from src.agents.nodes.inventory_agent import _interleave_properties_by_province

    items = [
        {"id": "1", "province": "Hà Nội", "list_price": 1_000_000_000},
        {"id": "2", "province": "Hà Nội", "list_price": 2_000_000_000},
        {"id": "3", "province": "Quảng Ninh", "list_price": 4_000_000_000},
        {"id": "4", "province": "Bắc Giang", "list_price": 5_000_000_000},
    ]
    interleaved = _interleave_properties_by_province(items, limit=4)
    # The first 3 items should be from 3 distinct provinces: Hà Nội, Quảng Ninh, Bắc Giang
    provs = [x["province"] for x in interleaved[:3]]
    assert "Hà Nội" in provs
    assert "Quảng Ninh" in provs
    assert "Bắc Giang" in provs



