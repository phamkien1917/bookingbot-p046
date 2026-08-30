"""Screenshot regressions:
- crawled ad titles ("Nhanh kẻo hết! ... CK 25,5% ... LH 09xx") reaching the card
- a bare "Nhà" title reaching the card
- "vay mua căn số 1 được không" answered without checking that căn's price
"""

from types import SimpleNamespace

from src.agents.nodes.inventory_agent import _display_title
from src.services.affordability import assess_target_price, estimate_affordability
from src.utils.property_text import clean_property_title

B = 1_000_000_000


def _prop(**kw):
    base = dict(
        title=None, property_kind=SimpleNamespace(value="APARTMENT"),
        bedrooms=2, area_sqm=55, ward="Phường Láng Hạ", district="Quận Đống Đa", province="Hà Nội",
    )
    base.update(kw)
    return SimpleNamespace(**base)


def test_title_tail_and_prefix_stripped():
    raw = "Nhanh kẻo hết! Giỏ hàng CĐT An Gia - CK 25,5% + Full nội thất & full điện máy - LH ngay 0902 999 ***"
    assert clean_property_title(raw) == "An Gia"  # what's left is too thin -> synth kicks in


def test_good_title_kept():
    raw = "CCMN Mặt Phố Xe Buýt, Thoáng Đẹp, Có Thể Làm Văn Phòng"
    assert clean_property_title(raw) == raw


def test_display_title_synthesised_from_fields_when_junk():
    assert _display_title(_prop(title="Nhà")) == "Căn hộ 2PN 55m² · Phường Láng Hạ"
    assert _display_title(_prop(title="An Gia")) == "Căn hộ 2PN 55m² · Phường Láng Hạ"


def test_display_title_keeps_real_title():
    p = _prop(title="Căn hộ CT2A Hoàng Cầu sổ đỏ 58m²")
    assert _display_title(p) == "Căn hộ CT2A Hoàng Cầu sổ đỏ 58m²"


def test_assess_target_price_verdict():
    est = estimate_affordability(40_000_000, own_capital_vnd=1 * B)
    assert "nằm trong tầm" in assess_target_price(est, 2_590_000_000)
    assert "cao hơn" in assess_target_price(est, 5 * B)
