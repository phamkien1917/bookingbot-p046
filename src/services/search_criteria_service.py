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

REGION_PROVINCES: dict[str, list[str]] = {
    "Miền Bắc": [
        "Hà Nội", "Hải Phòng", "Quảng Ninh", "Bắc Ninh", "Hưng Yên", "Bắc Giang",
        "Vĩnh Phúc", "Hải Dương", "Nam Định", "Thái Bình", "Ninh Bình", "Hà Nam",
        "Thái Nguyên", "Phú Thọ", "Lạng Sơn", "Tuyên Quang", "Yên Bái", "Lào Cai",
        "Sơn La", "Hòa Bình", "Điện Biên", "Lai Châu", "Cao Bằng", "Bắc Kạn", "Hà Giang",
    ],
    "Miền Trung": [
        "Đà Nẵng", "Khánh Hòa", "Thanh Hóa", "Nghệ An", "Hà Tĩnh", "Quảng Bình",
        "Quảng Trị", "Thừa Thiên Huế", "Quảng Nam", "Quảng Ngãi", "Bình Định",
        "Phú Yên", "Ninh Thuận", "Bình Thuận", "Kon Tum", "Gia Lai", "Đắk Lắk",
        "Đắk Nông", "Lâm Đồng",
    ],
    "Miền Nam": [
        "Hồ Chí Minh", "Bình Dương", "Đồng Nai", "Long An", "Bà Rịa - Vũng Tàu",
        "Tây Ninh", "Bình Phước", "Cần Thơ", "Tiền Giang", "Bến Tre", "Trà Vinh",
        "Vĩnh Long", "Đồng Tháp", "An Giang", "Kiên Giang", "Hậu Giang", "Sóc Trăng",
        "Bạc Liêu", "Cà Mau",
    ],
}


_WORD_NUMS = {
    "mot": 1, "hai": 2, "ba": 3, "bon": 4, "nam": 5,
    "sau": 6, "bay": 7, "tam": 8, "chin": 9, "muoi": 10,
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

    # Loan calculations or interest inquiries without explicit house search intent
    # must not pollute search criteria with loan amounts or year counts.
    norm_orig = message.lower()
    is_loan_inquiry = (
        bool(re.search(r"\b(vay von|vay tien|vay ngan hang|khoan vay|tinh lai|tinh phuong an vay|tinh lai vay|lai suat vay|cho vay)\b", text))
        or (bool(re.search(r"\bvay\s+\d+", text)) and not bool(re.search(r"\b(?:vay|vậy)\s+(?:thi|noi|tang|giam|doi|chuyen|chon|ha|nang)\b", norm_orig)))
    ) and not bool(re.search(r"\b(tim|can mua|muon mua|thue nha|tim can ho|tim nha|bat dong san|bds)\b", text))
    if is_loan_inquiry:
        return criteria, groups

    sale_signal = re.search(
        r"\b(mua|can mua|muon mua|ban nha|ban can ho|nha ban|dang ban|rao ban)\b",
        text,
    )
    rent_signal = re.search(r"\b(thue|can thue|muon thue|cho thue)\b", text)
    cancels_rent = re.search(r"\b(khong thue nua|thoi thue|bo thue|chuyen (?:sang )?mua)\b", text)
    if sale_signal and (not rent_signal or cancels_rent):
        criteria["transaction_type"] = "SALE"
        groups.add("transaction")
    elif rent_signal:
        criteria["transaction_type"] = "RENT"
        groups.add("transaction")

    # Requested quantity / limit detection
    num_qty = re.search(
        r"\b(?:tim|goi y|cho|lay|chon|xem|can|muon|top)?\s*(\d+)\s*(?:can ho|can nha|can|nha|bat dong san|bds|biet thu|villa|lo dat)\b(?!\s*(?:phong|pn|ngu|tang|ty|ti|trieu|tr|m2|m|met|tieng|gio|thang|nam))",
        text,
    )
    word_qty = re.search(
        r"\b(?:tim|goi y|cho|lay|chon|xem|can|muon)?\s*(mot|hai|ba|bon|nam|sau|bay|tam|chin|muoi)\s*(?:can ho|can nha|can|nha|bat dong san|bds|biet thu|villa|lo dat)\b(?!\s*(?:phong|pn|ngu|tang|ty|ti|trieu|tr|m2|m|met|tieng|gio|thang|nam))",
        text,
    )
    top_qty = re.search(r"\btop\s*(\d+)\b", text)

    if num_qty:
        qty_val = int(num_qty.group(1))
        if 1 <= qty_val <= 50:
            criteria["limit"] = qty_val
            groups.add("quantity")
    elif word_qty:
        criteria["limit"] = _WORD_NUMS[word_qty.group(1)]
        groups.add("quantity")
    elif top_qty:
        criteria["limit"] = int(top_qty.group(1))
        groups.add("quantity")

    price_range = re.search(
        r"(?:tu|khoang)\s*(\d+(?:[.,]\d+)?)\s*(?:(ty|ti|trieu|tr)\s*)?"
        r"(?:den|-|toi)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)",
        text,
    )
    if price_range:
        low_value, low_unit, high_value, high_unit = price_range.groups()
        criteria["min_price"] = _vnd_amount(low_value, low_unit or high_unit)
        criteria["max_price"] = _vnd_amount(high_value, high_unit)
        groups.add("budget")
    else:
        minimum = re.search(r"(?:tren|tu|toi thieu|it nhat|>=)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)", text)
        maximum = re.search(
            r"(?:duoi|toi da|nhieu nhat|khong qua|<=|ngan sach(?: la)?|tam|len|noi len|tang len)\s*"
            r"(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)",
            text,
        )
        if minimum:
            criteria["min_price"] = _vnd_amount(*minimum.groups())
            groups.add("budget")
        if maximum:
            criteria["max_price"] = _vnd_amount(*maximum.groups())
            groups.add("budget")
        if not minimum and not maximum:
            bare_price = re.search(r"\b(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)\b", text)
            if bare_price and not re.search(rf"\b(?:tang|pn|phong|nam|thang|m2|met)\s*{bare_price.group(1)}\b", text):
                criteria["max_price"] = _vnd_amount(*bare_price.groups())
                groups.add("budget")

    bedrooms = re.search(r"(\d+)\s*(?:phong ngu|pn|ngu)", text)
    if bedrooms:
        bed_count = int(bedrooms.group(1))
        is_exact = bool(re.search(r"\b(chi|chi lay|dung|chinh xac|loai|can)\b", text))
        is_min_explicit = bool(re.search(
            r"(?:tu|it nhat|toi thieu|tren|>=)\s*" + str(bed_count) + r"\s*(?:phong ngu|pn|ngu)"
            r"|" + str(bed_count) + r"\s*(?:phong ngu|pn|ngu)\s*(?:tro len|\+)",
            text,
        ))
        is_max_explicit = bool(re.search(
            r"(?:duoi|toi da|nhieu nhat|khong qua|<=)\s*" + str(bed_count) + r"\s*(?:phong ngu|pn|ngu)",
            text,
        ))
        if is_max_explicit:
            criteria["max_bedrooms"] = bed_count
        elif is_min_explicit:
            criteria["min_bedrooms"] = bed_count
        elif is_exact or bed_count == 1:
            criteria["min_bedrooms"] = bed_count
            criteria["max_bedrooms"] = bed_count
        else:
            criteria["min_bedrooms"] = bed_count

    area = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:m2|met vuong)", text)
    if area:
        criteria["min_area"] = float(area.group(1).replace(",", "."))

    orientation = re.search(
        r"\bhuong\s+(dong nam|dong bac|tay nam|tay bac|dong|tay|nam|bac)\b",
        text,
    )
    if orientation:
        orientation_labels = {
            "dong nam": "Đông Nam", "dong bac": "Đông Bắc",
            "tay nam": "Tây Nam", "tay bac": "Tây Bắc",
            "dong": "Đông", "tay": "Tây", "nam": "Nam", "bac": "Bắc",
        }
        criteria["orientation"] = orientation_labels[orientation.group(1)]

    floor_range = re.search(r"(?:tu|khoang)\s*tang\s*(\d+)\s*(?:den|-|toi)\s*tang?\s*(\d+)", text)
    floor_min = re.search(r"(?:tu|tren|it nhat|toi thieu)\s*tang\s*(\d+)|tang\s*(\d+)\s*tro len", text)
    floor_max = re.search(r"(?:duoi|toi da|khong qua)\s*tang\s*(\d+)|tang\s*(\d+)\s*tro xuong", text)
    floor_exact = re.search(r"\b(?:o|tai|can)\s*tang\s*(\d+)\b|\btang\s*(\d+)\b", text)
    if floor_range:
        criteria["min_floor"] = int(floor_range.group(1))
        criteria["max_floor"] = int(floor_range.group(2))
    else:
        if floor_min:
            criteria["min_floor"] = int(floor_min.group(1) or floor_min.group(2))
        if floor_max:
            criteria["max_floor"] = int(floor_max.group(1) or floor_max.group(2))
        if not floor_min and not floor_max and floor_exact:
            value = int(floor_exact.group(1) or floor_exact.group(2))
            criteria["min_floor"] = value
            criteria["max_floor"] = value

    legal_match = re.search(r"\b(so hong rieng|so hong|so do|hop dong mua ban|hdmb|vi bang)\b", text)
    if legal_match:
        legal_labels = {
            "so hong rieng": "Sổ hồng riêng", "so hong": "Sổ hồng",
            "so do": "Sổ đỏ", "hop dong mua ban": "Hợp đồng mua bán",
            "hdmb": "Hợp đồng mua bán", "vi bang": "Vi bằng",
        }
        criteria["legal_status"] = legal_labels[legal_match.group(1)]

    if re.search(r"\b(noi that day du|full noi that)\b", text):
        criteria["furniture_status"] = "Nội thất đầy đủ"
    elif re.search(r"\b(noi that cao cap)\b", text):
        criteria["furniture_status"] = "Nội thất cao cấp"
    elif re.search(r"\b(hoan thien co ban|noi that co ban)\b", text):
        criteria["furniture_status"] = "Hoàn thiện cơ bản"

    # Region detection
    if re.search(r"\b(mien bac|phia bac|bac bo)\b", text):
        criteria["region"] = "Miền Bắc"
        groups.add("location")
    elif re.search(r"\b(mien trung|phia trung|trung bo)\b", text):
        criteria["region"] = "Miền Trung"
        groups.add("location")
    elif re.search(r"\b(mien nam|phia nam|nam bo)\b", text):
        criteria["region"] = "Miền Nam"
        groups.add("location")

    if re.search(r"ha\s*noi", text):
        criteria["province"] = "Hà Nội"
        groups.add("location")
    elif re.search(r"ho\s*chi\s*minh|tp\s*\.?\s*hcm|tphcm|sai\s*gon", text):
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
        "limit", "region", "area_or_ward", "ward", "district", "province", "property_kind", "min_price", "max_price",
        "min_bedrooms", "max_bedrooms", "min_bathrooms", "min_area",
        "transaction_type", "orientation", "legal_status", "furniture_status",
        "min_floor", "max_floor",
    }
    current, groups = extract_search_criteria(message)
    text = _normalize(message)
    starts_new_search = (
        bool(re.search(
            r"\b(tim|tim kiem|can mua|muon mua|can thue|muon thue|can tim|muon tim)\b",
            text,
        ))
        and not bool(re.search(r"\b(tim them|xem them|can khac|cai khac|khac ko|khac khong|doi can khac)\b", text))
    )
    merged = {} if starts_new_search else {
        key: value
        for key, value in (memory or {}).items()
        if key in allowed and value not in (None, "")
    }

    if "quantity" in groups:
        merged.pop("limit", None)
    if "budget" in groups:
        merged.pop("min_price", None)
        merged.pop("max_price", None)
    if "min_bedrooms" in current or "max_bedrooms" in current:
        merged.pop("min_bedrooms", None)
        merged.pop("max_bedrooms", None)
    if "min_floor" in current or "max_floor" in current:
        merged.pop("min_floor", None)
        merged.pop("max_floor", None)
    if "location" in groups:
        merged.pop("region", None)
        merged.pop("area_or_ward", None)
        merged.pop("ward", None)
        merged.pop("district", None)
        merged.pop("province", None)
    if "transaction" in groups:
        merged.pop("transaction_type", None)

    merged.update(current)
    return merged


def validate_search_criteria(criteria: dict) -> list[str]:
    """Return contradictions so the agent can ask instead of guessing."""
    errors: list[str] = []
    if criteria.get("min_price") is not None and criteria.get("max_price") is not None:
        if criteria["min_price"] > criteria["max_price"]:
            errors.append("mức giá tối thiểu đang lớn hơn mức giá tối đa")
    if criteria.get("min_bedrooms") is not None and criteria.get("max_bedrooms") is not None:
        if criteria["min_bedrooms"] > criteria["max_bedrooms"]:
            errors.append("số phòng ngủ tối thiểu đang lớn hơn số tối đa")
    if criteria.get("min_floor") is not None and criteria.get("max_floor") is not None:
        if criteria["min_floor"] > criteria["max_floor"]:
            errors.append("tầng tối thiểu đang lớn hơn tầng tối đa")
    if criteria.get("transaction_type") == "SALE" and criteria.get("max_price") is not None:
        if criteria["max_price"] < 100_000_000:
            errors.append("ngân sách mua nhà dưới 100 triệu đồng chưa phù hợp với thị trường mở bán (mức giá này thường là ngân sách thuê hằng tháng hoặc gõ nhầm)")
    return errors
