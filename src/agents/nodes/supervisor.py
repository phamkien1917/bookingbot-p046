"""Supervisor (Conversation) Agent - Main orchestrator.

This agent classifies user intent and routes to appropriate sub-agents.
"""

import json
import logging
from typing import Any

from src.agents.state import AgentState, AgentType, Intent
from src.services.llm import get_llm, get_system_prompt

logger = logging.getLogger(__name__)


# District normalization mapping
_DISTRICT_ALIASES = {
    # TP. Thủ Đức (merged from Q2, Q9, Thủ Đức district)
    "thủ đức": "Thành phố Thủ Đức",
    "quận 2": "Thành phố Thủ Đức",
    "quận 9": "Thành phố Thủ Đức",
    "tp thủ đức": "Thành phố Thủ Đức",
    "thành phố thủ đức": "Thành phố Thủ Đức",
    "tp.hcm thủ đức": "Thành phố Thủ Đức",
    # Other districts
    "cầu giấy": "Quận Cầu Giấy",
    "cau giay": "Quận Cầu Giấy",
    "hai ba trung": "Quận Hai Bà Trưng",
    "thanh xuan": "Quận Thanh Xuân",
    "dong da": "Quận Đống Đa",
    "hoan kiem": "Quận Hoàn Kiếm",
    "hoàn kiếm": "Quận Hoàn Kiếm",
    "tay ho": "Quận Tây Hồ",
    "tây hồ": "Quận Tây Hồ",
    "ba dinh": "Quận Ba Đình",
    "bà đình": "Quận Ba Đình",
    "long bien": "Quận Long Biên",
    "long biên": "Quận Long Biên",
}

# Property kind normalization
_PROPERTY_KIND_ALIASES = {
    "căn hộ": "APARTMENT",
    "căn hộ chung cư": "APARTMENT",
    "chung cư": "APARTMENT",
    "nhà": "HOUSE",
    "nhà phố": "TOWNHOUSE",
    "nhà liền kề": "TOWNHOUSE",
    "biệt thự": "VILLA",
    "đất": "LAND",
    "đất nền": "LAND",
    "mặt bằng": "COMMERCIAL",
    "shophouse": "COMMERCIAL",
}


def _normalize_entities(entities: dict) -> dict:
    """Normalize extracted entities for consistency.

    Args:
        entities: Raw entities from classification

    Returns:
        Normalized entities
    """
    normalized = entities.copy() if entities else {}

    # Normalize district
    district = normalized.get("district")
    if district:
        district_lower = district.lower().strip()
        if district_lower in _DISTRICT_ALIASES:
            normalized["district"] = _DISTRICT_ALIASES[district_lower]
        # Also check without "quận" prefix
        elif district_lower.startswith("quận "):
            dist_name = district_lower.replace("quận ", "")
            if dist_name in _DISTRICT_ALIASES:
                normalized["district"] = _DISTRICT_ALIASES[dist_name]

    # Normalize province
    province = normalized.get("province")
    if province:
        province_lower = province.lower().strip()
        if province_lower in ["tp.hcm", "tphcm", "hcm", "sg", "sài gòn", "hồ chí minh"]:
            normalized["province"] = "Hồ Chí Minh"

    # Normalize property_kind
    property_kind = normalized.get("property_kind")
    if property_kind:
        kind_lower = property_kind.lower().strip()
        if kind_lower in _PROPERTY_KIND_ALIASES:
            normalized["property_kind"] = _PROPERTY_KIND_ALIASES[kind_lower]

    # Handle "dự án" as property search intent
    if "dự án" in str(normalized).lower() or "du an" in str(normalized).lower():
        if "property_kind" not in normalized or normalized.get("property_kind") is None:
            # User asking about projects, likely apartment/development
            normalized["property_kind"] = "APARTMENT"

    return normalized


# Intent classification prompt
INTENT_CLASSIFICATION_PROMPT = """Bạn là một classifier phân loại ý định của khách hàng trong hệ thống đặt lịch xem nhà.

## Các intent có thể có:
1. SEARCH_PROPERTY - Khách muốn tìm kiếm bất động sản
2. BOOK_APPOINTMENT - Khách muốn đặt lịch xem nhà
3. CANCEL_BOOKING - Khách muốn hủy lịch đã đặt
4. RESCHEDULE - Khách muốn dời lịch
5. CHECK_STATUS - Khách muốn kiểm tra trạng thái booking
6. GET_INFO - Khách hỏi thông tin về bất động sản, quy trình...
7. GREETING - Chào hỏi, hỏi thăm
8. FALLBACK - Không xác định được intent

## Yêu cầu:
- Chỉ trả về JSON với format bên dưới
- Không giải thích thêm
- confidence: mức độ tin chắc (0.0-1.0)

## Output format:
{
    "intent": "INTENT_NAME",
    "confidence": 0.95,
    "entities": {
        "district": "Quận 7",  # nếu có
        "district": "Thành phố Thủ Đức",  # normalize Thủ Đức/Quận 9/Quận 2
        "property_kind": "APARTMENT",  # nếu có
        "budget": 3000000000,  # nếu có
        "booking_code": "BK12345678"  # nếu có
    }

## Xử lý district đặc biệt:
- "Thủ Đức", "Quận 2", "Quận 9", "Quận Thủ Đức" -> normalize thành "Thành phố Thủ Đức"
- "Bình Thạnh" -> "Quận Bình Thạnh"
- "Gò Vấp" -> "Quận Gò Vấp"
}

## Hội thoại mẫu:
- "Tôi muốn tìm căn hộ 2 phòng ngủ ở quận 7" -> SEARCH_PROPERTY
- "Có dự án nào mới ở Thủ Đức không?" -> SEARCH_PROPERTY
- "Tìm nhà giá dưới 3 tỷ" -> SEARCH_PROPERTY
- "Căn hộ quận 9 nào đang bán?" -> SEARCH_PROPERTY
- "Đặt lịch xem căn đó vào chiều mai" -> BOOK_APPOINTMENT
- "Tôi muốn hủy lịch" -> CANCEL_BOOKING
- "Lịch của tôi thế nào rồi?" -> CHECK_STATUS
- "Căn này có tầng view sông không?" -> GET_INFO
- "Xin chào" -> GREETING

Phân loại tin nhắn sau và trả về JSON:"""


async def classify_intent(messages: list[dict]) -> dict:
    """Classify user intent from messages.

    Args:
        messages: List of conversation messages

    Returns:
        Dict with intent, confidence, and entities
    """
    llm = get_llm()

    # Get recent messages for context
    recent = messages[-5:] if len(messages) > 5 else messages
    conversation = "\n".join([f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in recent])

    prompt = f"{INTENT_CLASSIFICATION_PROMPT}\n\nTin nhắn gần nhất:\n{conversation}"

    try:
        from langchain_core.messages import HumanMessage
        result = await llm.ainvoke([HumanMessage(content=prompt)])

        # Parse JSON response
        content = result.content if hasattr(result, 'content') else str(result)
        # Extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        return json.loads(content.strip())
    except Exception as e:
        logger.error(f"Error classifying intent: {e}")
        return {
            "intent": Intent.FALLBACK,
            "confidence": 0.0,
            "entities": {},
            "error": str(e),
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

    # If already routed, don't re-classify
    if current_agent != AgentType.SUPERVISOR:
        return {"current_agent": current_agent}

    try:
        # Classify intent
        classification = await classify_intent(messages)
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

        # Normalize entities
        entities = _normalize_entities(entities)
        updates["metadata"] = {
            **state.get("metadata", {}),
            "entities": entities,
            "classification": classification,
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
            updates["current_agent"] = AgentType.INVENTORY
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

    Args:
        state: Current agent state

    Returns:
        Next node name
    """
    current_agent = state.get("current_agent", AgentType.SUPERVISOR)

    # If awaiting human decision, go to HITL
    if state.get("awaiting_human"):
        return AgentType.HITL

    # Route based on current agent
    agent_routes = {
        AgentType.SUPERVISOR: AgentType.RESPOND,
        AgentType.INVENTORY: AgentType.RESPOND,
        AgentType.BOOKING: AgentType.ASSIGNMENT,
        AgentType.ASSIGNMENT: AgentType.RESPOND,
        AgentType.HITL: AgentType.RESPOND,
        AgentType.RESPOND: "__end__",
    }

    return agent_routes.get(current_agent, AgentType.RESPOND)
