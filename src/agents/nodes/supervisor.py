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
from src.services.search_criteria_service import extract_search_criteria
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
- OUT_OF_SCOPE: Các câu hỏi hoàn toàn không liên quan đến BĐS, nhà đất, lịch hẹn (thời tiết, làm thơ, viết code, kể chuyện cười). Viết phản hồi lịch sự, khéo léo từ chối và hướng về BĐS vào direct_response.

LƯU Ý QUAN TRỌNG:
- Chuẩn hóa tiền Việt: "5 tỷ" -> 5000000000, "15 triệu" -> 15000000, "khoảng 3 đến 5 tỷ" -> min_price=3000000000, max_price=5000000000.
- Ngày xem nhà: quy đổi các từ "hôm nay", "ngày mai", "thứ Bảy", "Chủ Nhật tuần sau" về định dạng YYYY-MM-DD dựa vào ngày hiện tại được cung cấp.
- Giữ vững ngữ cảnh hội thoại nhiều lượt. Nếu khách nói "căn đó", "căn này", đó là tham chiếu đến căn đang được chọn hoặc căn vừa thảo luận.
- Khi khách bắt đầu một nhu cầu mua/tìm mới chung chung (ví dụ: "t muốn mua 1 căn nhà ?", "tôi muốn mua nhà", "muốn tìm nhà", "cần mua nhà", "tìm nhà") mà KHÔNG nêu rõ địa điểm hay tầm giá trong câu hiện tại: BẮT BUỘC đặt is_new_search=true và ĐỂ TRỐNG TOÀN BỘ tiêu chí (criteria), KHÔNG tự ý copy tiêu chí cũ từ các lượt chat trước.
- Khi khách yêu cầu tiếp tục tìm kiếm theo nhu cầu cũ/sở thích đã lưu (ví dụ: "Tiếp tục tìm kiếm với nhu cầu cũ của tôi", "tiếp tục hành trình", "tìm theo nhu cầu cũ", "sở thích đã lưu"): Intent PHẢI LÀ SEARCH_PROPERTY, đặt is_new_search=false và kế thừa active_search_criteria từ context.
"""


def _extract_booking_code(message: str) -> str | None:
    match = re.search(r"\b(BK[A-Z0-9-]{4,}|TR-[A-Z0-9-]{4,})\b", message.upper())
    return match.group(1) if match else None


async def supervisor_node(state: AgentState) -> dict[str, Any]:
    """Supervisor node: runs LLM understanding on full conversation context."""
    started = time.perf_counter()
    query = state.get("query", "").strip()
    history = state.get("messages", [])
    now = datetime.now(LOCAL_TZ)

    # Fast deterministic pre-checks
    det_criteria, det_groups = extract_search_criteria(query)
    booking_code = _extract_booking_code(query)

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
        norm_query = normalize_text(query)
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
            inferred_intent = Intent.COMPARE_PROPERTIES
        elif det_criteria or re.search(r"\b(tim|can ho|chung cu|nha|biet thu|dat nen)\b", norm_query):
            inferred_intent = Intent.SEARCH_PROPERTY

        understanding = SupervisorUnderstanding(
            intent=inferred_intent,
            confidence=0.8,
            booking_code=booking_code,
            criteria=ExtractedCriteria(
                region=det_criteria.get("region"),
                limit=det_criteria.get("limit"),
                ward=None,
                district=det_criteria.get("district"),
                province=det_criteria.get("province"),
                property_kind=det_criteria.get("property_kind"),
                min_price=det_criteria.get("min_price"),
                max_price=det_criteria.get("max_price"),
                min_bedrooms=det_criteria.get("min_bedrooms"),
                max_bedrooms=det_criteria.get("max_bedrooms"),
                min_area=det_criteria.get("min_area"),
            ),
        )

    # Reconcile deterministic explicit criteria with LLM criteria
    merged_criteria = dict(state.get("search_criteria", {}))
    norm_query = normalize_text(query)
    is_resume_signal = bool(re.search(
        r"\b(nhu cau cu|so thich da luu|tiep tuc tim|nhu lan truoc|nhu cu|tim lai|theo tieu chi cu|tiep tuc hanh trinh|tiep tuc tim kiem)\b",
        norm_query,
    )) or bool(state.get("is_resume_search"))
    starts_new_search_signal = (
        not is_resume_signal
        and bool(re.search(r"\b(tim|tim kiem|mua|can mua|muon mua|can tim|muon tim)\b", norm_query))
        and not bool(re.search(r"\b(tim them|xem them|can khac|cai khac|khac ko|khac khong|doi can khac)\b", norm_query))
    )
    llm_dict = understanding.criteria.model_dump(exclude_none=True)
    if is_resume_signal:
        understanding.is_new_search = False
        understanding.intent = Intent.SEARCH_PROPERTY
    elif understanding.is_new_search or starts_new_search_signal:
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
    if area_val:
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
    elif understanding.is_new_search or "location" in det_groups:
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

    for field in ("min_bedrooms", "max_bedrooms", "min_bathrooms", "min_area"):
        if field in det_criteria:
            merged_criteria[field] = det_criteria[field]
        elif field in llm_dict:
            merged_criteria[field] = llm_dict[field]

    # Target date / hour resolution
    target_date = parse_requested_date(query)
    if not target_date and understanding.requested_date:
        try:
            target_date = datetime.strptime(understanding.requested_date, "%Y-%m-%d").date()
        except ValueError:
            target_date = None

    target_hour = parse_requested_hour(query) or understanding.requested_hour

    # Ordinal & Property Name resolution
    prop_count = len(state.get("selected_properties", []))
    slot_count = len(state.get("selected_slots", []))
    ordinal = extract_ordinal(query, maximum=max(prop_count, slot_count, 10))
    if ordinal is None and understanding.property_ordinal:
        ordinal = understanding.property_ordinal - 1

    matched_prop_id = None
    if ordinal is None and state.get("phase") != "AWAITING_SLOT":
        search_pool = state.get("selected_properties") or state.get("search_results") or []
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

    # Promote compound intent (selecting a property AND requesting booking)
    norm_query = normalize_text(query)
    if (
        re.search(r"\b(dat lich|xem nha|hen xem|tham quan|xem vao|dat ngay)\b", norm_query)
        or (target_date and "xem" in norm_query)
    ) and intent not in (Intent.CANCEL_BOOKING, Intent.RESCHEDULE, Intent.CHECK_STATUS):
        intent = Intent.BOOK_APPOINTMENT
    elif state.get("current_property_id") and intent != Intent.BOOK_APPOINTMENT:
        if re.search(r"\b(can nay|nha nay|can dang xem|can hien tai|review|danh gia|chi tiet|thong tin|phap ly|gia bao nhieu|dien tich|phong ngu|huong gi|co ban cong|co cho de xe)\b", norm_query):
            intent = Intent.PROPERTY_DETAILS
    elif re.search(r"\b(tiep tuc hanh trinh|nhu cau cu|so thich da luu|tiep tuc tim kiem)\b", norm_query):
        intent = Intent.SEARCH_PROPERTY
    elif re.search(r"\b(thay doi nhu cau|doi nhu cau|nhu cau moi|xoa tieu chi|muon thay doi)\b", norm_query):
        intent = Intent.SEARCH_PROPERTY
        merged_criteria = {}

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

    # If currently in AWAITING_SLOT and customer provides ordinal -> route to BOOKING
    if state.get("phase") == "AWAITING_SLOT" and (ordinal is not None or intent == Intent.SELECT_SLOT):
        current_agent = AgentType.BOOKING
        intent = Intent.SELECT_SLOT

    latency_ms = round((time.perf_counter() - started) * 1000)

    # Construct state updates
    updates: dict[str, Any] = {
        "current_agent": current_agent,
        "intent": intent,
        "confidence": understanding.confidence,
        "direct_response": understanding.direct_response,
        "search_criteria": merged_criteria,
        "soft_preferences": soft_prefs,
        "household_context": household_ctx,
        "commute_landmark": understanding.commute_landmark or state.get("commute_landmark"),
        "max_commute_minutes": understanding.max_commute_minutes or state.get("max_commute_minutes"),
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
            props = state.get("selected_properties", [])
            if 0 <= ordinal < len(props):
                updates["current_property_id"] = str(props[ordinal].get("id"))

    return updates


def route_from_supervisor(state: AgentState) -> str:
    """Routing function from supervisor to workers."""
    return state.get("current_agent", AgentType.RESPOND)
