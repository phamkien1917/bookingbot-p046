"""Respond Node for LangGraph Multi-Agent System.

Generates final grounded, natural, and personality-driven responses as Nera.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import AgentState, Intent
from src.services.llm import get_llm

logger = logging.getLogger(__name__)

NERA_PERSONA_PROMPT = """Bạn là Nera – Trợ lý AI kiêm chuyên viên tư vấn bất động sản cao cấp hàng đầu tại Việt Nam.

Phẩm chất & phong cách của bạn:
- Tự nhiên, ấm áp, tận tâm, chuyên nghiệp, thông thái và am hiểu sâu sắc thị trường bất động sản Việt Nam (TP.HCM, Hà Nội, Đà Nẵng...).
- Nắm vững các quy định pháp luật (Luật Đất đai, Luật Nhà ở, thủ tục công chứng, sang tên sổ đỏ, đặt cọc an toàn).
- Nắm vững tài chính & ngân hàng (tính toán phương án vay 70%, lãi suất thả nổi, thời gian ân hạn, khả năng chi trả hàng tháng).
- Hiểu phong thủy ứng dụng thực tế (hướng nhà, ánh sáng, thông gió, cảnh quan).
- Thấu hiểu hoàn cảnh khách hàng (gia đình có con nhỏ cần gần trường, người đi làm cần tiện đường, người đầu tư cần tiềm năng sinh lời).

Nguyên tắc phản hồi:
1. Tuyệt đối không bịa đặt các thông số kỹ thuật (giá, diện tích, phòng) nếu không có trong dữ liệu.
2. Trả lời mạch lạc, dễ hiểu, dùng Markdown đẹp mắt (bullet points, in đậm các ý chính, dùng emoji tinh tế).
3. Luôn kết thúc bằng một câu gợi mở tự nhiên hoặc hướng dẫn bước tiếp theo phù hợp.
4. Nếu người dùng hỏi các câu hỏi hoàn toàn ngoài lề (thời tiết, làm thơ, viết code...), hãy trả lời ngắn gọn, lịch sự và khéo léo kết nối lại về chủ đề nhà đất.
"""


async def respond_node(state: AgentState) -> dict[str, Any]:
    """Respond node: ensures a natural, high-quality, persona-aligned response is generated."""
    existing_response = state.get("response", "").strip()
    intent = state.get("intent")
    query = state.get("query", "")
    history = state.get("messages", [])
    direct_response = state.get("direct_response")

    final_response = existing_response
    ai_mode = state.get("ai_mode", "llm_grounded")

    # If no response generated yet, or intent is consultative/conversational
    if not final_response or intent in (
        Intent.CONSULTATION_QA,
        Intent.GREETING,
        Intent.THANKS,
        Intent.GOODBYE,
        Intent.OUT_OF_SCOPE,
        Intent.FALLBACK,
    ):
        if direct_response and direct_response.strip():
            final_response = direct_response.strip()
            ai_mode = "llm_direct"
        else:
            # Generate dynamic response with LLM
            recent_turns = []
            for msg in history[-6:]:
                role = msg.get("role", "user")
                content = str(msg.get("content", ""))
                if content:
                    recent_turns.append(f"{role.upper()}: {content}")

            context_info = {
                "intent": intent,
                "user_message": query,
                "active_criteria": state.get("search_criteria", {}),
                "soft_preferences": state.get("soft_preferences", []),
                "household_context": state.get("household_context", []),
                "selected_property_count": len(state.get("selected_properties", [])),
                "current_property_id": state.get("current_property_id"),
                "recent_history": recent_turns,
            }

            try:
                llm = get_llm()
                prompt_messages = [
                    SystemMessage(content=NERA_PERSONA_PROMPT),
                    HumanMessage(
                        content=f"Ngữ cảnh hiện tại:\n{json.dumps(context_info, ensure_ascii=False)}\n\n"
                        f"Tin nhắn mới của khách: \"{query}\"\n\n"
                        "Hãy trả lời khách hàng một cách xuất sắc, tận tâm và tự nhiên nhất:"
                    ),
                ]
                res = await llm.ainvoke(prompt_messages)
                final_response = res.content if hasattr(res, "content") else str(res)
                ai_mode = "llm_direct"
            except Exception as e:
                logger.error(f"Error in LLM response generation: {e}")
                if not final_response:
                    final_response = (
                        "Chào bạn, mình là Nera! Mình có thể hỗ trợ bạn tìm kiếm bất động sản phù hợp, "
                        "xem thông tin chi tiết và đặt lịch xem nhà trực tiếp với chuyên viên Sale. "
                        "Bạn đang quan tâm đến khu vực hoặc phân khúc nào?"
                    )
                ai_mode = "fallback"

    # Derive smart default suggested actions (Quick Replies) if empty
    suggested_actions = list(state.get("suggested_actions", []))
    if not suggested_actions:
        if intent == Intent.GREETING:
            suggested_actions = [
                "Tìm căn hộ Quận 7",
                "Tìm nhà riêng Hà Nội",
                "Tư vấn mua nhà lần đầu",
            ]
        elif intent == Intent.CONSULTATION_QA:
            suggested_actions = [
                "Tìm bất động sản phù hợp",
                "Tính thử phương án vay",
                "Quy trình đặt cọc an toàn",
            ]
        elif intent == Intent.OUT_OF_SCOPE:
            suggested_actions = [
                "Tìm căn hộ chung cư",
                "Tìm nhà phố liền kề",
                "Kiểm tra lịch xem nhà",
            ]
        elif state.get("phase") == "SEARCH_RESULTS":
            suggested_actions = ["Chọn căn số 1", "Chọn căn số 2", "So sánh các căn"]
        else:
            suggested_actions = ["Tìm căn hộ", "Tìm nhà phố", "Đặt lịch xem nhà"]

    # Build insights dictionary for frontend sidebar
    criteria = state.get("search_criteria", {})
    insights: dict[str, Any] = {
        key: val for key, val in criteria.items() if val not in (None, "", [])
    }
    if state.get("soft_preferences"):
        insights["soft_preferences"] = state["soft_preferences"]
    if state.get("household_context"):
        insights["household_context"] = state["household_context"]
    if state.get("commute_landmark"):
        insights["commute_landmark"] = state["commute_landmark"]
    if state.get("max_commute_minutes"):
        insights["max_commute_minutes"] = state["max_commute_minutes"]

    return {
        "response": final_response,
        "suggested_actions": suggested_actions,
        "insights": insights,
        "ai_mode": ai_mode,
    }
