"""Crawled descriptions carry the broker's sales pitch, not just facts.

Nera quotes these descriptions back to customers, so a phone number left in the
text reads as Nera handing out someone else's contact details.
"""

from src.utils.property_text import clean_property_description


def test_contact_sentence_is_dropped_but_the_facts_stay() -> None:
    cleaned = clean_property_description(
        "Căn hộ 2PN, 55m², ban công hướng Đông Bắc.\n"
        "Chi tiết liên hệ 0941 356 *** Ms. Mai để nhận bảng giá."
    )

    assert "55m²" in cleaned
    assert "0941" not in cleaned
    assert "Mai" not in cleaned


def test_contact_appended_to_a_real_sentence_loses_only_the_contact() -> None:
    cleaned = clean_property_description(
        "Sổ đỏ sẵn, sang tên nhanh. Liên hệ: 0869 929 *** ngay để xem nhà 24/7."
    )

    assert cleaned == "Sổ đỏ sẵn, sang tên nhanh."


def test_stranded_broker_name_goes_with_the_number() -> None:
    # The number lives in its own sentence, so dropping it would otherwise
    # leave "Mr Mừng." standing alone as if it described the home.
    cleaned = clean_property_description("Nhà đẹp.\nĐiện thoại: 0909 139 *** (24/7). Mr Mừng.")

    assert cleaned == "Nhà đẹp."


def test_decorated_line_keeps_its_sentence() -> None:
    # "***" also opens real bullet lines; only a digit before it means a phone.
    cleaned = clean_property_description("***The Global City rộng 117,4 hecta.")

    assert cleaned == "The Global City rộng 117,4 hecta."


def test_divider_lines_are_removed() -> None:
    cleaned = clean_property_description("Giá 3 tỷ.\n------------------\nSổ hồng riêng.")

    assert cleaned == "Giá 3 tỷ.\nSổ hồng riêng."


def test_broker_free_text_survives_untouched() -> None:
    text = "Nhà 4 tầng, sổ đỏ lâu dài.\n- Diện tích xây dựng: 212,9m².\n- An ninh 24/7."

    assert clean_property_description(text) == text


def test_excerpt_stops_at_a_sentence_not_mid_word() -> None:
    text = "Một câu đủ dài để vượt giới hạn. Câu thứ hai bị cắt bỏ hoàn toàn."

    cleaned = clean_property_description(text, max_chars=40)

    assert cleaned == "Một câu đủ dài để vượt giới hạn.…"


def test_empty_input_is_passed_through() -> None:
    assert clean_property_description(None) is None
    assert clean_property_description("") == ""
