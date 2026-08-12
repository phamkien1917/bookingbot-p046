"""Supervisor (Conversation) Agent - Main orchestrator.

This agent classifies user intent and routes to appropriate sub-agents.
"""

import json
import logging
import re

from src.agents.state import AgentState, AgentType, Intent
from src.services.llm import get_llm
from src.services.memory import get_intent_cache

logger = logging.getLogger(__name__)


# Intent classification prompt
INTENT_CLASSIFICATION_PROMPT = """Bạn là một classifier phân loại ý định của khách hàng trong hệ thống đặt lịch xem nhà.

## Các intent có thể có:
1. SEARCH_PROPERTY - Khách muốn tìm kiếm bất động sản
2. BOOK_APPOINTMENT - Khách muốn đặt lịch xem nhà
3. CANCEL_BOOKING - Khách muốn hủy lịch đã đặt
4. RESCHEDULE - Khách muốn dời lịch
5. CHECK_STATUS - Khách muốn kiểm tra trạng thái booking
6. GET_INFO - Khách hỏi thông tin về MỘT CĂN CỤ THỂ (kèm mã căn / property_id)
7. GENERAL_QA - Khách hỏi câu hỏi tổng quát về BĐS (lưu ý khi mua, xu hướng, thị trường...) — KHÔNG search DB
8. GREETING - Chào hỏi, hỏi thăm
9. FALLBACK - Không xác định được intent

## Yêu cầu:
- Chỉ trả về JSON với format bên dưới
- Không giải thích thêm
- confidence: mức độ tin chắc (0.0-1.0)

## Hướng dẫn đọc hiểu (Từ viết tắt tiếng Việt):
- "pn", "ngủ" -> bedrooms (phòng ngủ)
- "vs", "wc", "tắm" -> bathrooms (phòng tắm/vệ sinh)
- "tr", "triệu" -> x 1,000,000 VND
- "tỷ" -> x 1,000,000,000 VND

## Output format:
{
    "intent": "INTENT_NAME",
    "confidence": 0.95,
    "entities": {
        "district": "Quận 7",
        "province": "Hà Nội",
        "property_kind": "APARTMENT",
        "budget": 3000000000,            # số VND hoặc null
        "bedrooms": 2,                   # số phòng ngủ tối thiểu
        "bathrooms": 2,                  # số phòng tắm/vệ sinh tối thiểu
        "area_sqm": 80,                  # diện tích tối thiểu (m²)
        "keyword": "tên dự án, tên căn hộ hoặc đặc điểm", # từ khóa tìm kiếm
        "property_id": "uuid-or-code",   # chỉ có khi GET_INFO về căn cụ thể
        "booking_code": "BK12345678",
        "preferred_date": "2026-08-07"
    }
}

## Hội thoại mẫu:
- "Tôi muốn tìm căn hộ 2 phòng ngủ ở quận 7" -> SEARCH_PROPERTY
- "Đặt lịch xem căn đó vào chiều mai" -> BOOK_APPOINTMENT
- "Tôi muốn hủy lịch" -> CANCEL_BOOKING
- "Lịch của tôi thế nào rồi?" -> CHECK_STATUS
- "Cho tôi xem thông tin căn mã 0223" -> GET_INFO (kèm property_id)
- "Lưu ý khi mua căn hộ chung cư là gì?" -> GENERAL_QA
- "Xu hướng BĐS hiện nay thế nào?" -> GENERAL_QA
- "Xin chào" -> GREETING

Phân loại tin nhắn sau và trả về JSON:"""


# ============== Fast-path Intent Classification ==============
# Xử lý intent đơn giản bằng pattern matching, KHÔNG qua LLM
# Giảm thời gian phản hồi từ 10-20s xuống <100ms

_FAST_INTENT_PATTERNS = {
    Intent.GREETING: [
        r"^(xin\s+chào|chào|hello|hi|hey|chào\s+bạn)\s*[.!]*$",
        r"^(tôi|tớ|mình)\s+(muốn|cần|muốn|cần)\s*$",
    ],
    Intent.SEARCH_PROPERTY: [
        r"(tìm|tìm\s+kiếm|muốn\s+tìm|cần\s+tìm)\s.*(căn\s+hộ|nhà|đất|villa|biet\s*thu|townhouse)",
        r"(căn\s+hộ|nhà\s+ở|đất\s+nền|shophouse)\s",
        r"(quận|huyện|phường|thành\s+phố|tp)\s*\d",
        r"(diện\s+tích|ngân\s+sách)\s*\d",
    ],
    Intent.BOOK_APPOINTMENT: [
        r"(đặt\s+lich|đặt\s+lich\s+xem|dặt\s+lich|dặt\s+lich\s+xem)\s",
        r"(hẹn\s+xem|xem\s+nhà|thăm\s+nhà)\s",
        r"(ngày\s+nào|khi\s+nào|lúc\s+nào)\s+(đặt|xem|đi\s+xem)",
    ],
    Intent.CHECK_STATUS: [
        r"(trạng\s+thái|tình\s+trạng|tới\s+đâu|rồi|chưa)\s*(lịch|booking|hẹn)",
        r"(lịch|hẹn|booking)\s+(của|tôi)\s",
        r"(có\s+hẹn|đã\s+đặt)\s",
    ],
    Intent.CANCEL_BOOKING: [
        r"(hủy|hủy\s+bỏ|bỏ)\s+(lịch|hẹn|booking)",
    ],
    Intent.RESCHEDULE: [
        r"(dời|dời\s+lịch|thay\s+đổi\s+lịch|chuyển\s+lịch)\s",
    ],
    Intent.GET_INFO: [
        r"(thông\s+tin|chi\s+tiết|xem\s+thêm)\s+(căn|mã|property)",
        r"(căn|mã|property)\s*(nào|id|mã)\s*\w",
    ],
    Intent.GENERAL_QA: [
        r"(lưu\s+ý|chú\s+ý|cần\s+biết)\s+(khi|mua|đầu\s+tư)",
        r"(xu\s+hướng|tình\s+hình|thị\s+trường)\s",
        r"(nên|mua|đầu\s+tư)\s+(ở|đâu|khi)\s",
        r"( CCMN|ccmn|dự\s+án)\s",
    ],
}

_FAST_INTENT_RESPONSES = {
    Intent.GREETING: {"intent": Intent.GREETING, "confidence": 0.95, "entities": {}},
    Intent.SEARCH_PROPERTY: {"intent": Intent.SEARCH_PROPERTY, "confidence": 0.5, "entities": {}},
    Intent.BOOK_APPOINTMENT: {"intent": Intent.BOOK_APPOINTMENT, "confidence": 0.5, "entities": {}},
    Intent.CHECK_STATUS: {"intent": Intent.CHECK_STATUS, "confidence": 0.9, "entities": {}},
    Intent.CANCEL_BOOKING: {"intent": Intent.CANCEL_BOOKING, "confidence": 0.9, "entities": {}},
    Intent.RESCHEDULE: {"intent": Intent.RESCHEDULE, "confidence": 0.9, "entities": {}},
    Intent.GET_INFO: {"intent": Intent.GET_INFO, "confidence": 0.5, "entities": {}},
    Intent.GENERAL_QA: {"intent": Intent.GENERAL_QA, "confidence": 0.8, "entities": {}},
}


def _fast_classify_intent(message: str) -> dict | None:
    """Fast intent classification bằng pattern matching.

    Args:
        message: Tin nhắn của user

    Returns:
        Dict với intent, confidence, entities hoặc None nếu không match
    """
    if not message:
        return None

    cleaned = message.lower().strip()
    # Bỏ emoji ở cuối
    cleaned = re.sub(r"[\W_]+$", "", cleaned, flags=re.UNICODE).strip()

    for intent, patterns in _FAST_INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, cleaned, re.IGNORECASE | re.UNICODE):
                result = _FAST_INTENT_RESPONSES[intent].copy()
                logger.debug(f"Fast intent match: {intent} (pattern: {pattern})")
                return result

    return None


async def classify_intent(
    messages: list[dict],
    session_id: str | None = None,
) -> dict:
    """Classify user intent from messages.

    Thứ tự ưu tiên:
    1. Cache - trả ngay nếu đã có kết quả
    2. Fast classification (pattern matching) - <10ms, không gọi LLM
    3. LLM classification - cho các trường hợp phức tạp

    Args:
        messages: List of conversation messages
        session_id: Session ID (dùng làm cache key)

    Returns:
        Dict with intent, confidence, and entities
    """
    import time
    start_time = time.time()

    cache = get_intent_cache()
    msg_hash = IntentCache.hash_messages(messages) if session_id else None

    # 1) Check cache
    if session_id and msg_hash:
        cached = await cache.get(session_id, msg_hash)
        if cached:
            logger.debug(f"Intent cache hit (session={session_id})")
            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Intent classified in {elapsed_ms:.0f}ms (cache)")
            return cached

    # Lấy tin nhắn gần nhất
    recent = messages[-5:] if len(messages) > 5 else messages
    last_user_msg = ""
    for msg in reversed(recent):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "")
            break

    # 2) Fast classification - pattern matching (KHÔNG gọi LLM)
    if last_user_msg:
        fast_result = _fast_classify_intent(last_user_msg)
        if fast_result and fast_result["confidence"] >= 0.8:
            # Set cache for next time
            if session_id and msg_hash:
                await cache.set(session_id, msg_hash, fast_result)
            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Intent classified in {elapsed_ms:.0f}ms (fast-path: {fast_result['intent']})")
            return fast_result

    # 3) LLM classification - cho các trường hợp phức tạp
    conversation = "\n".join([f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in recent])
    prompt = f"{INTENT_CLASSIFICATION_PROMPT}\n\nTin nhắn gần nhất:\n{conversation}"

    from langchain_core.messages import HumanMessage

    from src.services.llm import reset_llm

    last_error = None
    tried_models = []

    # Retry với automatic fallback - thử 3 model khác nhau
    for attempt in range(3):
        try:
            llm = get_llm()
            current_model = llm.model_name
            tried_models.append(current_model)

            logger.info(f"Intent LLM attempt {attempt + 1}: using {current_model}")

            result = await llm.ainvoke([HumanMessage(content=prompt)])

            # Parse JSON response
            content = result.content if hasattr(result, 'content') else str(result)
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            parsed = json.loads(content.strip())

            # Set cache
            if session_id and msg_hash:
                await cache.set(session_id, msg_hash, parsed)

            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Intent classified in {elapsed_ms:.0f}ms (LLM: {tried_models[-1]})")
            return parsed

        except Exception as e:
            last_error = e
            error_str = str(e).lower()
            logger.warning(f"Intent LLM attempt {attempt + 1} failed: {e}")

            # Kiểm tra loại lỗi - nếu là quota/credits thì thử model khác
            if any(keyword in error_str for keyword in [
                "insufficient credits", "quota", "rate limit", "429",
                "overloaded", "context length", "max tokens"
            ]):
                logger.info(f"Model {tried_models[-1] if tried_models else 'unknown'} exhausted, switching...")
                reset_llm()  # Reset để dùng model tiếp theo
                continue
            else:
                # Lỗi khác - vẫn thử model khác
                reset_llm()
                continue

    # Tất cả đều thất bại - dùng fast classification làm fallback
    logger.warning("All LLM attempts failed, using fast classification fallback")
    fast_result = _fast_classify_intent(last_user_msg) if last_user_msg else None
    if fast_result:
        if session_id and msg_hash:
            await cache.set(session_id, msg_hash, fast_result)
        return fast_result

    elapsed_ms = (time.time() - start_time) * 1000
    logger.error(f"All intent classification failed after {elapsed_ms:.0f}ms")
    return {
        "intent": Intent.GREETING,
        "confidence": 0.0,
        "entities": {},
        "error": str(last_error),
    }


async def supervisor_node(state: AgentState) -> dict:
    """Supervisor node - classifies intent and routes to appropriate agent.

    This is the main entry point for the multi-agent system.

    Args:
        state: Current agent state

    Returns:
        Updated state with routing information
    """
    messages = state.get("messages", [])
    current_agent = state.get("current_agent", AgentType.SUPERVISOR)
    session_id = state.get("session_id")

    logger.info(f"[SUPERVISOR] Starting. current_agent={current_agent}, messages_count={len(messages)}")

    # If already routed, don't re-classify
    if current_agent != AgentType.SUPERVISOR:
        logger.info(f"[SUPERVISOR] Already routed to {current_agent}, skipping classification")
        return {"current_agent": current_agent}

    try:
        # Classify intent (có cache)
        classification = await classify_intent(messages, session_id=session_id)
        intent = classification.get("intent", Intent.FALLBACK)
        confidence = classification.get("confidence", 0.0)
        entities = classification.get("entities", {})

        logger.info(f"Classified intent: {intent} (confidence: {confidence})")

        # Update state with classification
        updates = {
            "intent": intent,
            "confidence": confidence,
            "metadata": {
                **state.get("metadata", {}),
                "entities": entities,
                "classification": classification,
            },
        }

        # Route based on intent
        if intent == Intent.SEARCH_PROPERTY:
            updates["current_agent"] = AgentType.INVENTORY
        elif intent == Intent.BOOK_APPOINTMENT:
            updates["current_agent"] = AgentType.BOOKING
        elif intent == Intent.CANCEL_BOOKING:
            updates["current_agent"] = AgentType.BOOKING
        elif intent == Intent.RESCHEDULE:
            updates["current_agent"] = AgentType.BOOKING
        elif intent == Intent.CHECK_STATUS:
            updates["current_agent"] = AgentType.RESPOND  # Can handle directly
            updates["next_action"] = "check_booking_status"
        elif intent == Intent.GET_INFO:
            # Route tới INVENTORY khi có property_id cụ thể HOẶC có keyword/tên căn
            if entities.get("property_id") or entities.get("keyword"):
                updates["current_agent"] = AgentType.INVENTORY
            else:
                updates["current_agent"] = AgentType.RESPOND
                updates["next_action"] = "ask_property_id"
        elif intent == Intent.GENERAL_QA:
            # Câu hỏi tổng quát — KHÔNG search DB, route thẳng tới respond
            updates["current_agent"] = AgentType.RESPOND
            updates["next_action"] = "general_qa"
        elif intent == Intent.GREETING:
            updates["current_agent"] = AgentType.RESPOND
            updates["next_action"] = "greet"
        else:
            # FALLBACK - respond with clarification
            updates["current_agent"] = AgentType.RESPOND
            updates["next_action"] = "clarify"

        return updates

    except Exception as e:
        logger.error(f"Error in supervisor: {e}")
        return {
            "current_agent": AgentType.RESPOND,
            "error": str(e),
            "error_recovery_suggestion": "Xin lỗi, tôi không hiểu ý bạn. Bạn có thể diễn đạt lại được không?",
        }


def route_from_supervisor(state: AgentState) -> str:
    """Determine next node based on supervisor routing.

    The routing is based on current_agent (which supervisor sets BEFORE this is called):
    - SUPERVISOR: Initial entry, should go to specialized agent based on intent
    - INVENTORY: Inventory agent should run next
    - BOOKING: Booking agent should run next
    - RESPOND/ASSIGNMENT/HITL: Should go to respond

    Args:
        state: Current agent state

    Returns:
        Next node name
    """
    current_agent = state.get("current_agent", AgentType.SUPERVISOR)

    # If awaiting human decision, go to HITL
    if state.get("awaiting_human"):
        return AgentType.HITL

    # Route based on current_agent set by supervisor
    agent_to_node = {
        AgentType.INVENTORY: "inventory",
        AgentType.BOOKING: "booking",
        AgentType.ASSIGNMENT: "respond",
        AgentType.HITL: "respond",
        AgentType.RESPOND: "respond",
    }

    # If agent is SUPERVISOR, route based on intent
    if current_agent == AgentType.SUPERVISOR:
        intent = state.get("intent", "GREETING")
        intent_routes = {
            "SEARCH_PROPERTY": "inventory",
            "GET_INFO": "inventory",
            "BOOK_APPOINTMENT": "booking",
            "CANCEL_BOOKING": "booking",
            "RESCHEDULE": "booking",
            "GET_BOOKING_STATUS": "respond",
            "GET_MY_BOOKINGS": "respond",
            "CLARIFY": "respond",
            "GREETING": "respond",
            "SMALLTALK": "respond",
            "ESCALATE": "hitl",
        }
        return intent_routes.get(intent, "respond")

    return agent_to_node.get(current_agent, "respond")


# Backward-compatible alias for IntentCache (avoid circular import in some contexts)
from src.services.memory import IntentCache  # noqa: E402
