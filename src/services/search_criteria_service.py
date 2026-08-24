"""Deterministic search criteria parsing outside the AI agent package.

This keeps web/API personalization concerns separate from the agent graph,
which is maintained independently by another team member.
"""

import re
import unicodedata

DISTRICT_NAMES = {
    # Hà Nội
    "ba dinh": "Quận Ba Đình",
    "hoan kiem": "Quận Hoàn Kiếm",
    "tay ho": "Quận Tây Hồ",
    "long bien": "Quận Long Biên",
    "cau giay": "Quận Cầu Giấy",
    "dong da": "Quận Đống Đa",
    "hai ba trung": "Quận Hai Bà Trưng",
    "hoang mai": "Quận Hoàng Mai",
    "thanh xuan": "Quận Thanh Xuân",
    "nam tu liem": "Quận Nam Từ Liêm",
    "bac tu liem": "Quận Bắc Từ Liêm",
    "ha dong": "Quận Hà Đông",
    "gia lam": "Huyện Gia Lâm",
    "dong anh": "Huyện Đông Anh",
    "thanh tri": "Huyện Thanh Trì",
    "dan phuong": "Huyện Đan Phượng",
    "hoai duc": "Huyện Hoài Đức",
    "thuong tin": "Huyện Thường Tín",
    "me linh": "Huyện Mê Linh",
    "soc son": "Huyện Sóc Sơn",
    "son tay": "Thị xã Sơn Tây",

    # TP. Hồ Chí Minh
    "binh thanh": "Quận Bình Thạnh",
    "go vap": "Quận Gò Vấp",
    "tan binh": "Quận Tân Bình",
    "tan phu": "Quận Tân Phú",
    "phu nhuan": "Quận Phú Nhuận",
    "binh tan": "Quận Bình Tân",
    "thu duc": "Thành phố Thủ Đức",
    "binh chanh": "Huyện Bình Chánh",
    "can gio": "Huyện Cần Giờ",
    "hoc mon": "Huyện Hóc Môn",
    "cu chi": "Huyện Củ Chi",
    "nha be": "Huyện Nhà Bè",

    # Đà Nẵng
    "hai chau": "Quận Hải Châu",
    "son tra": "Quận Sơn Trà",
    "ngu hanh son": "Quận Ngũ Hành Sơn",
    "lien chieu": "Quận Liên Chiểu",
    "cam le": "Quận Cẩm Lệ",
    "thanh khe": "Quận Thanh Khê",
    "hoa vang": "Huyện Hòa Vang",

    # Khánh Hòa / Quảng Ninh / Bình Dương / Bắc Ninh / Hưng Yên / Long An
    "nha trang": "Thành phố Nha Trang",
    "ha long": "Thành phố Hạ Long",
    "thuan an": "Thành phố Thuận An",
    "di an": "Thành phố Dĩ An",
    "thu dau mot": "Thành phố Thủ Dầu Một",
    "tu son": "Thành phố Từ Sơn",
    "van giang": "Huyện Văn Giang",
    "ben luc": "Huyện Bến Lức",
    "duc hoa": "Huyện Đức Hòa",
    "thanh hoa": "Thành phố Thanh Hóa",
}


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
        maximum = re.search(
            r"(?:duoi|toi da|nhieu nhat|khong qua|<=|ngan sach(?: la)?|tam|len)\s*"
            r"(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)",
            text,
        )
        if minimum:
            criteria["min_price"] = _vnd_amount(*minimum.groups())
            groups.add("budget")
        elif maximum:
            criteria["max_price"] = _vnd_amount(*maximum.groups())
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
    elif re.search(r"da\s*nang", text):
        criteria["province"] = "Đà Nẵng"
        groups.add("location")
    elif re.search(r"khanh\s*hoa|nha\s*trang", text):
        criteria["province"] = "Khánh Hòa"
        groups.add("location")
    elif re.search(r"quang\s*ninh|ha\s*long", text):
        criteria["province"] = "Quảng Ninh"
        groups.add("location")
    elif re.search(r"binh\s*duong", text):
        criteria["province"] = "Bình Dương"
        groups.add("location")
    elif re.search(r"bac\s*ninh", text):
        criteria["province"] = "Bắc Ninh"
        groups.add("location")
    elif re.search(r"hung\s*yen", text):
        criteria["province"] = "Hưng Yên"
        groups.add("location")
    elif re.search(r"long\s*an", text):
        criteria["province"] = "Long An"
        groups.add("location")
    elif re.search(r"thanh\s*hoa", text):
        criteria["province"] = "Thanh Hóa"
        groups.add("location")

    named_districts = "|".join(
        re.escape(name) for name in sorted(DISTRICT_NAMES, key=len, reverse=True)
    )
    district = re.search(rf"\b(?:quan|huyen|thanh pho|tp\.?|tx\.?)\s+({named_districts})\b|\b({named_districts})\b", text)
    numbered_district = re.search(r"\b(?:quan|q\.?)\s*(\d+)\b", text)
    if district:
        dist_name = district.group(1) or district.group(2)
        criteria["district"] = DISTRICT_NAMES[dist_name]
        groups.add("location")
    elif numbered_district:
        criteria["district"] = f"Quận {numbered_district.group(1)}"
        groups.add("location")

    if re.search(r"\b(can ho|chung cu|ccmn)\b", text):
        criteria["property_kind"] = "APARTMENT"
    elif re.search(r"\b(biet thu|villa)\b", text):
        criteria["property_kind"] = "VILLA"
    elif (
        re.search(r"\bđất(?:\s+nền)?\b", message.lower())
        or re.search(r"\b(dat nen|lo dat|mua dat|tim dat|can dat)\b", text)
    ):
        criteria["property_kind"] = "LAND"
    elif re.search(r"\b(nha pho|lien ke|townhouse)\b", text):
        criteria["property_kind"] = "TOWNHOUSE"
    elif re.search(r"\b(shophouse|mat bang|thuong mai)\b", text):
        criteria["property_kind"] = "COMMERCIAL"
    elif re.search(r"\b(nha rieng|nha nguyen can)\b", text):
        criteria["property_kind"] = "HOUSE"

    return criteria, groups


def build_search_criteria(message: str, memory: dict | None) -> dict:
    """Merge memory with the current request, with explicit input winning."""
    allowed = {
        "area_or_ward", "ward", "district", "province", "property_kind", "min_price", "max_price",
        "min_bedrooms", "min_bathrooms", "min_area",
    }
    current, groups = extract_search_criteria(message)
    text = _normalize(message)
    starts_new_search = (
        bool(re.search(r"\b(tim|tim kiem|mua)\b", text))
        and not bool(re.search(r"\btim them\b", text))
        and bool(current)
    )
    merged = {} if starts_new_search else {
        key: value
        for key, value in (memory or {}).items()
        if key in allowed and value not in (None, "")
    }

    if "budget" in groups:
        merged.pop("min_price", None)
        merged.pop("max_price", None)
    if "location" in groups:
        merged.pop("area_or_ward", None)
        merged.pop("ward", None)
        merged.pop("district", None)
        merged.pop("province", None)

    merged.update(current)
    return merged
