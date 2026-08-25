from datetime import datetime
from zoneinfo import ZoneInfo

from src.services.customer_memory_service import extract_time_preferences, time_preference_score


def test_extract_explicit_weekend_evening_preference() -> None:
    assert extract_time_preferences("Tôi ưu tiên xem nhà cuối tuần sau 18h") == ["AFTER_18", "WEEKEND"]


def test_time_preference_score_prioritizes_matching_slot() -> None:
    saturday_evening = datetime(2026, 8, 29, 19, tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"))
    weekday_morning = datetime(2026, 8, 26, 9, tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"))
    preferences = ["WEEKEND", "AFTER_18"]
    assert time_preference_score(saturday_evening, preferences) == 4
    assert time_preference_score(weekday_morning, preferences) == 0


def test_one_off_time_without_preference_language_is_only_extracted_by_parser_layer() -> None:
    # Persistence additionally requires explicit preference language; this pure
    # extractor can still identify the slot label for callers that need it.
    assert extract_time_preferences("Đặt lịch thứ Bảy lúc 14h") == ["WEEKEND"]
