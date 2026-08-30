"""Regression: a stated monthly income must not be read as a listing price.

The model kept turning "thu nhập mình 40 triệu một tháng" into "bạn muốn mua
căn 40 tỷ?". `_extract_finance` is the deterministic backstop.
"""

from src.agents.nodes.supervisor import _extract_finance
from src.services.chat_state_service import normalize_text

M = 1_000_000
B = 1_000_000_000


def _run(text: str) -> tuple[int | None, int | None]:
    return _extract_finance(normalize_text(text))


def test_income_one_month_phrasing_and_own_capital():
    income, capital = _run("thu nhập mình 40 triệu một tháng, có sẵn 1 tỷ, vay mua căn số 1 được không")
    assert income == 40 * M
    assert capital == 1 * B


def test_income_slash_thang_and_de_danh():
    income, capital = _run("lương 25tr/tháng, để dành được 800 triệu")
    assert income == 25 * M
    assert capital == 800 * M


def test_plain_price_is_not_income():
    income, capital = _run("tìm chung cư 2 phòng ngủ ở Cầu Giấy dưới 6 tỷ")
    assert income is None
    assert capital is None


def test_income_in_ty_needs_month_marker():
    # "thu nhập 1 tỷ" with no month marker is ambiguous — do not guess.
    assert _run("thu nhập 1 tỷ")[0] is None
    assert _run("thu nhập 1 tỷ mỗi tháng")[0] == 1 * B


if __name__ == "__main__":
    test_income_one_month_phrasing_and_own_capital()
    test_income_slash_thang_and_de_danh()
    test_plain_price_is_not_income()
    test_income_in_ty_needs_month_marker()
    print("ok")
