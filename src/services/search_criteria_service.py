"""Deterministic search criteria parsing outside the AI agent package.

This keeps web/API personalization concerns separate from the agent graph,
which is maintained independently by another team member.
"""

import re
import unicodedata


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower())
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return normalized.replace("đ", "d")


def _vnd_amount(value: str, unit: str) -> int:
    amount = float(value.replace(",", "."))
    multiplier = 1_000_000_000 if unit.lower() in {"ty", "ti"} else 1_000_000
    return round(amount * multiplier)


def extract_search_criteria(message: str) -> tuple[dict, set[str]]:
    """Return explicit filters and filter groups mentioned by the user."""
    text = _normalize(message)
    criteria: dict = {}
    groups: set[str] = set()

    price_range = re.search(
        r"(?:tu|khoang)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)\s*(?:den|-|toi)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)",
        text,
    )
    if price_range:
        low_value, low_unit, high_value, high_unit = price_range.groups()
        criteria["min_price"] = _vnd_amount(low_value, low_unit)
        criteria["max_price"] = _vnd_amount(high_value, high_unit)
        groups.add("budget")
    else:
        minimum = re.search(r"(?:tren|tu|toi thieu|it nhat|>=)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)", text)
        maximum = re.search(r"(?:duoi|toi da|nhieu nhat|<=)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)", text)
        if minimum:
            criteria.update(min_price=_vnd_amount(*minimum.groups()), max_price=None)
            groups.add("budget")
        elif maximum:
            criteria.update(min_price=None, max_price=_vnd_amount(*maximum.groups()))
            groups.add("budget")

    bedrooms = re.search(r"(\d+)\s*(?:phong ngu|pn|ngu)", text)
    if bedrooms:
        criteria["min_bedrooms"] = int(bedrooms.group(1))

    area = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:m2|met vuong)", text)
    if area:
        criteria["min_area"] = float(area.group(1).replace(",", "."))

    if re.search(r"ha\s*noi", text):
        criteria["province"] = "Hà Nội"
        groups.add("location")
    elif re.search(r"ho\s*chi\s*minh|tphcm|sai\s*gon", text):
        criteria["province"] = "Hồ Chí Minh"
        groups.add("location")

    district = re.search(
        r"\bquan\s+(\d+|ba dinh|hoan kiem|tay ho|long bien|cau giay|dong da|hai ba trung|hoang mai|thanh xuan|nam tu liem|bac tu liem|ha dong|go vap|binh thanh|tan binh|phu nhuan|thu duc)\b",
        text,
    )
    if district:
        criteria["district"] = f"Quận {district.group(1).title()}"
        groups.add("location")

    if re.search(r"\b(can ho|chung cu|ccmn)\b", text):
        criteria["property_kind"] = "APARTMENT"
    elif re.search(r"\b(biet thu|villa)\b", text):
        criteria["property_kind"] = "VILLA"
    elif re.search(r"\b(dat|dat nen)\b", text):
        criteria["property_kind"] = "LAND"

    return criteria, groups


def build_search_criteria(message: str, memory: dict | None) -> dict:
    """Merge memory with the current request, with explicit input winning."""
    allowed = {
        "district", "province", "property_kind", "min_price", "max_price",
        "min_bedrooms", "min_bathrooms", "min_area",
    }
    merged = {
        key: value
        for key, value in (memory or {}).items()
        if key in allowed and value not in (None, "")
    }
    current, groups = extract_search_criteria(message)

    if "budget" in groups:
        merged.pop("min_price", None)
        merged.pop("max_price", None)
    if "location" in groups:
        merged.pop("district", None)
        merged.pop("province", None)

    merged.update(current)
    return merged
