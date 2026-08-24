from src.services.chat_ai_service import (
    ChatUnderstanding,
    LLMSearchCriteria,
    SearchNarrative,
    order_properties,
    reconcile_understanding,
    render_grounded_search,
)


def test_model_ranking_cannot_inject_unknown_property() -> None:
    properties = [
        {"id": "p-1", "title": "A"},
        {"id": "p-2", "title": "B"},
    ]

    ordered = order_properties(properties, ["invented-id", "p-2", "p-2"])

    assert [item["id"] for item in ordered] == ["p-2", "p-1"]


def test_unsupported_model_filter_is_removed_before_sql() -> None:
    raw = ChatUnderstanding(
        intent="SEARCH",
        is_new_search=True,
        hard_criteria=LLMSearchCriteria(
            district="Thanh Xuân",
            province="Hà Nội",
            property_kind="HOUSE",
            min_price=0,
            max_price=4_600_000_000,
            min_bedrooms=2,
        ),
        soft_preferences=["yên tĩnh"],
        household_context=["sắp có em bé"],
        commute_landmark="Ngã Tư Sở",
        confidence=0.9,
    )

    safe = reconcile_understanding(
        "Hãy tìm ở Thanh Xuân một chỗ yên tĩnh có 2 phòng ngủ dưới 4,6 tỷ",
        raw,
    )

    assert safe.hard_criteria.property_kind is None
    assert safe.hard_criteria.min_price is None
    assert safe.hard_criteria.max_price == 4_600_000_000


def test_province_search_cannot_be_duplicated_as_a_district() -> None:
    raw = ChatUnderstanding(
        intent="SEARCH",
        is_new_search=True,
        hard_criteria=LLMSearchCriteria(
            district="Ha Noi",
            province="Ha Noi",
            min_price=10_000_000_000,
        ),
        confidence=0.95,
    )

    safe = reconcile_understanding("Tim nha tren 10 ty o Ha Noi", raw)

    assert safe.hard_criteria.district is None
    assert safe.hard_criteria.province == "Hà Nội"
    assert safe.hard_criteria.min_price == 10_000_000_000
    assert safe.hard_criteria.max_price is None


def test_grounded_renderer_uses_verified_numeric_facts() -> None:
    narrative = SearchNarrative(
        opening="Mình đã cân nhắc hoàn cảnh gia đình bạn.",
        preference_assessment="Ưu tiên yên tĩnh cần được kiểm tra thực địa.",
        caveat="Chưa có dữ liệu thời gian di chuyển.",
        follow_up="Bạn muốn xem căn nào trước?",
        ranked_property_ids=["p-1"],
    )
    properties = [{
        "id": "p-1",
        "title": "Căn đã xác minh",
        "list_price": 4_600_000_000,
        "area_sqm": 75,
        "bedrooms": 2,
        "district": "Quận Thanh Xuân",
        "province": "Hà Nội",
    }]

    rendered = render_grounded_search(narrative, properties)

    assert "4.6 tỷ" in rendered
    assert "75 m²" in rendered
    assert "2 phòng ngủ" in rendered
    assert "Quận Thanh Xuân, Hà Nội" in rendered
    assert "Chưa có dữ liệu thời gian di chuyển" in rendered
