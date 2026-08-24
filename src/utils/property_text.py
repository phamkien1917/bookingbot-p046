"""Shared text cleanup for property data pulled from crawled listings."""

from __future__ import annotations

import re

# Comprehensive prefixes to remove (crawler junk, marketing prefixes, noisy sale keywords)
_JUNK_PREFIXES = [
    re.compile(r"^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*", re.IGNORECASE),
    re.compile(r"^\s*\[(?:hot|si[eê]u\s*ph[aẩ]m|g[aấ]p|ch[ií]nh\s*ch[uủ]|b[aá]n\s*g[aấ]p)\]\s*", re.IGNORECASE),
    re.compile(r"^\s*(?:[🏡🏠🏢✨🔥💥⚡️🌟*]+)\s*", re.IGNORECASE),
    re.compile(r"^\s*(?:t[oô]i\s+)?(?:ch[ií]nh\s*ch[uủ])\s*(?:c[aầ]n\s*b[aá]n|b[aá]n\s*g[aấ]p|b[aá]n)?\s*", re.IGNORECASE),
    re.compile(r"^\s*(?:g[dđ]|gia\s*đ[iì]nh)\s*(?:c[aầ]n\s*b[aá]n|chuy[eể]n\s*nh[aà]|chuy[eể]n\s*v[eề]\s*qu[eê]\s*c[aầ]n\s*b[aá]n)\s*", re.IGNORECASE),
    re.compile(r"^\s*(?:c[aầ]n\s*b[aá]n\s*g[aấ]p|b[aá]n\s*g[aấ]p|b[aá]n\s*nhanh|c[aắ]t\s*l[oỗ]|c[aầ]n\s*ti[eề]n\s*b[aá]n\s*g[aấ]p|c[aầ]n\s*b[aá]n)\s*", re.IGNORECASE),
    re.compile(r"^\s*b[aá]n\s+(?=(?:c[aă]n\s*h[oộ]|ch(?![a-zA-Zà-ỹÀ-Ỹ])|cc(?![a-zA-Zà-ỹÀ-Ỹ])|nh[aà]|chung\s*c[uư]|t[aậ]p\s*th[eể]|bi[eệ]t\s*th[uự]|shophouse|penthouse|duplex|đ[aấ]t))", re.IGNORECASE),
    re.compile(r"^\s*b[aá]n\s+", re.IGNORECASE),
]

_PROPER_NOUNS = [
    (r"b[aã]i\s+ch[aá]y", "Bãi Cháy"),
    (r"nam\s+trung\s+y[eê]n", "Nam Trung Yên"),
    (r"ho[aà]ng\s+c[aầ]u", "Hoàng Cầu"),
    (r"c[aầ]u\s+gi[aấ]y", "Cầu Giấy"),
    (r"m[yỹ]\s+[dđ][iì]nh", "Mỹ Đình"),
    (r"y[eê]n\s+ho[aà]", "Yên Hòa"),
    (r"thanh\s+xu[aâ]n", "Thanh Xuân"),
    (r"[dđ][oố]ng\s+[dđ]a", "Đống Đa"),
    (r"h[aà]\s+[dđ][oô]ng", "Hà Đông"),
    (r"ba\s+[dđ][iì]nh", "Ba Đình"),
    (r"hai\s+b[aà]\s+tr[uư]ng", "Hai Bà Trưng"),
    (r"long\s+bi[eê]n", "Long Biên"),
    (r"t[aâ]y\s+h[oồ]", "Tây Hồ"),
    (r"ho[aà]n\s+ki[eế]m", "Hoàn Kiếm"),
    (r"b[aắ]c\s+t[uừ]\s+li[eê]m", "Bắc Từ Liêm"),
    (r"nam\s+t[uừ]\s+li[eê]m", "Nam Từ Liêm"),
    (r"ho[aà]ng\s+mai", "Hoàng Mai"),
    (r"b[iì]nh\s+th[aạ]nh", "Bình Thạnh"),
    (r"th[uủ]\s+[dđ][uứ]c", "Thủ Đức"),
    (r"g[oò]\s+v[aấ]p", "Gò Vấp"),
    (r"m[oỗ]\s+lao", "Mỗ Lao"),
    (r"b[aắ]c\s+h[aà]", "Bắc Hà"),
    (r"fodacon", "Fodacon"),
    (r"vinhomes", "Vinhomes"),
    (r"smart\s+city", "Smart City"),
    (r"ocean\s+park", "Ocean Park"),
    (r"times\s+city", "Times City"),
    (r"royal\s+city", "Royal City"),
    (r"goldmark\s+city", "Goldmark City"),
    (r"bcons", "Bcons"),
    (r"newsky", "Newsky"),
]


def clean_property_title(raw_title: str | None) -> str | None:
    """Standardize, clean and beautify real estate property titles cleanly."""
    if not raw_title:
        return raw_title

    title = raw_title.strip()

    # Step 1: Remove noisy junk / seller announcement prefixes first
    for pat in _JUNK_PREFIXES:
        title = pat.sub("", title).strip()

    # Step 2: Fix punctuation spacing: ",chung" -> ", chung" (ignoring decimals "5,8" and ellipsis "...")
    title = re.sub(r",([^\s\d])", r", \1", title)
    title = re.sub(r"(?<!\.)\.(?!\.)([^\s\d])", r". \1", title)
    title = re.sub(r"\s+", " ", title).strip()

    # Step 3: Expand abbreviations with STRICT Vietnamese Unicode letter boundary checks
    # (Avoid replacing "ch" inside "chính", "chủ", "Bãi Cháy")
    # CHCC / chcc -> Chung cư
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])chcc(?![a-zA-Zà-ỹÀ-Ỹ])", "Chung cư", title, flags=re.IGNORECASE)

    # "ch 506" / "ch506" -> "Căn hộ 506"
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])ch\s*(\d+[a-zA-Z]?)(?![a-zA-Zà-ỹÀ-Ỹ])", r"Căn hộ \1", title, flags=re.IGNORECASE)
    # "ccb10a" -> "Chung cư B10A"
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])cc\s*([a-zA-Z]\d+[a-zA-Z]?)(?![a-zA-Zà-ỹÀ-Ỹ])", r"Chung cư \1", title, flags=re.IGNORECASE)

    # Standalone "ch" -> "Căn hộ" (ONLY when not attached to any Vietnamese letters)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])ch(?![a-zA-Zà-ỹÀ-Ỹ])", "Căn hộ", title, flags=re.IGNORECASE)
    # Standalone "cc" -> "Chung cư"
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])cc(?![a-zA-Zà-ỹÀ-Ỹ])", "Chung cư", title, flags=re.IGNORECASE)

    # Urban area abbreviations
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])k[dđ]tm(?![a-zA-Zà-ỹÀ-Ỹ])", "Khu đô thị mới", title, flags=re.IGNORECASE)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])k[dđ]t(?![a-zA-Zà-ỹÀ-Ỹ])", "Khu đô thị", title, flags=re.IGNORECASE)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])tttm(?![a-zA-Zà-ỹÀ-Ỹ])", "TTTM", title, flags=re.IGNORECASE)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])(\d+)\s*pn(?![a-zA-Zà-ỹÀ-Ỹ])", r"\1PN", title, flags=re.IGNORECASE)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])(\d+)\s*wc(?![a-zA-Zà-ỹÀ-Ỹ])", r"\1WC", title, flags=re.IGNORECASE)
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])(\d+(?:[.,]\d+)?)\s*m2(?![a-zA-Zà-ỹÀ-Ỹ])", r"\1m²", title, flags=re.IGNORECASE)
    title = re.sub(
        r"(?<![a-zA-Zà-ỹÀ-Ỹ])(\d+(?:[.,]\d+)?)\s*m(?=\s+(?:nam|cầu|bắc|hoàng|đống|thanh|hà|hướng|tầng|view|full|giá|trung|đô)|$)",
        r"\1m²",
        title,
        flags=re.IGNORECASE,
    )

    # Step 4: Uppercase unit codes like "b10a" -> "B10A", "ct2a" -> "CT2A"
    title = re.sub(r"(?<![a-zA-Zà-ỹÀ-Ỹ])([a-zA-Z]{1,3}\d+[a-zA-Z]{0,2})(?![a-zA-Zà-ỹÀ-Ỹ])", lambda m: m.group(1).upper(), title)

    # Step 5: Capitalize proper nouns for locations
    for pattern_str, proper_name in _PROPER_NOUNS:
        pattern = re.compile(rf"(?<![a-zA-Zà-ỹÀ-Ỹ]){pattern_str}(?![a-zA-Zà-ỹÀ-Ỹ])", re.IGNORECASE)
        title = pattern.sub(proper_name, title)

    # Step 6: Fix double/redundant phrasing
    title = re.sub(r"\bcăn hộ\s+căn hộ\b", "Căn hộ", title, flags=re.IGNORECASE)
    title = re.sub(r"\bchung cư\s+chung cư\b", "Chung cư", title, flags=re.IGNORECASE)
    title = re.sub(r"\bcăn hộ\s+chung cư\b", "Căn hộ Chung cư", title, flags=re.IGNORECASE)

    # Capitalize words right after commas: ", chung cư" -> ", Chung cư"
    title = re.sub(r",\s*([a-zà-ỹ])", lambda m: ", " + m.group(1).upper(), title)

    title = re.sub(r"\s+", " ", title).strip()

    # Step 7: Capitalize first letter of title
    if title:
        title = title[0].upper() + title[1:]

    return title


def build_full_address(
    address_line: str | None,
    ward: str | None,
    district: str | None,
    province: str | None,
) -> str:
    """Join address parts without repeating ward/district/province already present in address_line.

    Crawled ``address_line`` values are often already a full human-readable address
    (street + ward + district + province in one string), so appending the same
    ward/district/province again produces a visibly duplicated address.
    """
    if address_line:
        tail = ", ".join(filter(None, [ward, district, province]))
        if not tail or tail in address_line:
            return address_line
        return f"{address_line}, {tail}" if tail not in address_line else address_line
    return ", ".join(filter(None, [ward, district, province]))
