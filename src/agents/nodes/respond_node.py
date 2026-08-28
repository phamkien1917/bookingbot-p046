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
- Am hiểu phong thủy & kiến trúc ứng dụng thực tế (các hướng nhà Đông/Tây/Nam/Bắc/Đông Nam/Tây Bắc, đón gió nồm, tránh nắng gắt, thông gió, cảnh quan, ban công).
- Thấu hiểu hoàn cảnh khách hàng (gia đình có con nhỏ cần gần trường, người đi làm cần tiện đường, người đầu tư cần tiềm năng sinh lời).

Nguyên tắc phản hồi:
1. Đối với các câu hỏi kiến thức bất động sản / tư vấn chuyên môn / so sánh khái niệm (ví dụ: so sánh các hướng nhà, so sánh chung cư và nhà đất, so sánh sổ đỏ và sổ hồng, quy trình mua nhà...): Hãy phân tích chuyên sâu, toàn diện và thực tế (ưu nhược điểm, ánh sáng, nhiệt độ, phong thủy, đối tượng phù hợp, giải pháp khắc phục...).
2. Đối với câu hỏi về căn nhà cụ thể trong giỏ hàng: Tuyệt đối không bịa đặt các thông số kỹ thuật (giá, diện tích, phòng) nếu không có trong dữ liệu.
3. Trả lời mạch lạc, dễ hiểu, dùng Markdown đẹp mắt (bảng so sánh, bullet points, in đậm các ý chính, dùng emoji tinh tế).
4. Luôn kết thúc bằng một câu gợi mở tự nhiên hoặc hỏi nhu cầu tiếp theo để hỗ trợ khách hàng tốt nhất.
5. Nếu người dùng hỏi các câu hỏi hoàn toàn ngoài lề (thời tiết, làm thơ, viết code...), hãy trả lời ngắn gọn, lịch sự và khéo léo kết nối lại về chủ đề nhà đất.
"""

_CONVERSATIONAL_INTENTS = {
    Intent.CONSULTATION_QA,
    Intent.GREETING,
    Intent.THANKS,
    Intent.GOODBYE,
    Intent.OUT_OF_SCOPE,
    Intent.FALLBACK,
}


async def respond_node(state: AgentState) -> dict[str, Any]:
    """Respond node: ensures a natural, high-quality, persona-aligned response is generated."""
    existing_response = state.get("response", "").strip()
    intent = state.get("intent")
    query = state.get("query", "")
    history = state.get("messages", [])
    direct_response = state.get("direct_response")

    final_response = existing_response
    ai_mode = state.get("ai_mode", "llm_grounded")
    ai_model = state.get("ai_model")
    affordability_note = state.get("affordability_note")

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

            # Money answers are computed, never improvised. When the turn carries a
            # worked affordability figure, the model must quote it rather than run
            # its own arithmetic on the customer's income.
            affordability_note = state.get("affordability_note")
            if affordability_note:
                context_info["affordability_analysis"] = affordability_note

            try:
                llm = get_llm()
                system_prompt = NERA_PERSONA_PROMPT
                if affordability_note:
                    # Kept in the leading system message: a trailing one is ignored
                    # by several providers, and this rule must not be optional.
                    system_prompt += (
                        "\n\nQUY TẮC BẮT BUỘC VỀ TIỀN: ngữ cảnh có trường affordability_analysis "
                        "đã được hệ thống tính sẵn bằng công thức tài chính. Hãy dùng đúng các con số "
                        "trong đó và giữ nguyên phần nêu giả định. TUYỆT ĐỐI không tự tính lại khoản vay, "
                        "tiền trả góp hay tầm giá từ thu nhập của khách."
                    )
                if intent == Intent.CONSULTATION_QA:
                    system_prompt += (
                        "\n\nBẠN ĐANG TRẢ LỜI CÂU HỎI TƯ VẤN KIẾN THỨC BẤT ĐỘNG SẢN / SO SÁNH KHÁI NIỆM:\n"
                        "- Vận dụng kiến thức chuyên môn bất động sản để giải đáp, phân tích chi tiết và so sánh toàn diện các mặt "
                        "(ánh sáng, nhiệt độ, gió mùa, phong thủy, pháp lý, kiến trúc vi khí hậu Việt Nam, ưu/nhược điểm, lời khuyên thực tế...).\n"
                        "- Trả lời trực tiếp và đầy đủ vào câu hỏi của khách hàng ngay lập tức.\n"
                        "- TUYỆT ĐỐI KHÔNG hỏi ngược lại hay yêu cầu khách cung cấp thêm thông số kỹ thuật (như giá, diện tích, số phòng) "
                        "nếu khách đang hỏi về kiến thức chung hoặc so sánh hướng nhà / loại hình / pháp lý."
                    )
                    human_content = (
                        f"Câu hỏi của khách hàng: \"{query}\"\n\n"
                        "Hãy trả lời chi tiết, khoa học, có cấu trúc rõ ràng (dùng Markdown, bullet points) và đưa ra lời khuyên chuyên gia:"
                    )
                    if affordability_note:
                        human_content = (
                            f"Phân tích tài chính đã tính toán:\n{affordability_note}\n\n"
                            f"Câu hỏi của khách: \"{query}\"\n\n"
                            "Hãy trả lời tư vấn cho khách dựa trên phân tích trên:"
                        )
                else:
                    human_content = (
                        f"Ngữ cảnh hiện tại:\n{json.dumps(context_info, ensure_ascii=False)}\n\n"
                        f"Tin nhắn mới của khách: \"{query}\"\n\n"
                        "Hãy trả lời khách hàng một cách xuất sắc, tận tâm và tự nhiên nhất:"
                    )

                prompt_messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_content),
                ]
                res = await llm.ainvoke(prompt_messages)
                final_response = res.content if hasattr(res, "content") else str(res)
                ai_mode = "llm_direct"
                ai_model = llm.model_name
            except Exception as e:
                logger.error(f"Error in LLM response generation: {e}")
                if not final_response:
                    final_response = (
                        "Chào bạn, mình là Nera! Mình có thể hỗ trợ bạn tìm kiếm bất động sản phù hợp, "
                        "xem thông tin chi tiết và đặt lịch xem nhà trực tiếp với chuyên viên Sale. "
                        "Bạn đang quan tâm đến khu vực hoặc phân khúc nào?"
                    )
                ai_mode = "fallback"

    # Derive smart contextual suggested actions (Quick Replies)
    suggested_actions: list[str] = []
    mem_summary = state.get("memory_summary", "")

    if intent == Intent.GREETING:
        if mem_summary:
            suggested_actions.append(f"Tiếp tục: {mem_summary[:28]}...")
        suggested_actions.extend([
            "Tìm căn hộ Quận 7",
            "Tìm nhà riêng Hà Nội",
            "Tư vấn mua nhà lần đầu",
        ])
    elif intent == Intent.CONSULTATION_QA:
        if affordability_note and "Phương án vay" in affordability_note:
            suggested_actions = [
                "Thử vay trong 10 năm",
                "Thử vay trong 15 năm",
                "Tìm nhà phù hợp tầm tài chính này",
            ]
        elif affordability_note:
            suggested_actions = [
                "Tính thử phương án vay",
                "Tìm bất động sản phù hợp",
                "Quy trình đặt cọc an toàn",
            ]
        else:
            suggested_actions = [
                "Tìm bất động sản phù hợp",
                "Tính thử phương án vay",
                "Quy trình đặt cọc an toàn",
            ]
    elif intent == Intent.FALLBACK:
        max_p = state.get("search_criteria", {}).get("max_price")
        if (
            max_p
            and max_p < 100_000_000
            and state.get("search_criteria", {}).get("transaction_type") == "SALE"
        ):
            from src.services.affordability import format_vnd
            suggested_actions = [
                f"Tìm thuê căn hộ {format_vnd(max_p)}/tháng",
                f"Tìm mua căn hộ {format_vnd(max_p * 1000)}",
                "Tư vấn ngân sách mua nhà",
            ]
        else:
            suggested_actions = [
                "Tìm căn hộ chung cư",
                "Tìm nhà riêng",
                "Tư vấn chọn nhà",
            ]
    elif intent == Intent.OUT_OF_SCOPE:
        suggested_actions = [
            "Tìm căn hộ chung cư",
            "Tìm nhà phố liền kề",
            "Kiểm tra lịch xem nhà",
        ]
    elif state.get("suggested_actions"):
        suggested_actions = list(state["suggested_actions"])
    elif (
        state.get("phase") == "SEARCH_NO_RESULTS"
        or (not state.get("selected_properties") and intent == Intent.SEARCH_PROPERTY)
    ):
        suggested_actions = [
            "Mở rộng khu vực tìm kiếm",
            "Điều chỉnh khoảng ngân sách",
            "Xem tất cả căn đang có",
        ]
    elif state.get("selected_properties"):
        count = len(state["selected_properties"])
        suggested_actions = [f"Chọn căn số {i}" for i in range(1, min(count + 1, 4))]
        if count >= 2:
            suggested_actions.append("So sánh các căn này")
    else:
        suggested_actions = ["Tìm căn hộ", "Tìm nhà phố", "Đặt lịch xem nhà"]

    # Build insights dictionary for frontend sidebar
    criteria = state.get("search_criteria", {})
    insights: dict[str, Any] = {
        key: val for key, val in criteria.items() if val not in (None, "", [])
    }
    if state.get("soft_preferences"):
        insights["soft_preferences"] = state["soft_preferences"]
    if state.get("nearby_categories"):
        insights["nearby_categories"] = state["nearby_categories"]
    if state.get("household_context"):
        insights["household_context"] = state["household_context"]
    if state.get("commute_landmark"):
        insights["commute_landmark"] = state["commute_landmark"]
    if state.get("max_commute_minutes"):
        insights["max_commute_minutes"] = state["max_commute_minutes"]

    result: dict[str, Any] = {
        "response": final_response,
        "suggested_actions": suggested_actions,
        "insights": insights,
        "ai_mode": ai_mode,
        "ai_model": ai_model,
    }

    # Clear selected_properties if purely conversational to avoid leaking property cards
    if intent in _CONVERSATIONAL_INTENTS:
        result["selected_properties"] = []

    return result
