"""Shared text cleanup for property data pulled from crawled listings."""

from __future__ import annotations

import re
from typing import Any

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


# Crawled descriptions end in the broker's own sales pitch: a phone number, a
# name to call, a thank-you. None of it is a fact about the home, and quoting it
# back makes Nera sound like it is reading a classified ad.
_JUNK_SENTENCE = re.compile(
    r"0\d[\d\s.\-]{6,}\d"                                 # phone number
    r"|\d\s*\*{3,}"                                       # masked phone tail: "0903 899 ***"
    r"|(?<![a-zà-ỹ])(?:li[eê]n\s*h[eệ]|lh|hotline|zalo|inbox|call|alo)(?![a-zà-ỹ])"
    r"|(?<![a-zà-ỹ])(?:g[oọ]i\s*ngay|nh[aắ]n\s*tin|xem\s*nh[aà]\s*24/?7)(?![a-zà-ỹ])"
    r"|(?<![a-zà-ỹ])(?:mi[eễ]n\s*ph[ií]\s*m[oô]i\s*gi[oớ]i|ph[ií]\s*m[oô]i\s*gi[oớ]i|hoa\s*h[oồ]ng)(?![a-zà-ỹ])"
    r"|(?<![a-zà-ỹ])(?:c[aả]m\s*[oơ]n|tr[aâ]n\s*tr[oọ]ng|h[aâ]n\s*h[aạ]nh|[dđ][uừ]ng\s*b[oỏ]\s*l[oỡ]|nhanh\s*tay)(?![a-zà-ỹ])",
    re.IGNORECASE,
)

# "0909 139 *** (24/7). Mr Mừng." loses the number to the rule above and leaves
# the name stranded as its own sentence.
_BROKER_NAME_ONLY = re.compile(
    r"^(?:mr|ms|mrs|anh|ch[iị]|em|c[oô]|ch[uú])\.?\s+\S{1,15}\.?$",
    re.IGNORECASE,
)

# A line made only of ***, ----, ==== or ____ is a visual divider from the source
# listing; it renders as a stray rule in the chat bubble.
_DIVIDER_LINE = re.compile(r"^[\s*\-=_~•+]+$")

# Splitting after "Ms." would leave the broker's name behind once the sentence
# holding their phone number is dropped.
_SENTENCE_SPLIT = re.compile(
    r"(?<=[.!?…])(?<!\bMs\.)(?<!\bMr\.)(?<!Mrs\.)(?<!\bTP\.)(?<!\bQ\.)(?<!\bP\.)\s+",
    re.IGNORECASE,
)


def clean_property_description(raw: str | None, max_chars: int = 1200) -> str | None:
    """Strip broker contact pitch and dividers from a crawled description.

    Filtering happens per sentence, because the contact line is sometimes its own
    paragraph and sometimes the last sentence of a real one.
    """
    if not raw:
        return raw

    kept_lines: list[str] = []
    for line in str(raw).splitlines():
        stripped = line.strip()
        if not stripped:
            kept_lines.append("")
            continue
        if _DIVIDER_LINE.match(stripped):
            continue
        # "***The Global City ..." is a real sentence wearing a decoration.
        stripped = re.sub(r"^[*=~_]{2,}\s*", "", stripped)
        sentences = [
            s
            for s in _SENTENCE_SPLIT.split(stripped)
            if not _JUNK_SENTENCE.search(s) and not _BROKER_NAME_ONLY.match(s.strip())
        ]
        rebuilt = " ".join(s.strip() for s in sentences if s.strip())
        if rebuilt:
            kept_lines.append(rebuilt)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(kept_lines)).strip()

    if len(text) > max_chars:
        window = text[:max_chars]
        # Prefer a sentence boundary so the excerpt does not stop mid-word.
        cut = max(window.rfind(". "), window.rfind("\n"), window.rfind("! "), window.rfind("? "))
        text = (window[: cut + 1] if cut > max_chars // 2 else window.rstrip()).rstrip() + "…"

    return text or None


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


def get_search_variations(text: str | None) -> list[str]:
    """Return common search patterns and spelling variations for Vietnamese locations."""
    if not text:
        return []
    clean = text.strip()
    # Remove prefix "phường", "xã", "quận", "huyện" for core name
    core = re.sub(r"^(?:phường|xã|quận|huyện|thành phố|thị trấn|tt\.?|p\.?|q\.?)\s+", "", clean, flags=re.IGNORECASE).strip()

    variations = {clean, core}

    # Generate old vs new tone placement variants (e.g. Yên Hòa vs Yên Hoà)
    tone_map = [
        ("oà", "òa"), ("oá", "óa"), ("oả", "ỏa"), ("oã", "õa"), ("oạ", "ọa"),
        ("uỳ", "ùy"), ("uý", "úy"), ("uỷ", "ủy"), ("uỹ", "ũy"), ("uỵ", "ụy"),
        ("oè", "òe"), ("oé", "óe"), ("oẻ", "ỏe"), ("oẽ", "õe"), ("oẹ", "ọe"),
    ]

    for term in list(variations):
        for v1, v2 in tone_map:
            if v1 in term:
                variations.add(term.replace(v1, v2))
            if v2 in term:
                variations.add(term.replace(v2, v1))

    return [v for v in variations if v]


def match_property_by_title(
    query: str,
    properties: list[dict[str, Any]],
) -> tuple[int | None, dict[str, Any] | None]:
    """Find the best matching property from a list given user query text."""
    if not query or not properties:
        return None, None

    def _normalize_str(s: str) -> str:
        import unicodedata
        normalized = unicodedata.normalize("NFD", s.lower())
        normalized = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        return normalized.replace("đ", "d").strip()

    q_norm = _normalize_str(query)
    best_idx = None
    best_prop = None
    max_score = 0

    for idx, prop in enumerate(properties):
        title = prop.get("title", "")
        t_norm = _normalize_str(title)
        code = _normalize_str(str(prop.get("code") or ""))

        # Direct property code match
        if code and len(code) >= 3 and re.search(rf"(?<!\w){re.escape(code)}(?!\w)", q_norm):
            return idx, prop

        # Direct title inclusion
        if t_norm and len(t_norm) >= 5 and t_norm in q_norm:
            return idx, prop

        # Keyword token overlap score
        noise = {
            "can", "ho", "chung", "cu", "nha", "ban", "mua", "cho", "toi",
            "dat", "lich", "xem", "tai", "phuong", "quan", "tp", "ha", "noi", "hcm",
        }
        location_tokens: set[str] = set()
        for field in ("address", "address_line", "ward", "district", "province"):
            location_tokens.update(re.findall(r"\w+", _normalize_str(str(prop.get(field) or ""))))

        # Structured location fields are search facts, not a distinctive
        # property name. Excluding them prevents location-only language from
        # silently selecting an arbitrary result in that district.
        tokens = [
            word
            for word in re.findall(r"\w+", t_norm)
            if (
                len(word) >= 2
                and word not in noise
                and word not in location_tokens
            )
        ]

        score = 0
        for i in range(len(tokens)):
            if tokens[i] in q_norm:
                score += 1
            if i + 1 < len(tokens):
                bigram = f"{tokens[i]} {tokens[i+1]}"
                if bigram in q_norm:
                    score += 3
            if i + 2 < len(tokens):
                trigram = f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}"
                if trigram in q_norm:
                    score += 6

        if score > max_score and score >= 3:
            max_score = score
            best_idx = idx
            best_prop = prop

    if best_prop:
        return best_idx, best_prop
    return None, None
