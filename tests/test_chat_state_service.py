from datetime import date, datetime

import pytest

from src.services.chat_state_service import (
    LOCAL_TZ,
    default_chat_state,
    extract_ordinal,
    load_chat_state,
    parse_requested_date,
    parse_requested_hour,
    save_chat_state,
)


@pytest.mark.parametrize(
    ("message", "maximum", "expected"),
    [
        ("chọn căn số 1", 3, 0),
        ("tôi thích căn thứ hai", 3, 1),
        ("lấy căn cuối", 4, 3),
        ("2", 4, 1),
        ("căn 2 phòng ngủ", 3, 1),
        ("chọn căn số 9", 3, None),
    ],
)
def test_extract_ordinal(message: str, maximum: int, expected: int | None) -> None:
    assert extract_ordinal(message, maximum=maximum) == expected


def test_parse_relative_vietnamese_date() -> None:
    friday = datetime(2026, 8, 21, 10, tzinfo=LOCAL_TZ)
    assert parse_requested_date("14 giờ thứ Bảy tuần này", now=friday) == date(2026, 8, 22)
    assert parse_requested_date("chiều mai", now=friday) == date(2026, 8, 22)
    assert parse_requested_date("Chủ Nhật tuần sau", now=friday) == date(2026, 8, 30)


@pytest.mark.parametrize(
    ("message", "expected"),
    [("14 giờ", 14), ("2h chiều", 14), ("buổi sáng", 9), ("buổi chiều", 14)],
)
def test_parse_requested_hour(message: str, expected: int) -> None:
    assert parse_requested_hour(message) == expected


def test_chat_state_round_trip_ignores_unknown_fields() -> None:
    state = default_chat_state()
    state.update({"phase": "SEARCH_RESULTS", "selected_property_id": "p-1"})
    metadata = save_chat_state({"title": "Demo"}, state)
    metadata["chat_state"]["untrusted_future_field"] = "ignored"

    restored = load_chat_state(metadata)

    assert restored["phase"] == "SEARCH_RESULTS"
    assert restored["selected_property_id"] == "p-1"
    assert "untrusted_future_field" not in restored


def test_match_property_by_title() -> None:
    from src.utils.property_text import match_property_by_title

    pool = [
        {"id": "p1", "title": "Căn Hộ Mini Hoàng Đạo Thành. Thanh Xuân- Thoáng Đẹp Rộng, Giá Rẻ"},
        {"id": "p2", "title": "Chung cư cao cấp Feliz Home 297 Hoàng Mai"},
        {"id": "p3", "title": "CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông"},
    ]

    # Full exact query matching
    idx, prop = match_property_by_title("đặt lịch căn CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông cho tôi", pool)
    assert idx == 2
    assert prop["id"] == "p3"

    # Partial / keyword query matching
    idx2, prop2 = match_property_by_title("đặt lịch xem căn Fodacon Bắc Hà", pool)
    assert idx2 == 2
    assert prop2["id"] == "p3"

    # Feliz Home matching
    idx3, prop3 = match_property_by_title("xem chi tiết Feliz Home", pool)
    assert idx3 == 1
    assert prop3["id"] == "p2"

    # Non matching query
    idx4, prop4 = match_property_by_title("tìm căn ở đà nẵng", pool)
    assert idx4 is None
    assert prop4 is None

