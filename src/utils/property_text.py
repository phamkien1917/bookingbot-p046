"""Shared text cleanup for property data pulled from crawled listings."""

from __future__ import annotations

import re

# Comprehensive prefixes to remove (crawler junk, marketing prefixes, noisy sale keywords)
_JUNK_PREFIXES = [
    re.compile(r"^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*", re.IGNORECASE),
    re.compile(r"^\s*\[(?:hot|si[eê]u\s*ph[aẩ]m|g[aấ]p|ch[ií]nh\s*ch[uủ]|b[aá]n\s*g[aấ]p)\]\s*", re.IGNORECASE),
    re.compile(r"^\s*(?:g[dđ]|gia\s*đ[iì]nh)\s*(?:c[aầ]n\s*b[aá]n|chuy[eể]n\s*nh[aà]|chuy[eể]n\s*v[eề]\s*qu[eê]\s*c[aầ]n\s*b[aá]n)\s+", re.IGNORECASE),
    re.compile(r"^\s*(?:ch[ií]nh\s*ch[uủ]\s*c[aầ]n\s*b[aá]n|ch[ií]nh\s*ch[uủ]\s*b[aá]n\s*g[aấ]p|ch[ií]nh\s*ch[uủ]\s*b[aá]n|c[aầ]n\s*b[aá]n\s*g[aấ]p|b[aá]n\s*g[aấ]p|b[aá]n\s*nhanh|c[aắ]t\s*l[oỗ]|c[aầ]n\s*ti[eề]n\s*b[aá]n\s*g[aấ]p)\s+", re.IGNORECASE),
    re.compile(r"^\s*b[aá]n\s+(?=(?:c[aă]n\s*h[oộ]|ch\b|cc\b|nh[aà]|chung\s*c[uư]|t[aậ]p\s*th[eể]|bi[eệ]t\s*th[uự]|shophouse|penthouse|duplex|đ[aấ]t))", re.IGNORECASE),
    re.compile(r"^\s*b[aá]n\s+", re.IGNORECASE),
]

_PROPER_NOUNS = [
    (r"\bnam\s+trung\s+y[eê]n\b", "Nam Trung Yên"),
    (r"\bho[aà]ng\s+c[aầ]u\b", "Hoàng Cầu"),
    (r"\bc[aầ]u\s+gi[aấ]y\b", "Cầu Giấy"),
    (r"\bm[yỹ]\s+[dđ][iì]nh\b", "Mỹ Đình"),
    (r"\by[eê]n\s+ho[aà]\b", "Yên Hòa"),
    (r"\bthanh\s+xu[aâ]n\b", "Thanh Xuân"),
    (r"\b[dđ][oố]ng\s+[dđ]a\b", "Đống Đa"),
    (r"\bh[aà]\s+[dđ][oô]ng\b", "Hà Đông"),
    (r"\bba\s+[dđ][iì]nh\b", "Ba Đình"),
    (r"\bhai\s+b[aà]\s+tr[uư]ng\b", "Hai Bà Trưng"),
    (r"\blong\s+bi[eê]n\b", "Long Biên"),
    (r"\bt[aâ]y\s+h[oồ]\b", "Tây Hồ"),
    (r"\bho[aà]n\s+ki[eế]m\b", "Hoàn Kiếm"),
    (r"\bb[aắ]c\s+t[uừ]\s+li[eê]m\b", "Bắc Từ Liêm"),
    (r"\bnam\s+t[uừ]\s+li[eê]m\b", "Nam Từ Liêm"),
    (r"\bho[aà]ng\s+mai\b", "Hoàng Mai"),
    (r"\bb[iì]nh\s+th[aạ]nh\b", "Bình Thạnh"),
    (r"\bth[uủ]\s+[dđ][uứ]c\b", "Thủ Đức"),
    (r"\bg[oò]\s+v[aấ]p\b", "Gò Vấp"),
    (r"\bvinhomes\b", "Vinhomes"),
    (r"\bsmart\s+city\b", "Smart City"),
    (r"\bocean\s+park\b", "Ocean Park"),
    (r"\btimes\s+city\b", "Times City"),
    (r"\broyal\s+city\b", "Royal City"),
    (r"\bgoldmark\s+city\b", "Goldmark City"),
    (r"\bthe\s+matrix\s+one\b", "The Matrix One"),
    (r"\bimperia\b", "Imperia"),
    (r"\bmasteri\b", "Masteri"),
    (r"\bsunshine\b", "Sunshine"),
    (r"\bgamuda\b", "Gamuda"),
    (r"\becopark\b", "Ecopark"),
]


def clean_property_title(raw_title: str | None) -> str | None:
    """Standardize, clean and beautify real estate property titles cleanly."""
    if not raw_title:
        return raw_title

    title = raw_title.strip()

    # Step 1: Remove noisy junk prefixes
    for pat in _JUNK_PREFIXES:
        title = pat.sub("", title).strip()

    # Step 2: Fix punctuation spacing: ",chung" -> ", chung" (ignoring decimals like "5,8")
    title = re.sub(r",([^\s\d])", r", \1", title)
    title = re.sub(r"\.([^\s\d])", r". \1", title)
    title = re.sub(r"\s+", " ", title).strip()

    # Step 3: Expand common abbreviations
    # "ch 506" / "ch506" -> "Căn hộ 506"
    title = re.sub(r"\bch\s*(\d+[a-zA-Z]?)\b", r"Căn hộ \1", title, flags=re.IGNORECASE)
    # "ccb10a" -> "Chung cư B10A"
    title = re.sub(r"\bcc\s*([a-zA-Z]\d+[a-zA-Z]?)\b", r"Chung cư \1", title, flags=re.IGNORECASE)
    # standalone "ch" -> "Căn hộ"
    title = re.sub(r"\bch\b", "Căn hộ", title, flags=re.IGNORECASE)
    # standalone "cc" -> "Chung cư"
    title = re.sub(r"\bcc\b", "Chung cư", title, flags=re.IGNORECASE)
    # "kđtm" / "kđt"
    title = re.sub(r"\bk[dđ]tm\b", "Khu đô thị mới", title, flags=re.IGNORECASE)
    title = re.sub(r"\bk[dđ]t\b", "Khu đô thị", title, flags=re.IGNORECASE)
    title = re.sub(r"\btttm\b", "TTTM", title, flags=re.IGNORECASE)
    # "2pn" / "2 pn" -> "2PN"
    title = re.sub(r"\b(\d+)\s*pn\b", r"\1PN", title, flags=re.IGNORECASE)
    # "2wc" / "2 wc" -> "2WC"
    title = re.sub(r"\b(\d+)\s*wc\b", r"\1WC", title, flags=re.IGNORECASE)
    # "58m2" / "58 m2" -> "58m²"
    title = re.sub(r"\b(\d+(?:[.,]\d+)?)\s*m2\b", r"\1m²", title, flags=re.IGNORECASE)
    # "sổ đỏ 58m" -> "sổ đỏ 58m²"
    title = re.sub(r"\b(diện tích|dt|sổ đỏ|sd)\s+(\d+(?:[.,]\d+)?)\s*m\b", r"\1 \2m²", title, flags=re.IGNORECASE)

    # Step 4: Uppercase building codes like "b10a" -> "B10A", "ct2a" -> "CT2A", "n04b" -> "N04B"
    title = re.sub(r"\b([a-zA-Z]{1,3}\d+[a-zA-Z]{0,2})\b", lambda m: m.group(1).upper(), title)

    # Step 5: Capitalize proper nouns for locations
    for pattern_str, proper_name in _PROPER_NOUNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        title = pattern.sub(proper_name, title)

    # Step 6: Fix double "Căn hộ Căn hộ" or "Chung cư Chung cư"
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
