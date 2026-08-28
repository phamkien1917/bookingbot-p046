"""Supervisor (Conversation & Classification) Agent for LangGraph.

Classifies user intent and routes to specialized sub-agents with full multi-turn context.
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.agents.state import AgentState, AgentType, Intent
from src.services.affordability import (
    calculate_loan_schedule,
    estimate_affordability,
    explain_loan_calculation,
    format_vnd,
    purchase_guidance_lines,
)
from src.services.affordability import (
    explain as explain_affordability,
)
from src.services.chat_state_service import (
    LOCAL_TZ,
    extract_ordinal,
    is_affirmative,
    is_negative,
    normalize_text,
    parse_requested_date,
    parse_requested_hour,
)
from src.services.llm import get_llm
from src.services.search_criteria_service import extract_search_criteria, validate_search_criteria
from src.utils.property_text import match_property_by_title

logger = logging.getLogger(__name__)


class ExtractedCriteria(BaseModel):
    area_or_ward: str | None = Field(
        default=None,
        description="Phường/xã, khu đô thị, dự án, tên đường hoặc địa danh cụ thể (ví dụ: Xa La, Văn Quán, Yên Hòa, Nam Trung Yên, Văn Khê, Dịch Vọng, Mễ Trì, Trung Kính, Times City...)"
    )
    ward: str | None = None
    district: str | None = None
    province: str | None = None
    region: str | None = Field(
        default=None,
        description="Vùng miền nếu khách tìm theo vùng lớn: 'Miền Bắc', 'Miền Trung', hoặc 'Miền Nam'"
    )
    limit: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Số lượng nhà/căn khách yêu cầu cụ thể (ví dụ: tìm 2 nhà -> limit=2, 3 căn -> limit=3)"
    )
    property_kind: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    min_bedrooms: int | None = None
    max_bedrooms: int | None = None
    min_bathrooms: int | None = None
    min_area: float | None = None
    transaction_type: str | None = Field(default=None, description="SALE hoặc RENT")
    orientation: str | None = None
    legal_status: str | None = None
    furniture_status: str | None = None
    min_floor: int | None = None
    max_floor: int | None = None


class SupervisorUnderstanding(BaseModel):
    intent: str = Field(
        description="One of SEARCH_PROPERTY, SELECT_PROPERTY, PROPERTY_DETAILS, COMPARE_PROPERTIES, "
        "BOOK_APPOINTMENT, SELECT_SLOT, CHECK_STATUS, CANCEL_BOOKING, RESCHEDULE, CONFIRM, DENY, "
        "CONSULTATION_QA, GREETING, THANKS, GOODBYE, OUT_OF_SCOPE, FALLBACK"
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_new_search: bool = False
    criteria: ExtractedCriteria = Field(default_factory=ExtractedCriteria)
    soft_preferences: list[str] = Field(default_factory=list)
    household_context: list[str] = Field(default_factory=list)
    commute_landmark: str | None = None
    max_commute_minutes: int | None = None
    max_commute_km: float | None = None
    travel_mode: str | None = Field(default=None, description="DRIVE, WALK, BICYCLE, TRANSIT hoặc TWO_WHEELER")
    nearby_categories: list[str] = Field(default_factory=list)
    monthly_income_vnd: int | None = Field(
        default=None,
        description="Thu nhập hằng tháng khách tự nêu, quy về số VND (ví dụ '15-20 triệu/tháng' -> 17500000, "
        "lấy trung bình khi khách nói một khoảng). Chỉ điền khi khách thực sự nói về thu nhập của mình."
    )
    own_capital_vnd: int | None = Field(
        default=None,
        description="Số vốn tự có / tiền đang có sẵn khách nêu, quy về số VND (ví dụ 'em có sẵn 800 triệu' -> 800000000). "
        "Không suy đoán nếu khách không nói."
    )
    property_ordinal: int | None = None
    requested_date: str | None = None
    requested_hour: int | None = None
    booking_code: str | None = None
    direct_response: str | None = None


SUPERVISOR_SYSTEM_PROMPT = """Bạn là Supervisor AI điều phối cho hệ thống bất động sản và đặt lịch xem nhà chuyên nghiệp tại Việt Nam.

Nhiệm vụ của bạn:
1. Hiểu sâu sắc ý định (Intent) và ngữ cảnh của khách hàng qua lịch sử trò chuyện.
2. Trả lời trực diện, chính xác câu hỏi của khách hàng. KHÔNG tự ý suy diễn hoặc ép khách vào việc tìm kiếm nhà nếu khách chỉ đang hỏi thông tin tư vấn.
3. Trích xuất chính xác các thực thể khi khách thật sự có nhu cầu tìm BĐS (địa điểm, loại nhà, tầm giá VND, số phòng ngủ, ngày giờ, mã booking).
4. Phân loại chuẩn xác vào các Intent sau:

- SEARCH_PROPERTY: Khách THỰC SỰ muốn tìm BĐS mới hoặc tinh chỉnh tiêu chí (ví dụ: "tìm nhà 2 ngủ ở xa la hà đông", "tìm 2 căn hộ ở Thảo Điền Quận 2", "gợi ý 3 nhà ở Liên Chiểu Đà Nẵng", "tìm căn hộ 2PN dưới 5 tỷ", "lọc nhà có ban công", "xem thêm căn khác", "nhà trên 10 tỷ ở miền bắc").
  * SỐ LƯỢNG YÊU CẦU (limit): Nếu khách yêu cầu rõ số lượng nhà muốn tìm (ví dụ: "tìm 2 nhà", "gợi ý 3 căn", "lấy 1 căn", "top 3 căn"), trích xuất số lượng đó vào trường limit. Nếu khách không nói số lượng, để trống limit.
  * VÙNG MIỀN (region): Khi khách tìm theo vùng miền lớn ("Miền Bắc", "Miền Trung", "Miền Nam"), BẮT BUỘC trích xuất vào trường region (giá trị: "Miền Bắc", "Miền Trung", "Miền Nam"). KHÔNG gán "Miền Bắc" vào province hay area_or_ward.
  * ĐỊA ĐIỂM CHI TIẾT (area_or_ward): Khi khách nhắc đến bất kỳ phường/xã, khu đô thị, dự án, tên đường hay địa danh cụ thể trên toàn quốc (ví dụ:
    - Hà Nội: Xa La, Văn Quán, Yên Hòa, Nam Trung Yên, Văn Khê, Mỗ Lao, Trung Kính, Linh Đàm, Times City, Dịch Vọng, Mễ Trì...
    - TP. HCM: Thảo Điền, An Phú, Tân Quy, Phú Mỹ Hưng, Bến Nghé, Bến Thành, Hiệp Bình Chánh, Vinhomes Central Park...
    - Đà Nẵng: Mỹ An, Khuê Mỹ, Phước Mỹ, An Hải Bắc, Hòa Cường, Hòa Khánh, Nam Hòa Xuân...
    - Các tỉnh khác: Bãi Cháy (Hạ Long), Vĩnh Hải (Nha Trang), Dĩ An (Bình Dương)...),
    BẮT BUỘC trích xuất tên địa danh/phường đó vào trường area_or_ward (hoặc ward). KHÔNG đưa tên Tỉnh/Thành phố lớn (Hà Nội, TP.HCM...) vào area_or_ward.
  * QUẬN/HUYỆN/THÀNH PHỐ THUỘC TỈNH (district): Trích xuất vào trường district (ví dụ: "Quận Hà Đông", "Quận Cầu Giấy", "Quận 7", "Quận 2", "Quận Bình Thạnh", "Thành phố Thủ Đức", "Quận Liên Chiểu", "Quận Hải Châu", "Quận Sơn Trà", "Thành phố Nha Trang", "Thành phố Hạ Long"...).
  * TỈNH/THÀNH PHỐ (province): Trích xuất vào trường province (ví dụ: "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Khánh Hòa", "Quảng Ninh", "Bình Dương", "Bắc Ninh"...).
- SELECT_PROPERTY: Khách muốn chọn 1 căn cụ thể trong danh sách đã tìm (ví dụ: "chọn căn 1", "căn đầu tiên", "xem căn số 2", "căn Masteri").
- PROPERTY_DETAILS: Khách hỏi sâu về căn đang xem/đã chọn (ví dụ: "căn này có sổ chưa?", "giá bao nhiêu?", "diện tích thế nào?", "phí quản lý bao nhiêu?").
- COMPARE_PROPERTIES: CHỈ khi khách THỰC SỰ YÊU CẦU SO SÁNH (dùng từ "so sánh", "đối chiếu" hoặc "so sánh căn 1 và căn 2", "so sánh các căn này"). KHÔNG phân loại vào COMPARE_PROPERTIES khi khách chỉ hỏi tìm căn có đặc điểm cụ thể (ví dụ: "căn nào trên 2 phòng ngủ", "căn nào có ban công", "căn nào rẻ nhất", "căn nào gần trường"). Những câu đó là SEARCH_PROPERTY.
- BOOK_APPOINTMENT: Khách muốn đặt lịch hẹn xem nhà (ví dụ: "cho tôi xem căn này", "đặt lịch vào 14h thứ Bảy", "hẹn chiều mai", "chọn căn 1 và đặt lịch xem").
- Với câu phức hợp vừa chọn căn vừa đặt lịch (ví dụ: "Chọn căn 1, đặt lịch 14h thứ Bảy", "Chọn căn số 1, cho tôi hẹn xem chiều mai"): Intent PHẢI LÀ BOOK_APPOINTMENT, đồng thời đặt property_ordinal và trích xuất requested_date, requested_hour.
- SELECT_SLOT: Khách chọn khung giờ trong danh sách slot được đề xuất (ví dụ: "chọn slot 1", "khung giờ 2", "lúc 9h").
- CHECK_STATUS: Khách hỏi về lịch của mình (ví dụ: "lịch của tôi thế nào rồi?", "kiểm tra mã TR-12345").
- CANCEL_BOOKING: Khách muốn hủy lịch hẹn xem nhà.
- RESCHEDULE: Khách muốn đổi ngày/giờ lịch hẹn đã đặt.
- CONFIRM: Khách xác nhận, đồng ý ("xác nhận", "đồng ý", "tiếp tục", "được", "ok").
- DENY: Khách từ chối, hủy ("không", "thôi", "hủy thao tác").
- CONSULTATION_QA: Khách hỏi tư vấn kiến thức BĐS, pháp lý (sổ đỏ/sổ hồng, đặt cọc an toàn, công chứng, vi bằng), tài chính (vay ngân hàng, lãi suất, tỷ lệ vay), phong thủy, quy trình mua bán nhà đất, hoặc hỏi lời khuyên... Với intent này, hãy viết câu trả lời chuyên gia xuất sắc, tận tâm và giải đáp trực diện vào trường direct_response. KHÔNG tạo tiêu chí tìm kiếm giả.
- GREETING: Chào hỏi ("chào bạn", "hello Nera", "hi"). Viết câu chào thân thiện, giới thiệu bản thân là Nera - trợ lý BĐS vào direct_response.
- THANKS: Cảm ơn. Viết lời đáp lịch sự, tận tâm vào direct_response.
- GOODBYE: Tạm biệt. Viết lời chào tạm biệt vào direct_response.
- OUT_OF_SCOPE: Các câu hỏi hoàn toàn không liên quan đến BĐS, nhà đất, lịch hẹn (thời tiết, làm thơ, viết code, kể chuyện cười). ĐẶC BIỆT: Nếu khách yêu cầu tính khoảng cách đến một địa danh không thuộc Việt Nam (ví dụ: Tháp Tokyo, Tháp Eiffel, Rừng Amazon...), BẮT BUỘC phân loại vào OUT_OF_SCOPE và viết thẳng câu từ chối khéo (ví dụ: "Dạ Nera chỉ hỗ trợ tính khoảng cách trong lãnh thổ Việt Nam thôi ạ") vào direct_response. Viết phản hồi lịch sự, khéo léo từ chối và hướng về BĐS vào direct_response.

LƯU Ý QUAN TRỌNG:
- Chuẩn hóa tiền Việt: "5 tỷ" -> 5000000000, "15 triệu" -> 15000000, "khoảng 3 đến 5 tỷ" -> min_price=3000000000, max_price=5000000000.
- Ngày xem nhà: quy đổi các từ "hôm nay", "ngày mai", "thứ Bảy", "Chủ Nhật tuần sau" về định dạng YYYY-MM-DD dựa vào ngày hiện tại được cung cấp.
- Giữ vững ngữ cảnh hội thoại nhiều lượt. Nếu khách nói "căn đó", "căn này", đó là tham chiếu đến căn đang được chọn hoặc căn vừa thảo luận.
- Khi khách bắt đầu một nhu cầu mua/tìm mới chung chung (ví dụ: "t muốn mua 1 căn nhà ?", "tôi muốn mua nhà", "muốn tìm nhà", "cần mua nhà", "tìm nhà") mà KHÔNG nêu rõ địa điểm hay tầm giá trong câu hiện tại: BẮT BUỘC đặt is_new_search=true và ĐỂ TRỐNG TOÀN BỘ tiêu chí (criteria), KHÔNG tự ý copy tiêu chí cũ từ các lượt chat trước.
- Khi khách yêu cầu tiếp tục tìm kiếm theo nhu cầu cũ/sở thích đã lưu (ví dụ: "Tiếp tục tìm kiếm với nhu cầu cũ của tôi", "tiếp tục hành trình", "tìm theo nhu cầu cũ", "sở thích đã lưu"): Intent PHẢI LÀ SEARCH_PROPERTY, đặt is_new_search=false và kế thừa active_search_criteria từ context.
- Khi khách nêu THU NHẬP thay vì tầm giá (ví dụ: "tôi làm 15-20 triệu/tháng thì mua được căn nào", "lương em 25 củ"): điền monthly_income_vnd và ĐỂ TRỐNG max_price. Hệ thống sẽ tự tính tầm giá từ thu nhập; bạn KHÔNG được tự nhẩm ra con số ngân sách. Intent vẫn là SEARCH_PROPERTY nếu khách đang hỏi có căn nào phù hợp.
- Khi khách nêu VỐN TỰ CÓ (ví dụ: "em có sẵn 800 triệu", "tôi để dành được 1 tỷ"): điền own_capital_vnd. Vốn tự có khác thu nhập, đừng gộp làm một.
- Nếu khách vừa nêu thu nhập vừa nêu tầm giá cụ thể, giữ nguyên tầm giá khách nói và vẫn điền monthly_income_vnd.
"""


def _extract_booking_code(message: str) -> str | None:
    match = re.search(r"\b(BK[A-Z0-9-]{4,}|TR-[A-Z0-9-]{4,})\b", message.upper())
    return match.group(1) if match else None


def _extract_geo_constraints(message: str) -> dict[str, Any]:
    text = normalize_text(message)
    result: dict[str, Any] = {}
    if re.search(r"\b(di bo|walking)\b", text):
        result["travel_mode"] = "WALK"
    elif re.search(r"\b(xe may|motorbike|hai banh)\b", text):
        result["travel_mode"] = "TWO_WHEELER"
    elif re.search(r"\b(xe dap|bicycle)\b", text):
        result["travel_mode"] = "BICYCLE"
    elif re.search(r"\b(xe buyt|tau dien|cong cong|transit)\b", text):
        result["travel_mode"] = "TRANSIT"
    elif re.search(r"\b(lai xe|o to|di xe|driving)\b", text):
        result["travel_mode"] = "DRIVE"

    distance = re.search(r"(?:duoi|khong qua|toi da|trong vong)\s*(\d+(?:[.,]\d+)?)\s*km\b", text)
    if distance:
        result["max_commute_km"] = float(distance.group(1).replace(",", "."))
    duration = re.search(r"(?:duoi|khong qua|toi da|trong vong)\s*(\d+)\s*phut\b", text)
    if duration:
        result["max_commute_minutes"] = int(duration.group(1))

    categories = []
    for pattern, category in (
        (r"\b(truong hoc|truong cap|mam non)\b", "school"),
        (r"\b(benh vien|phong kham|y te)\b", "hospital"),
        (r"\b(dai hoc|cao dang)\b", "university"),
        (r"\b(sieu thi)\b", "supermarket"),
        (r"\b(cong vien)\b", "park"),
    ):
        if re.search(pattern, text):
            categories.append(category)
    if categories:
        result["nearby_categories"] = categories

    landmark = re.search(
        r"\bcach\s+(.+?)\s+(?:duoi|khong qua|toi da|trong vong)\s*\d+(?:[.,]\d+)?\s*(?:km|phut)\b",
        text,
    )
    if not landmark:
        landmark = re.search(
            r"\bcach\s+(.+?)\s+bao\s+nhieu\s*(?:km|phut)\b",
            text,
        )
    if landmark:
        candidate = landmark.group(1).strip(" ,.-")
        if candidate and candidate not in {"vi tri nay", "day", "do"}:
            result["commute_landmark"] = candidate
    return result


def _area_is_geo_target(area: str, geo: dict[str, Any]) -> bool:
    """Keep route destinations and POI categories out of inventory address filters."""
    normalized_area = normalize_text(area).strip()
    landmark = normalize_text(str(geo.get("commute_landmark") or "")).strip()
    if landmark and (
        normalized_area == landmark
        or normalized_area in landmark
        or landmark in normalized_area
    ):
        return True

    category_terms = {
        "hospital": ("benh vien", "phong kham", "y te"),
        "school": ("truong hoc", "truong cap", "mam non"),
        "university": ("dai hoc", "cao dang"),
        "supermarket": ("sieu thi",),
        "park": ("cong vien",),
    }
    return any(
        term in normalized_area
        for category in geo.get("nearby_categories", [])
        for term in category_terms.get(category, ())
    )


def _is_generic_geo_category_landmark(value: str | None) -> bool:
    """Reject generic POI labels as route destinations; Places handles them."""
    if not value:
        return False
    remainder = normalize_text(value)
    for term in (
        "truong hoc",
        "truong cap",
        "mam non",
        "benh vien",
        "phong kham",
        "y te",
        "dai hoc",
        "cao dang",
        "sieu thi",
        "cong vien",
    ):
        remainder = remainder.replace(term, " ")
    remainder = re.sub(r"\b(?:gan|va|hoac|cac|khu vuc|xung quanh)\b", " ", remainder)
    return not remainder.strip(" ,.-")


async def supervisor_node(state: AgentState) -> dict[str, Any]:
    """Supervisor node: runs LLM understanding on full conversation context."""
    started = time.perf_counter()
    query = state.get("query", "").strip()
    history = state.get("messages", [])
    now = datetime.now(LOCAL_TZ)

    # Fast deterministic pre-checks
    det_criteria, det_groups = extract_search_criteria(query)
    det_geo = _extract_geo_constraints(query)
    booking_code = _extract_booking_code(query)
    norm_query = normalize_text(query)

    # Format recent history for LLM
    recent_turns = []
    for msg in history[-8:]:
        role = msg.get("role", "user")
        content = str(msg.get("content", ""))
        if content:
            recent_turns.append(f"{role.upper()}: {content}")

    context_payload = {
        "today": now.date().isoformat(),
        "current_time": now.strftime("%H:%M"),
        "timezone": "Asia/Ho_Chi_Minh",
        "phase": state.get("phase", "IDLE"),
        "active_search_criteria": state.get("search_criteria", {}),
        "soft_preferences": state.get("soft_preferences", []),
        "household_context": state.get("household_context", []),
        "selected_property_id": state.get("current_property_id"),
        "property_count_in_memory": len(state.get("selected_properties", [])),
        "slot_count_in_memory": len(state.get("selected_slots", [])),
        "active_request_id": state.get("active_request_id"),
        "active_request_code": state.get("active_request_code"),
        "pending_action": state.get("pending_action"),
        "customer_authenticated": state.get("customer_authenticated", False),
        "memory_summary": state.get("memory_summary", ""),
        "recent_conversation": recent_turns,
        "user_message": query,
    }

    understanding: SupervisorUnderstanding | None = None
    ai_model = "gpt-4o-mini"

    has_property_context = bool(state.get("search_results") or state.get("selected_properties"))
    consultation_question_signal = bool(re.search(
        r"\b(can chuan bi|quy trinh|an toan|can kiem tra|truoc khi ky|"
        r"uu diem|nhuoc diem|rui ro|nen vay|vay them bao nhieu|thu tuc|phap ly)\b",
        norm_query,
    )) and not bool(det_geo)
    if re.fullmatch(r"\s*(xin chao|chao|hello|hi)(?:\s+nera)?[!.?]*\s*", norm_query):
        understanding = SupervisorUnderstanding(
            intent=Intent.GREETING,
            confidence=1.0,
            direct_response=(
                "Chào bạn! Mình là Nera. Bạn có thể cho mình khu vực, ngân sách hoặc loại nhà "
                "đang quan tâm để mình tìm ngay nhé."
            ),
        )
    elif re.search(r"\b(cam on|thanks|thank you)\b", norm_query):
        understanding = SupervisorUnderstanding(
            intent=Intent.THANKS,
            confidence=1.0,
            direct_response="Rất vui được hỗ trợ bạn. Khi cần tìm hoặc đặt lịch xem nhà, cứ nhắn Nera nhé!",
        )
    elif re.search(r"\b(tam biet|bye)\b", norm_query):
        understanding = SupervisorUnderstanding(
            intent=Intent.GOODBYE,
            confidence=1.0,
            direct_response="Chào bạn nhé! Khi cần tìm nhà hoặc xem lại lịch hẹn, Nera luôn sẵn sàng hỗ trợ.",
        )
    elif has_property_context and re.search(
        r"\b(chon|lay|xem)\s+(?:can|nha)(?:\s+so|\s+thu)?\s*\d+\b",
        norm_query,
    ):
        understanding = SupervisorUnderstanding(intent=Intent.SELECT_PROPERTY, confidence=1.0)
    elif has_property_context and re.search(
        r"\b(so sanh|doi chieu|lap bang so sanh)\b",
        norm_query,
    ):
        understanding = SupervisorUnderstanding(intent=Intent.COMPARE_PROPERTIES, confidence=1.0)
    elif consultation_question_signal:
        understanding = SupervisorUnderstanding(intent=Intent.CONSULTATION_QA, confidence=1.0)
    elif state.get("current_property_id") and det_geo and re.search(
        r"\b(can nay|nha nay|bat dong san nay)\b",
        norm_query,
    ):
        understanding = SupervisorUnderstanding(intent=Intent.PROPERTY_DETAILS, confidence=1.0)

    preserve_search_signal = bool(re.search(
        r"\b(giu nguyen|van vay|nhu vay|nhu cu|giu nhu cu|ngan sach cu|tieu chi cu)\b",
        norm_query,
    ))
    remove_filter_signal = bool(re.search(
        r"\b(bo|xoa|khong can|khong gioi han)\b.*\b(gia|ngan sach|phong ngu|dien tich|huong|tang)\b",
        norm_query,
    ))
    pagination_signal = bool(re.search(
        r"\b(tim them|xem them|can khac|nha khac|cai khac|doi can khac)\b",
        norm_query,
    ))
    reset_search_signal = bool(re.search(
        r"\b(nhu cau moi|bat dau (?:mot )?nhu cau moi|tim kiem moi)\b",
        norm_query,
    ))
    property_feature_followup = bool(
        (state.get("search_results") or state.get("selected_properties"))
        and re.search(
            r"\b(trong so do|can nao|nha nao|re nhat|dat nhat|co ban cong|co cho de xe|phap ly)\b",
            norm_query,
        )
    )


    if understanding is None:
        try:
            llm = get_llm()
            structured_llm = llm._create_chat_model().with_structured_output(
                SupervisorUnderstanding,
                method="json_schema",
                strict=True,
            )
            sys_msg = SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)
            human_msg = HumanMessage(content=json.dumps(context_payload, ensure_ascii=False))

            result = await structured_llm.ainvoke([sys_msg, human_msg])
            if isinstance(result, SupervisorUnderstanding):
                understanding = result
        except Exception as e:
            logger.warning(f"Structured supervisor understanding failed: {e}. Falling back to heuristic.")

    # Fallback heuristic if LLM failed
    if understanding is None:
        inferred_intent = Intent.FALLBACK
        if is_affirmative(query):
            inferred_intent = Intent.CONFIRM
        elif is_negative(query):
            inferred_intent = Intent.DENY
        elif re.search(r"\b(chao|xin chao|hello|hi)\b", norm_query):
            inferred_intent = Intent.GREETING
        elif re.search(r"\b(cam on|thanks|thank you)\b", norm_query):
            inferred_intent = Intent.THANKS
        elif re.search(r"\b(tam biet|bye)\b", norm_query):
            inferred_intent = Intent.GOODBYE
        elif re.search(r"\b(huy|huy lich)\b", norm_query):
            inferred_intent = Intent.CANCEL_BOOKING
        elif re.search(r"\b(doi lich|doi ngay|chuyen lich|doi gio)\b", norm_query):
            inferred_intent = Intent.RESCHEDULE
        elif re.search(r"\b(kiem tra lich|trang thai|lich cua toi)\b", norm_query) or booking_code:
            inferred_intent = Intent.CHECK_STATUS
        elif re.search(r"\b(dat lich|xem nha|hen xem)\b", norm_query):
            inferred_intent = Intent.BOOK_APPOINTMENT
        elif re.search(r"\b(so sanh)\b", norm_query):
            is_concept_comparison = bool(re.search(
                r"\b(huong\s*(?:dong|tay|nam|bac|dong nam|dong bac|tay nam|tay bac)|chung cu\s*(?:va|voi|hay)\s*nha|so do\s*(?:va|voi)\s*so hong|mua\s*(?:va|voi|hay)\s*thue|lai suat\s*(?:co dinh|tha noi))\b",
                norm_query,
            ))
            if is_concept_comparison and not re.search(r"\b(can 1|can 2|can so|can nay|cac can)\b", norm_query):
                inferred_intent = Intent.CONSULTATION_QA
            else:
                inferred_intent = Intent.COMPARE_PROPERTIES
        elif det_criteria or re.search(r"\b(tim|can ho|chung cu|nha|biet thu|dat nen)\b", norm_query):
            inferred_intent = Intent.SEARCH_PROPERTY

        understanding = SupervisorUnderstanding(
            intent=inferred_intent,
            confidence=0.8,
            booking_code=booking_code,
            criteria=ExtractedCriteria(**{
                key: value
                for key, value in det_criteria.items()
                if key in ExtractedCriteria.model_fields
            }),
        )

    # Reconcile deterministic explicit criteria with LLM criteria
    merged_criteria = dict(state.get("search_criteria", {}))
    is_resume_signal = bool(re.search(
        r"\b(nhu cau cu|so thich da luu|tiep tuc tim|nhu lan truoc|nhu cu|tim lai|theo tieu chi cu|tiep tuc hanh trinh|tiep tuc tim kiem)\b",
        norm_query,
    )) or bool(state.get("is_resume_search"))
    explicit_new_search_signal = reset_search_signal
    refinement_signal = (
        not explicit_new_search_signal
        and bool(state.get("search_criteria"))
        and bool(re.search(
            r"\b(doi|chuyen|thay|them|chi|bo|xoa|giu nguyen|van vay|neu|uu tien|loc|khong .+ nua)\b"
            r"|\b(?:noi|nang|tang|giam)\s+(?:ngan sach|gia|muc gia)\b",
            norm_query,
        ))
    )
    starts_new_search_signal = (
        not is_resume_signal
        and not refinement_signal
        and bool(re.search(r"\b(tim|tim kiem|can mua|muon mua|can tim|muon tim)\b", norm_query))
        and not bool(re.search(r"\b(tim them|xem them|can khac|cai khac|khac ko|khac khong|doi can khac)\b", norm_query))
    )
    llm_dict = understanding.criteria.model_dump(exclude_none=True)
    if is_resume_signal:
        understanding.is_new_search = False
        understanding.intent = Intent.SEARCH_PROPERTY
    elif refinement_signal:
        understanding.is_new_search = False
    elif understanding.is_new_search:
        merged_criteria = {}
        understanding.is_new_search = True
        if "location" not in det_groups:
            llm_dict.pop("region", None)
            llm_dict.pop("district", None)
            llm_dict.pop("province", None)
            llm_dict.pop("area_or_ward", None)
            llm_dict.pop("ward", None)
        if "budget" not in det_groups:
            llm_dict.pop("min_price", None)
            llm_dict.pop("max_price", None)
        if "property_kind" not in det_criteria:
            llm_dict.pop("property_kind", None)

    # Apply deterministic parser overrides for location / budget / kind if explicit
    if "location" in det_groups:
        merged_criteria.pop("region", None)
        merged_criteria.pop("district", None)
        merged_criteria.pop("province", None)
        merged_criteria.pop("area_or_ward", None)
        merged_criteria.pop("ward", None)
        if "region" in det_criteria:
            merged_criteria["region"] = det_criteria["region"]
        if "district" in det_criteria:
            merged_criteria["district"] = det_criteria["district"]
        if "province" in det_criteria:
            merged_criteria["province"] = det_criteria["province"]
    elif "region" in llm_dict or "district" in llm_dict or "province" in llm_dict:
        if "region" in llm_dict:
            merged_criteria.pop("district", None)
            merged_criteria.pop("province", None)
            merged_criteria["region"] = llm_dict["region"]
        if "district" in llm_dict:
            merged_criteria["district"] = llm_dict["district"]
        if "province" in llm_dict:
            merged_criteria["province"] = llm_dict["province"]

    if "quantity" in det_groups:
        merged_criteria.pop("limit", None)
        if "limit" in det_criteria:
            merged_criteria["limit"] = det_criteria["limit"]
    elif "limit" in llm_dict:
        merged_criteria["limit"] = llm_dict["limit"]
    elif understanding.is_new_search:
        merged_criteria.pop("limit", None)

    area_val = llm_dict.get("area_or_ward") or llm_dict.get("ward")
    if area_val and not _area_is_geo_target(str(area_val), det_geo):
        norm_area = normalize_text(area_val)
        norm_dist = normalize_text(merged_criteria.get("district") or "")
        norm_prov = normalize_text(merged_criteria.get("province") or "")
        norm_reg = normalize_text(merged_criteria.get("region") or "")
        if norm_area not in (norm_dist, norm_prov, norm_reg, "ha noi", "ho chi minh", "da nang", "mien bac", "mien trung", "mien nam"):
            merged_criteria["area_or_ward"] = area_val
            merged_criteria["ward"] = area_val
        else:
            merged_criteria.pop("area_or_ward", None)
            merged_criteria.pop("ward", None)
    elif understanding.is_new_search or "location" in det_groups or det_geo:
        merged_criteria.pop("area_or_ward", None)
        merged_criteria.pop("ward", None)

    if "budget" in det_groups:
        merged_criteria.pop("min_price", None)
        merged_criteria.pop("max_price", None)
        if "min_price" in det_criteria:
            merged_criteria["min_price"] = det_criteria["min_price"]
        if "max_price" in det_criteria:
            merged_criteria["max_price"] = det_criteria["max_price"]
    elif "min_price" in llm_dict or "max_price" in llm_dict:
        if "min_price" in llm_dict:
            merged_criteria["min_price"] = llm_dict["min_price"]
        if "max_price" in llm_dict:
            merged_criteria["max_price"] = llm_dict["max_price"]

    if "property_kind" in det_criteria:
        merged_criteria["property_kind"] = det_criteria["property_kind"]
    elif "property_kind" in llm_dict:
        merged_criteria["property_kind"] = llm_dict["property_kind"]

    bedroom_replacement = bool(re.search(
        r"\b(doi|chuyen|thay)(?:\s+thanh|\s+sang)?\b|\bchi can\b",
        norm_query,
    ))
    if bedroom_replacement and (
        "min_bedrooms" in det_criteria or "max_bedrooms" in det_criteria
    ):
        merged_criteria.pop("min_bedrooms", None)
        merged_criteria.pop("max_bedrooms", None)

    for field in ("min_bedrooms", "max_bedrooms", "min_bathrooms", "min_area"):
        if field in det_criteria:
            merged_criteria[field] = det_criteria[field]
        elif field in llm_dict:
            merged_criteria[field] = llm_dict[field]

    if re.search(
        r"\b(?:bo|xoa|khong can|khong gioi han)(?:\s+gioi han)?\s+(?:gia|ngan sach)\b",
        norm_query,
    ):
        merged_criteria.pop("min_price", None)
        merged_criteria.pop("max_price", None)
        merged_criteria.pop("target_price", None)

    # These are strict inventory constraints. Only explicit deterministic
    # extraction may add/replace them; model inference must not fabricate one.
    for field in (
        "transaction_type", "orientation", "legal_status", "furniture_status",
    ):
        if field in det_criteria:
            merged_criteria[field] = det_criteria[field]
        elif understanding.is_new_search:
            merged_criteria.pop(field, None)

    if "min_floor" in det_criteria or "max_floor" in det_criteria:
        merged_criteria.pop("min_floor", None)
        merged_criteria.pop("max_floor", None)
        if "min_floor" in det_criteria:
            merged_criteria["min_floor"] = det_criteria["min_floor"]
        if "max_floor" in det_criteria:
            merged_criteria["max_floor"] = det_criteria["max_floor"]
    elif understanding.is_new_search:
        merged_criteria.pop("min_floor", None)
        merged_criteria.pop("max_floor", None)

    # Income -> price ceiling. The model reports the income figure the customer
    # said; every number derived from it is computed in affordability.py, because
    # a budget the model guessed wrong sends someone to view homes they cannot buy.
    monthly_income = understanding.monthly_income_vnd or state.get("monthly_income_vnd")
    own_capital = understanding.own_capital_vnd or state.get("own_capital_vnd")
    affordability_note = None
    if monthly_income:
        estimate = estimate_affordability(monthly_income, own_capital_vnd=own_capital)
        if estimate:
            affordability_note = explain_affordability(estimate)
            # An explicit budget from the customer always wins over a derived one.
            if not merged_criteria.get("max_price"):
                merged_criteria["max_price"] = estimate.assumed_price_vnd

    # Target date / hour resolution
    target_date = parse_requested_date(query)
    invalid_requested_date = bool(re.search(
        r"\b(?:mot )?ngay (?:o |trong )?qua khu\b|\bngay da qua\b",
        normalize_text(query),
    ))
    if not target_date and understanding.requested_date:
        try:
            target_date = datetime.strptime(understanding.requested_date, "%Y-%m-%d").date()
        except ValueError:
            target_date = None

    target_hour = parse_requested_hour(query) or understanding.requested_hour

    # Ordinal & Property Name resolution
    property_pool = state.get("search_results") or state.get("selected_properties", [])
    prop_count = len(property_pool)
    slot_count = len(state.get("selected_slots", []))
    ordinal = extract_ordinal(query, maximum=max(prop_count, slot_count, 10))
    if ordinal is None and understanding.property_ordinal:
        ordinal = understanding.property_ordinal - 1

    matched_prop_id = None
    if ordinal is None and state.get("phase") != "AWAITING_SLOT":
        search_pool = state.get("search_results") or state.get("selected_properties") or []
        matched_idx, matched_prop = match_property_by_title(query, search_pool)
        if matched_prop:
            ordinal = matched_idx
            matched_prop_id = str(matched_prop["id"])

    # Soft preferences & household context accumulation
    soft_prefs = list(state.get("soft_preferences", []))
    for item in understanding.soft_preferences:
        if item and item not in soft_prefs:
            soft_prefs.append(item)

    household_ctx = list(state.get("household_context", []))
    for item in understanding.household_context:
        if item and item not in household_ctx:
            household_ctx.append(item)

    # Route determination
    intent = understanding.intent
    criteria_correction = bool(re.search(
        r"\b(doi sang|chuyen sang|khong phai|khong thue nua|nhu cau moi|bat dau nhu cau moi)\b",
        norm_query,
    ))
    if (det_criteria or det_geo) and (starts_new_search_signal or criteria_correction):
        intent = Intent.SEARCH_PROPERTY

    asks_current_location = bool(re.search(
        r"\b(vi tri (?:hien tai|cua toi|nay)|noi toi dang o|gan day)\b",
        normalize_text(query),
    )) or bool(re.search(r"\bchỗ tôi\b", query.lower()))
    if asks_current_location and not state.get("user_location"):
        intent = Intent.FALLBACK
        understanding.direct_response = (
            "Mình chưa nhận được quyền vị trí. Bạn có thể bật quyền vị trí cho trang này và hỏi lại, "
            "hoặc nhập một địa danh cụ thể (ví dụ: ‘cách Bệnh viện Bạch Mai dưới 5 km đi xe’)."
        )

    # Time-sensitive finance data routed to CONSULTATION_QA
    if re.search(
        r"\b(lai suat|interest rate)\b.*\b(hien tai|hom nay|bay gio|moi nhat|current)\b",
        normalize_text(query),
    ):
        intent = Intent.CONSULTATION_QA
        understanding.direct_response = (
            "Mình không có nguồn lãi suất ngân hàng theo thời gian thực và có ngày cập nhật để xác minh, "
            "nên không nên đưa ra một con số hiện tại như dữ liệu chắc chắn. Bạn hãy kiểm tra bảng lãi suất "
            "chính thức của ngân hàng dự định vay; nếu cung cấp mức lãi suất, thời hạn và khoản vay, Nera có thể "
            "tính phương án trả góp cho bạn."
        )

    # General real estate concept comparison (orientations, legal, house types) routed to CONSULTATION_QA
    if re.search(r"\b(so sanh|khac nhau|khac gi|uu nhuoc diem)\b", norm_query) and re.search(
        r"\b(huong\s*(?:dong|tay|nam|bac|dong nam|dong bac|tay nam|tay bac)|chung cu\s*(?:va|voi|hay)\s*nha|so do\s*(?:va|voi)\s*so hong|mua\s*(?:va|voi|hay)\s*thue|lai suat\s*(?:co dinh|tha noi))\b",
        norm_query,
    ) and not re.search(r"\b(can 1|can 2|can so|can nay|cac can|can ho nay)\b", norm_query):
        intent = Intent.CONSULTATION_QA

    # Monthly income affordability guidance
    income_match = re.search(
        r"\b(lam|thu nhap|luong|kiem duoc)\b\s*(\d+(?:[.,]\d+)?)\s*(?:-|den|toi)?\s*(\d+(?:[.,]\d+)?)?\s*(?:trieu|tr)\s*(?:/|\s*moi\s*|\s*hang\s*)thang\b",
        normalize_text(query),
    )
    if income_match and not re.search(r"\b(mua|thue|ban|dat lich|xem nha|hen xem)\b", normalize_text(query)):
        intent = Intent.CONSULTATION_QA
        district_val = det_criteria.get("district") or ("Cầu Giấy" if "cau giay" in normalize_text(query) else "khu vực bạn quan tâm")
        low_val = income_match.group(2)
        high_val = income_match.group(3) or low_val
        income_range_str = f"{low_val} – {high_val} triệu/tháng" if low_val != high_val else f"{low_val} triệu/tháng"

        # Calculate rental budget range (~25% to 35% of income)
        income_mid_vnd = None
        try:
            low_f = float(low_val.replace(",", "."))
            high_f = float(high_val.replace(",", "."))
            rent_low = max(3, round(low_f * 0.25))
            rent_high = max(rent_low + 1, round(high_f * 0.35))
            rent_range_str = f"{rent_low} – {rent_high} triệu/tháng"
            income_mid_vnd = int(round((low_f + high_f) / 2 * 1_000_000))
        except Exception:
            rent_range_str = "4 – 7 triệu/tháng"

        purchase_estimate = (
            estimate_affordability(income_mid_vnd, own_capital_vnd=own_capital)
            if income_mid_vnd
            else None
        )
        if purchase_estimate:
            buy_lines = purchase_guidance_lines(purchase_estimate)
        else:
            buy_lines = (
                "- Bạn cho Nera biết con số thu nhập cụ thể hơn để tính khoản vay và tầm giá phù hợp nhé.\n"
            )

        affordability_note = (
            f"Phân tích tài chính cho mức thu nhập {income_range_str} tại {district_val}:\n"
            f"- Ngân sách thuê an toàn (25%–35% thu nhập): {rent_range_str}\n"
            f"- Phương án mua căn hộ:\n{buy_lines}"
        )

    # Loan amortization calculation request parser (e.g. "vay 2 tỷ trong 3 năm, lãi 5%, thu nhập 50tr")
    loan_match = re.search(
        r"\b(?:vay|khoan vay|tinh lai|tinh vay|vay von)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)\b",
        normalize_text(query),
    )
    if loan_match and not re.search(r"\b(dat lich|hen xem|xem nha|mua nha o|thue nha o)\b", normalize_text(query)):
        intent = Intent.CONSULTATION_QA
        loan_val_raw = float(loan_match.group(1).replace(",", "."))
        loan_unit = loan_match.group(2)
        loan_amount_vnd = int(round(loan_val_raw * (1_000_000_000 if loan_unit in {"ty", "ti"} else 1_000_000)))

        # Term extraction (years or months)
        term_years = None
        term_match = re.search(r"(\d+)\s*(?:nam|year)", normalize_text(query))
        if term_match:
            term_years = float(term_match.group(1))
        else:
            month_match = re.search(r"(\d+)\s*(?:thang|month)", normalize_text(query))
            if month_match:
                term_years = float(month_match.group(1)) / 12

        # Interest rate extraction
        annual_rate = 0.08
        rate_match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:%|phan tram)", normalize_text(query))
        if rate_match:
            annual_rate = float(rate_match.group(1).replace(",", ".")) / 100.0

        # Income extraction
        income_val = None
        income_m = re.search(
            r"(?:thu nhap|luong|kiem duoc)\s*(?:cua toi|la)?\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)",
            normalize_text(query),
        )
        if income_m:
            income_num = float(income_m.group(1).replace(",", "."))
            income_unit = income_m.group(2)
            income_val = int(round(income_num * (1_000_000_000 if income_unit in {"ty", "ti"} else 1_000_000)))
        elif monthly_income:
            income_val = monthly_income

        schedule = calculate_loan_schedule(
            loan_amount_vnd,
            term_years=term_years or 15,
            annual_rate=annual_rate,
            monthly_income_vnd=income_val,
        )
        if schedule:
            affordability_note = explain_loan_calculation(schedule)
            merged_criteria.clear()  # Clear accidental property filters

    # Financial feasibility inquiry (e.g. "tôi có tài chính 3 triệu muốn mua nhà tầm 3 tỷ được không")
    feasibility_match = re.search(
        r"\b(?:tai chinh|thu nhap|von|tiet kiem|co)\s*(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)\b.*\b(?:mua|nham|nham mua)\b.*\b(\d+(?:[.,]\d+)?)\s*(ty|ti|trieu|tr)\b",
        normalize_text(query),
    )
    if feasibility_match and re.search(r"\b(duoc|duoc khong|co duoc|co the|on khong|hop ly|kha thi|nen khong)\b", normalize_text(query)):
        intent = Intent.CONSULTATION_QA
        current_agent = AgentType.RESPOND
        merged_criteria.clear()

        cap_val = float(feasibility_match.group(1).replace(",", "."))
        cap_unit = feasibility_match.group(2)
        cap_vnd = int(round(cap_val * (1_000_000_000 if cap_unit in {"ty", "ti"} else 1_000_000)))

        prop_val = float(feasibility_match.group(3).replace(",", "."))
        prop_unit = feasibility_match.group(4)
        prop_vnd = int(round(prop_val * (1_000_000_000 if prop_unit in {"ty", "ti"} else 1_000_000)))

        down_payment_vnd = int(round(prop_vnd * 0.3))
        loan_vnd = prop_vnd - down_payment_vnd

        # Monthly payment estimate for 20 years at 9%
        r_month = 0.09 / 12
        n_months = 240
        monthly_payment = int(round(loan_vnd * (r_month * (1 + r_month)**n_months) / ((1 + r_month)**n_months - 1)))
        min_safe_income = int(round(monthly_payment / 0.4))

        understanding.direct_response = (
            f"Với mức tài chính / thu nhập **{format_vnd(cap_vnd)}**, bạn **chưa đủ điều kiện tài chính để mua nhà tầm {format_vnd(prop_vnd)}** ở thời điểm hiện tại.\n\n"
            f"📊 **Bài toán tài chính để mua căn nhà {format_vnd(prop_vnd)}:**\n"
            f"- **Vốn tự có ban đầu (tối thiểu 30%):** Cần khoảng **{format_vnd(down_payment_vnd)}** để thanh toán đợt đầu.\n"
            f"- **Khoản vay ngân hàng (70% ~ {format_vnd(loan_vnd)}):** Vay trong 20 năm (lãi suất ~9%/năm), mỗi tháng bạn cần trả góp cả gốc và lãi khoảng **{format_vnd(monthly_payment)}/tháng**.\n"
            f"- **Thu nhập an toàn (DTI ≤ 40%):** Thu nhập hàng tháng của bạn hoặc gia đình cần đạt từ **{format_vnd(min_safe_income)}/tháng** trở lên để vừa trả nợ vừa đảm bảo sinh hoạt.\n\n"
            f"💡 **Lời khuyên từ Nera:**\n"
            f"- Với tài chính {format_vnd(cap_vnd)}/tháng, phương án phù hợp nhất hiện tại là **thuê căn hộ/phòng trọ** trong tầm giá 1 – 2 triệu/tháng và tích lũy thêm vốn.\n"
            f"- Khi vốn tự có đạt từ 30% trở lên, Nera sẽ hỗ trợ bạn lập phương án vay chi tiết để mua nhà nhé!"
        )

    # Promote compound intent (selecting a property AND requesting booking)
    norm_query = normalize_text(query)
    if asks_current_location and not state.get("user_location"):
        pass
    elif (
        re.search(r"\b(dat lich|xem nha|hen xem|tham quan|xem vao|dat ngay)\b", norm_query)
        or (target_date and "xem" in norm_query)
    ) and intent not in (Intent.CANCEL_BOOKING, Intent.RESCHEDULE, Intent.CHECK_STATUS):
        intent = Intent.BOOK_APPOINTMENT
    elif state.get("current_property_id") and intent not in (
        Intent.BOOK_APPOINTMENT,
        Intent.COMPARE_PROPERTIES,
        Intent.SEARCH_PROPERTY,
        Intent.SELECT_PROPERTY,
    ):
        if re.search(r"\b(can nay|nha nay|can dang xem|can hien tai|review|danh gia|chi tiet|thong tin|phap ly|gia bao nhieu|dien tich|phong ngu|huong gi|co ban cong|co cho de xe)\b", norm_query):
            intent = Intent.PROPERTY_DETAILS
    elif re.search(r"\b(tiep tuc hanh trinh|nhu cau cu|so thich da luu|tiep tuc tim kiem)\b", norm_query):
        intent = Intent.SEARCH_PROPERTY
    elif re.search(r"\b(thay doi nhu cau|doi nhu cau|nhu cau moi|xoa tieu chi|muon thay doi)\b", norm_query):
        intent = Intent.SEARCH_PROPERTY
        if not det_criteria and not det_geo:
            merged_criteria = {}

    if re.search(r"\b(ban co the giup gi|ban giup duoc gi|co the lam gi|chuc nang cua ban)\b", norm_query):
        intent = Intent.GREETING
        understanding.direct_response = (
            "Mình có thể giúp bạn tìm bất động sản theo khu vực, ngân sách và nhu cầu; "
            "so sánh các căn, kiểm tra thông tin chi tiết và hỗ trợ đặt lịch xem nhà. "
            "Bạn muốn bắt đầu bằng khu vực hay khoảng giá nào?"
        )
    elif (
        re.search(r"\b(can nao tot nhat|nha nao tot nhat|nen chon can nao)\b", norm_query)
        and not property_pool
    ):
        intent = Intent.FALLBACK
        understanding.direct_response = (
            "Mình chưa có danh sách hoặc tiêu chí để xác định căn nào tốt nhất. "
            "Bạn hãy cho mình biết nhu cầu, khu vực và ngân sách; hoặc yêu cầu tìm một "
            "danh sách trước, rồi mình sẽ so sánh minh bạch cho bạn."
        )

    # Force SEARCH_PROPERTY if user asks about distance or nearby amenities but intent fell into GREETING/FALLBACK
    if intent in (Intent.GREETING, Intent.FALLBACK) and not understanding.direct_response:
        if det_geo.get("commute_landmark") or det_geo.get("nearby_categories"):
            if state.get("search_results") or state.get("selected_properties") or state.get("current_property_id"):
                intent = Intent.SEARCH_PROPERTY
                understanding.intent = intent

    current_agent = AgentType.RESPOND

    if intent in (Intent.SEARCH_PROPERTY, Intent.SELECT_PROPERTY, Intent.PROPERTY_DETAILS, Intent.COMPARE_PROPERTIES):
        current_agent = AgentType.INVENTORY
    elif intent in (
        Intent.BOOK_APPOINTMENT,
        Intent.SELECT_SLOT,
        Intent.CHECK_STATUS,
        Intent.CANCEL_BOOKING,
        Intent.RESCHEDULE,
    ):
        current_agent = AgentType.BOOKING
    elif intent in (Intent.CONFIRM, Intent.DENY):
        phase = state.get("phase")
        if phase in ("AWAITING_CANCEL_CONFIRMATION", "AWAITING_AUTH", "AWAITING_SLOT", "AWAITING_DATE"):
            current_agent = AgentType.BOOKING
        elif intent == Intent.CONFIRM and (state.get("current_property_id") or state.get("selected_properties") or matched_prop_id):
            current_agent = AgentType.BOOKING
            intent = Intent.BOOK_APPOINTMENT
        else:
            current_agent = AgentType.RESPOND
    else:
        current_agent = AgentType.RESPOND

    validation_errors = validate_search_criteria(merged_criteria)
    if validation_errors and intent == Intent.SEARCH_PROPERTY:
        current_agent = AgentType.RESPOND
        intent = Intent.FALLBACK
        is_low_sale_budget = any("dưới 100 triệu" in err for err in validation_errors)
        if is_low_sale_budget:
            low_price = merged_criteria.get("max_price", 3_000_000)
            understanding.direct_response = (
                f"Mức giá **{format_vnd(low_price)}** thường là chi phí dành cho việc **thuê căn hộ / phòng trọ hằng tháng**, "
                f"vì trên thị trường hiện tại không có bất động sản mở bán với mức giá này.\n\n"
                f"💡 **Bạn đang muốn:**\n"
                f"- **Tìm thuê căn hộ** với ngân sách khoảng {format_vnd(low_price)}/tháng?\n"
                f"- Hay bạn dự định **tìm mua căn hộ** khoảng **{format_vnd(low_price * 1000)}**?"
            )
        else:
            understanding.direct_response = (
                "Mình chưa thể tìm chính xác vì " + ", ".join(validation_errors) + ". "
                "Bạn vui lòng xác nhận lại khoảng tiêu chí mong muốn nhé."
            )

    # If currently in AWAITING_SLOT and customer provides ordinal -> route to BOOKING
    if state.get("phase") == "AWAITING_SLOT" and (ordinal is not None or intent == Intent.SELECT_SLOT):
        current_agent = AgentType.BOOKING
        intent = Intent.SELECT_SLOT

    latency_ms = round((time.perf_counter() - started) * 1000)

    llm_landmark = understanding.commute_landmark
    if not state.get("user_location") and normalize_text(llm_landmark or "") == "vi tri cua ban":
        llm_landmark = None
    if (
        det_geo.get("nearby_categories")
        and not det_geo.get("commute_landmark")
        and _is_generic_geo_category_landmark(llm_landmark)
    ):
        llm_landmark = None

    # For general CONSULTATION_QA (without explicit affordability direct response),
    # let respond_node generate the complete, rich real estate consultation.
    direct_resp = understanding.direct_response
    if intent == Intent.CONSULTATION_QA and not affordability_note and direct_resp and ("căn nhà" in direct_resp or "thông tin" in direct_resp):
        direct_resp = None

    nearby_categories = det_geo.get("nearby_categories") or understanding.nearby_categories
    if nearby_categories and state.get("nearby_categories") and re.search(r"\b(them|va)\b", norm_query):
        nearby_categories = list(dict.fromkeys([
            *state.get("nearby_categories", []),
            *nearby_categories,
        ]))
    elif not nearby_categories:
        nearby_categories = [] if understanding.is_new_search else state.get("nearby_categories", [])

    # Construct state updates
    updates: dict[str, Any] = {
        "current_agent": current_agent,
        "intent": intent,
        "confidence": understanding.confidence,
        "direct_response": direct_resp,
        "search_criteria": merged_criteria,
        "soft_preferences": soft_prefs,
        "household_context": household_ctx,
        "commute_landmark": ("Vị trí của bạn" if state.get("user_location") else None) or det_geo.get("commute_landmark") or llm_landmark or (None if understanding.is_new_search else state.get("commute_landmark")),
        "max_commute_minutes": det_geo.get("max_commute_minutes") or understanding.max_commute_minutes or (None if understanding.is_new_search else state.get("max_commute_minutes")),
        "max_commute_km": det_geo.get("max_commute_km") or understanding.max_commute_km or (None if understanding.is_new_search else state.get("max_commute_km")),
        "travel_mode": det_geo.get("travel_mode") or understanding.travel_mode or ("DRIVE" if understanding.is_new_search else state.get("travel_mode", "DRIVE")),
        "nearby_categories": nearby_categories,
        "invalid_requested_date": invalid_requested_date,
        "monthly_income_vnd": monthly_income,
        "own_capital_vnd": own_capital,
        "affordability_note": affordability_note,
        "ai_model": ai_model,
        "ai_latency_ms": state.get("ai_latency_ms", 0) + latency_ms,
    }

    if target_date:
        updates["requested_date"] = target_date.isoformat()
    if target_hour is not None:
        updates["requested_hour"] = target_hour
    if booking_code:
        updates["active_request_code"] = booking_code

    # Direct UUID property extraction from query (e.g. "Đặt lịch xem căn <id>")
    uuid_match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", query, re.IGNORECASE)
    if uuid_match:
        updates["current_property_id"] = uuid_match.group(1).lower()
    elif matched_prop_id:
        updates["current_property_id"] = matched_prop_id
        updates["selected_property_index"] = ordinal
    elif ordinal is not None:
        if state.get("phase") == "AWAITING_SLOT":
            updates["selected_slot_index"] = ordinal
        else:
            updates["selected_property_index"] = ordinal
            props = property_pool
            if 0 <= ordinal < len(props):
                updates["current_property_id"] = str(props[ordinal].get("id"))

    return updates


def route_from_supervisor(state: AgentState) -> str:
    """Routing function from supervisor to workers."""
    return state.get("current_agent", AgentType.RESPOND)
