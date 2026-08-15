"""Response Agent - Generates final response to user."""

import json
import logging
import re
from datetime import datetime

from src.agents.state import AgentState
from src.services.llm import get_llm, get_system_prompt

logger = logging.getLogger(__name__)


# ============== Smalltalk fast-path ==============
# Các câu ngắn như "Cảm ơn", "OK", "Tạm biệt" — KHÔNG qua LLM, tiết kiệm 3–8s.
_SMALLTALK_PATTERNS = [
    r"^(cảm\s+ơn|cám\s+ơn|thank\s*you|thanks|thank)\b",
    r"^(tạm\s+biệt|chào\s+tạm\s+biệt|bye|goodbye|see\s*you)\b",
    r"^(ok|okay|okie|được|tốt|hiểu\s+rồi|được\s+rồi)\s*[.!]*$",
    r"^(vâng|dạ|uhm|ừ|ừm)\s*[.!]*$",
]

_SMALLTALK_RESPONSES = [
    "Rất vui được hỗ trợ bạn! 😊 Bạn cần tôi giúp gì thêm không?",
    "Không có gì. Tôi sẵn sàng hỗ trợ bạn tiếp! 🏡",
    "Cảm ơn bạn! Hẹn gặp lại. 🌟",
    "Tạm biệt bạn! Chúc bạn một ngày tốt lành. 👋",
]


def _is_smalltalk(text: str) -> bool:
    """Kiểm tra text có phải smalltalk (cảm ơn / tạm biệt / ok) hay không.

    Trả về True nếu match bất kỳ pattern nào (case-insensitive, cho phép emoji cuối).
    """
    if not text:
        return False
    cleaned = text.strip().lower()
    # Bỏ emoji phía cuối (heuristic: bỏ non-alpha ở cuối)
    cleaned = re.sub(r"[\W_]+$", "", cleaned, flags=re.UNICODE).strip()
    for pattern in _SMALLTALK_PATTERNS:
        if re.match(pattern, cleaned, flags=re.IGNORECASE | re.UNICODE):
            return True
    return False


def _pick_smalltalk_response(text: str) -> str:
    """Chọn response template phù hợp với loại smalltalk."""
    cleaned = text.strip().lower()
    if "tạm biệt" in cleaned or "bye" in cleaned or "goodbye" in cleaned:
        return _SMALLTALK_RESPONSES[3]
    if "cảm ơn" in cleaned or "cám ơn" in cleaned or "thank" in cleaned:
        return _SMALLTALK_RESPONSES[0]
    return _SMALLTALK_RESPONSES[1]


# ============== Out-of-scope redirect ==============
# Chuyển hướng TẤT CẢ câu hỏi không liên quan đến tìm kiếm/đặt lịch
_OUT_OF_SCOPE_RESPONSE = """Tôi là BookingBot - **TRỢ LÝ ĐẶT LỊCH XEM NHÀ & GIỮ CĂN TỰ ĐỘNG** 😊

Câu hỏi của bạn tôi không trả lời được. Bạn vui lòng hỏi trực tiếp Sale khi đi xem nhà nhé.

Bạn có muốn tôi giữ căn này và đặt lịch xem nhà không?"""


# ============== General QA handler ==============
# Câu hỏi tổng quát về BĐS — trả message cố định, không qua LLM knowledge.
# Triết lý: SQL/DB là source of truth. Nếu không có data, KHÔNG bịa.
_GENERAL_QA_RESPONSES = [
    "Tôi chuyên hỗ trợ tìm kiếm bất động sản và đặt lịch xem nhà. "
    "Bạn có muốn tôi giúp:\n"
    "🔍 Tìm căn hộ phù hợp với tiêu chí của bạn\n"
    "📅 Đặt lịch xem một căn cụ thể\n"
    "📋 Kiểm tra trạng thái booking\n\n"
    "Bạn muốn tôi hỗ trợ gì?",
    "Tôi không có thông tin chi tiết về chủ đề này trong hệ thống. "
    "Tuy nhiên tôi có thể giúp bạn tìm bất động sản phù hợp hoặc đặt lịch xem nhà. "
    "Bạn muốn bắt đầu từ đâu?",
]


async def respond_node(state: AgentState) -> dict:
    """Respond node - generates the final response to user.

    Pipeline (theo thứ tự ưu tiên):
    1. Error response (nếu có error và response rỗng)
    2. next_action handler (greet/clarify/check_status/ask_property_id/general_qa)
    3. Smalltalk fast-path (cảm ơn/tạm biệt/ok) — KHÔNG qua LLM, <100ms
    4. Knowledge Base fast-path (FAQ, thông tin dự án) — KHÔNG qua LLM, <200ms
    5. _generate_response() qua LLM (với SystemMessage bound)
    6. Fallback

    Args:
        state: Current agent state

    Returns:
        Updated state with response
    """
    global _RESPOND_NODE_CALLED
    _RESPOND_NODE_CALLED = True

    import time
    start_time = time.time()
    response_source = "unknown"

    # Get existing response or generate new one
    existing_response = state.get("response", "")
    error = state.get("error")
    intent = state.get("intent")
    next_action = state.get("next_action")

    # 1) Error response
    if error and not existing_response:
        existing_response = f"Xin lỗi, tôi gặp lỗi: {error}. Bạn có thể diễn đạt lại được không?"
        response_source = "error"

    # 2) Specific next action handler
    if next_action and not existing_response:
        existing_response = await _handle_next_action(state, next_action)
        response_source = "next_action"

    # 3) Smalltalk fast-path — tiết kiệm latency
    if not existing_response:
        last_user_msg = _get_last_user_message(state)
        if last_user_msg and _is_smalltalk(last_user_msg):
            existing_response = _pick_smalltalk_response(last_user_msg)
            response_source = "smalltalk"
            logger.debug(f"Smalltalk fast-path: '{last_user_msg}' -> template")

    # 4) Out-of-scope: intent KHÔNG phải tìm kiếm/đặt lịch → chuyển về đặt lịch
    # Agent CHỈ làm: tìm kiếm bất động sản & đặt lịch xem nhà
    if not existing_response:
        intents_to_handle = {
            "SEARCH_PROPERTY", "GET_INFO", "BOOK_APPOINTMENT", "CANCEL_BOOKING",
            "RESCHEDULE", "CHECK_STATUS", "GET_BOOKING_STATUS", "GET_MY_BOOKINGS",
            "UPDATE_BOOKING"
        }
        # Nếu không có selected_properties và intent không phải core task → redirect
        selected_props = state.get("selected_properties", [])
        if intent and intent not in intents_to_handle and not selected_props:
            existing_response = _OUT_OF_SCOPE_RESPONSE
            response_source = "out_of_scope"
            logger.info(f"Out-of-scope intent: {intent}")

    # 5) Knowledge Base fast-path — TRƯỚC KHI gọi LLM!
    # Đây là bước QUAN TRỌNG để giảm thời gian phản hồi từ 20s xuống <500ms
    if not existing_response:
        from src.services.knowledge_base import get_answer
        last_user_msg = _get_last_user_message(state)
        if last_user_msg:
            kb_response = await get_answer(last_user_msg)
            if kb_response:
                existing_response = kb_response
                response_source = "knowledge_base"

    # 6) Generate via LLM (chỉ khi không có cached response)
    if not existing_response:
        response_source = "llm"
        existing_response = await _generate_response(state)

    # 7) Final fallback
    if not existing_response:
        existing_response = "Xin lỗi, tôi không thể xử lý yêu cầu của bạn lúc này. Bạn có thể thử lại sau?"
        response_source = "fallback"

    # Log response time
    elapsed_ms = (time.time() - start_time) * 1000

    # Add assistant message to history
    messages = state.get("messages", [])
    messages.append({
        "role": "assistant",
        "content": existing_response,
        "timestamp": datetime.utcnow().isoformat(),
        "_source": response_source,
        "_response_time_ms": elapsed_ms,
    })

    return {
        "response": existing_response,
        "messages": messages,
    }


def _get_last_user_message(state: AgentState) -> str:
    """Lấy text user message gần nhất (nếu có)."""
    messages = state.get("messages", [])
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "") or ""
    return state.get("query", "") or ""


async def _handle_next_action(state: AgentState, action: str) -> str:
    """Handle specific next actions.

    Args:
        state: Current agent state
        action: Action to handle

    Returns:
        Response string
    """
    if action == "greet":
        return (
            "Xin chào! 👋\n\n"
            "Tôi là BookingBot, trợ lý AI của công ty bất động sản.\n\n"
            "Tôi có thể giúp bạn:\n"
            "🔍 Tìm kiếm bất động sản phù hợp\n"
            "📅 Đặt lịch xem nhà\n"
            "📋 Kiểm tra trạng thái booking\n"
            "❓ Trả lời các câu hỏi về bất động sản\n\n"
            "Bạn cần tôi hỗ trợ gì hôm nay?"
        )

    elif action == "clarify":
        return (
            "Xin lỗi, tôi chưa hiểu rõ ý bạn. 😕\n\n"
            "Bạn có thể:\n"
            "1. Mô tả lại yêu cầu của bạn\n"
            "2. Hỏi về dịch vụ của chúng tôi\n"
            "3. Yêu cầu tìm kiếm bất động sản\n"
            "4. Đặt lịch xem nhà\n\n"
            "Tôi sẵn sàng giúp bạn!"
        )

    elif action == "check_booking_status":
        return (
            "Để kiểm tra trạng thái booking, vui lòng cung cấp:\n"
            "- Mã booking (VD: BK12345678)\n"
            "hoặc\n"
            "- Số điện thoại đã đăng ký\n\n"
            "Bạn có thể cung cấp thông tin này không?"
        )

    elif action == "ask_property_id":
        # GET_INFO mà không có property_id cụ thể — chuyển về đặt lịch
        # Agent CHỈ làm: tìm kiếm & đặt lịch
        return _OUT_OF_SCOPE_RESPONSE

    elif action == "general_qa":
        # GENERAL_QA — chuyển về đặt lịch xem nhà
        # Agent CHỈ làm: tìm kiếm & đặt lịch
        return _OUT_OF_SCOPE_RESPONSE

    else:
        return ""


async def _generate_response(state: AgentState) -> str:
    """Generate response using LLM với SystemMessage bound.

    Args:
        state: Current agent state

    Returns:
        Generated response
    """
    messages = state.get("messages", [])
    recent = messages[-6:] if len(messages) > 6 else messages

    # Build context for LLM
    context = {
        "intent": state.get("intent"),
        "confidence": state.get("confidence"),
        "selected_properties": state.get("selected_properties", [])[:3],
        "selected_slots": state.get("selected_slots", []),
        "booking_id": state.get("booking_id"),
        "error": state.get("error"),
        "analysis": state.get("analysis"),
    }

    prompt = f"""Bạn là trợ lý AI của công ty bất động sản. Dựa vào ngữ cảnh sau, hãy trả lời khách hàng một cách tự nhiên bằng tiếng Việt.

Ngữ cảnh:
{json.dumps(context, ensure_ascii=False, indent=2)}

Lịch sử hội thoại:
{chr(10).join([f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in recent])}

Yêu cầu:
- Trả lời ngắn gọn, thân thiện
- Sử dụng emoji phù hợp
- Nếu có thông tin bất động sản (trong selected_properties), trình bày rõ ràng
- Nếu không có dữ liệu, hãy nói "tôi chưa có thông tin này" thay vì bịa
- Không trả UUID nội bộ, mã code, hay địa chỉ chi tiết

Trả lời:"""

    # Retry với automatic fallback - thử 3 model khác nhau
    from langchain_core.messages import HumanMessage, SystemMessage

    from src.services.llm import reset_llm

    last_error = None
    tried_models = []

    for attempt in range(3):
        try:
            llm = get_llm()
            current_model = llm.model_name
            tried_models.append(current_model)

            logger.info(f"LLM attempt {attempt + 1}: using {current_model}")

            system_prompt = get_system_prompt()
            result = await llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt),
            ])
            return result.content if hasattr(result, 'content') else str(result)

        except Exception as e:
            last_error = e
            error_str = str(e).lower()
            logger.warning(f"LLM attempt {attempt + 1} failed: {e}")

            # Kiểm tra loại lỗi
            if any(keyword in error_str for keyword in [
                "insufficient credits", "quota", "rate limit", "429",
                "429", "overloaded", "context length", "max tokens"
            ]):
                logger.info(f"Model {tried_models[-1]} exhausted, switching to next model...")
                reset_llm()  # Reset để dùng model tiếp theo trong priority list
                continue
            else:
                # Lỗi khác - thử model khác một lần nữa
                reset_llm()
                continue

    # Tất cả đều thất bại
    logger.error(f"All LLM attempts failed. Tried models: {tried_models}. Last error: {last_error}")

    # Trả message cố định thay vì crash
    return "Xin lỗi, hệ thống AI đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ hỗ trợ."


def format_property_list(properties: list[dict]) -> str:
    """Format a list of properties for display.

    Args:
        properties: List of property dicts

    Returns:
        Formatted string
    """
    if not properties:
        return "Không có bất động sản nào phù hợp."

    lines = []
    for i, prop in enumerate(properties[:5], 1):
        price = prop.get("list_price")
        if price:
            if price >= 1e9:
                price_str = f"{price/1e9:.1f} tỷ"
            else:
                price_str = f"{price/1e6:.0f} triệu"
        else:
            price_str = "Liên hệ"

        line = f"{i}. {prop.get('title', 'N/A')} - {price_str}"
        if prop.get("district"):
            line += f" ({prop['district']})"
        if prop.get("bedrooms"):
            line += f" - {prop['bedrooms']}PN"

        lines.append(line)

    return "\n".join(lines)
