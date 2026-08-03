"""Response Agent - Generates final response to user."""

import json
import logging
from datetime import datetime

from src.agents.state import AgentState, AgentType, Intent, add_message
from src.services.llm import get_llm, get_system_prompt

logger = logging.getLogger(__name__)


async def respond_node(state: AgentState) -> dict:
    """Respond node - generates the final response to user.

    This node:
    1. Takes the current state and any accumulated results
    2. Uses LLM to generate a natural language response
    3. Adds the response to the message history

    Args:
        state: Current agent state

    Returns:
        Updated state with response
    """
    # Get existing response or generate new one
    existing_response = state.get("response", "")
    error = state.get("error")
    intent = state.get("intent")
    next_action = state.get("next_action")

    # If there's an error, generate error response
    if error and not existing_response:
        existing_response = f"Xin lỗi, tôi gặp lỗi: {error}. Bạn có thể diễn đạt lại được không?"

    # If there's a specific next action, handle it
    if next_action:
        existing_response = await _handle_next_action(state, next_action)

    # If no response yet, generate one
    if not existing_response:
        existing_response = await _generate_response(state)

    # If still no response, use fallback
    if not existing_response:
        existing_response = "Xin lỗi, tôi không thể xử lý yêu cầu của bạn lúc này. Bạn có thể thử lại sau?"

    # Add assistant message to history
    messages = state.get("messages", [])
    messages.append({
        "role": "assistant",
        "content": existing_response,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {
        "response": existing_response,
        "messages": messages,
    }


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

    else:
        return ""


async def _generate_response(state: AgentState) -> str:
    """Generate response using LLM.

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
- Nếu có thông tin bất động sản, trình bày rõ ràng
- Nếu cần thêm thông tin từ khách, đặt câu hỏi cụ thể

Trả lời:"""

    try:
        llm = get_llm()
        from langchain_core.messages import HumanMessage
        result = await llm.ainvoke([HumanMessage(content=prompt)])
        return result.content if hasattr(result, 'content') else str(result)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Xin lỗi, tôi gặp sự cố khi tạo phản hồi. Bạn có thể diễn đạt lại được không?"


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
