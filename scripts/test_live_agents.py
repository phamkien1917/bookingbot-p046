"""Comprehensive Live Multi-Turn Chatbot Test Script.

Tests all major scenarios against the LangGraph multi-agent system:
1. Greeting & persona
2. Property search with criteria extraction
3. Multi-turn search refinement (budget, bedrooms)
4. Property selection & details (anaphora resolution)
5. Comparison matrix
6. Consultation QA (real estate procedures & bank loan)
7. Out-of-scope handling
8. Booking & scheduling flow (guest auth gating)
9. Thanks & Goodbye
"""

import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding="utf-8")

from src.agents import create_initial_agent_state, run_agent
from src.database.models import UserRole


async def run_scenario(scenario_name: str, turns: list[str]):
    print("\n" + "=" * 80)
    print(f"🎬 SCENARIO: {scenario_name}")
    print("=" * 80)

    session_id = str(uuid.uuid4())
    history = []
    metadata = {"chat_state": {}, "insights": {}}

    for i, user_msg in enumerate(turns, 1):
        print(f"\n👤 [Turn {i}] User: {user_msg}")

        state = create_initial_agent_state(
            session_id=session_id,
            query=user_msg,
            customer_id=None,
            customer_role=None,
            history=history,
            metadata=metadata,
        )

        res_state = await run_agent(state)

        bot_reply = res_state.get("response", "")
        intent = res_state.get("intent")
        phase = res_state.get("phase")
        ai_mode = res_state.get("ai_mode")
        props_count = len(res_state.get("selected_properties", []))
        quick_replies = res_state.get("suggested_actions", [])

        print(f"🤖 Nera (Intent: {intent} | Phase: {phase} | Mode: {ai_mode} | Props: {props_count}):")
        print(f"--- Response ---")
        print(bot_reply)
        print(f"--- Quick Replies: {quick_replies} ---")

        # Update conversation history & state for next turn
        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": bot_reply})

        metadata["chat_state"] = {
            "criteria": res_state.get("search_criteria", {}),
            "soft_preferences": res_state.get("soft_preferences", []),
            "household_context": res_state.get("household_context", []),
            "commute_landmark": res_state.get("commute_landmark"),
            "max_commute_minutes": res_state.get("max_commute_minutes"),
            "property_refs": res_state.get("selected_properties", []),
            "selected_property_id": res_state.get("current_property_id"),
            "selected_property_index": res_state.get("selected_property_index"),
            "requested_date": res_state.get("requested_date"),
            "requested_hour": res_state.get("requested_hour"),
            "slots": res_state.get("selected_slots", []),
            "selected_slot_index": res_state.get("selected_slot_index"),
            "active_request_id": res_state.get("active_request_id"),
            "active_request_code": res_state.get("active_request_code"),
            "pending_action": res_state.get("pending_action"),
            "phase": res_state.get("phase", "IDLE"),
        }
        metadata["insights"] = res_state.get("insights", {})


async def main():
    # Scenario 1: Multi-turn Property Journey
    await run_scenario(
        "Tìm kiếm -> Tinh chỉnh -> Xem chi tiết -> So sánh",
        [
            "Chào bạn, tôi đang tìm căn hộ ở Quận 7",
            "Ngân sách tầm 4 đến 8 tỷ, có 2 phòng ngủ cho gia đình có con nhỏ",
            "Nới ngân sách lên 10 tỷ xem có căn nào đẹp hơn không",
            "Chọn căn số 1",
            "Căn đó diện tích bao nhiêu và có mấy phòng tắm?",
            "So sánh căn 1 với các căn khác vừa tìm được",
        ],
    )

    # Scenario 2: Real Estate Consultation & Out of Scope
    await run_scenario(
        "Tư vấn chuyên môn BĐS + Xử lý câu hỏi ngoài lề",
        [
            "Tôi muốn mua nhà lần đầu thì cần chuẩn bị những thủ tục pháp lý gì?",
            "Nếu vay ngân hàng 70% thì lãi suất và phương án trả góp tính thế nào?",
            "Thời tiết hôm nay ở Sài Gòn thế nào bạn?",
            "Cảm ơn em nhiều nha!",
            "Tạm biệt nhé",
        ],
    )

    # Scenario 3: Booking Flow (Guest -> Auth requirement)
    await run_scenario(
        "Đặt lịch xem nhà (Khách vãng lai)",
        [
            "Tìm căn hộ ở Quận 7 dưới 8 tỷ",
            "Chọn căn số 1, tôi muốn đặt lịch xem vào 14h thứ Bảy tuần này",
            "Chọn khung giờ số 1",
        ],
    )

    # Scenario 4: Full Authenticated Booking, Status Check, and Cancellation Flow
    print("\n" + "=" * 80)
    print("🎬 SCENARIO: Đặt lịch -> Kiểm tra trạng thái -> Hủy lịch (Khách đã đăng nhập)")
    print("=" * 80)

    auth_session_id = str(uuid.uuid4())
    auth_customer_id = "10000000-0000-0000-0000-000000000004"
    auth_history = []
    auth_metadata = {"chat_state": {}, "insights": {}}

    auth_turns = [
        "Tìm căn hộ ở Quận 7",
        "Chọn căn số 1, đặt lịch vào 10h thứ Bảy tuần này",
        "Chọn khung giờ 1",
        "Kiểm tra lại lịch xem nhà của tôi",
        "Tôi bận việc đột xuất, muốn hủy lịch này",
        "Xác nhận hủy",
    ]

    for i, user_msg in enumerate(auth_turns, 1):
        print(f"\n👤 [Turn {i}] User: {user_msg}")

        state = create_initial_agent_state(
            session_id=auth_session_id,
            query=user_msg,
            customer_id=auth_customer_id,
            customer_role=UserRole.CUSTOMER,
            history=auth_history,
            metadata=auth_metadata,
        )

        res_state = await run_agent(state)

        bot_reply = res_state.get("response", "")
        intent = res_state.get("intent")
        phase = res_state.get("phase")
        ai_mode = res_state.get("ai_mode")
        props_count = len(res_state.get("selected_properties", []))
        quick_replies = res_state.get("suggested_actions", [])

        print(f"🤖 Nera (Intent: {intent} | Phase: {phase} | Mode: {ai_mode} | Props: {props_count}):")
        print(f"--- Response ---")
        print(bot_reply)
        print(f"--- Quick Replies: {quick_replies} ---")

        auth_history.append({"role": "user", "content": user_msg})
        auth_history.append({"role": "assistant", "content": bot_reply})

        auth_metadata["chat_state"] = {
            "criteria": res_state.get("search_criteria", {}),
            "soft_preferences": res_state.get("soft_preferences", []),
            "household_context": res_state.get("household_context", []),
            "commute_landmark": res_state.get("commute_landmark"),
            "max_commute_minutes": res_state.get("max_commute_minutes"),
            "property_refs": res_state.get("selected_properties", []),
            "selected_property_id": res_state.get("current_property_id"),
            "selected_property_index": res_state.get("selected_property_index"),
            "requested_date": res_state.get("requested_date"),
            "requested_hour": res_state.get("requested_hour"),
            "slots": res_state.get("selected_slots", []),
            "selected_slot_index": res_state.get("selected_slot_index"),
            "active_request_id": res_state.get("active_request_id"),
            "active_request_code": res_state.get("active_request_code"),
            "pending_action": res_state.get("pending_action"),
            "phase": res_state.get("phase", "IDLE"),
        }
        auth_metadata["insights"] = res_state.get("insights", {})


if __name__ == "__main__":
    asyncio.run(main())
