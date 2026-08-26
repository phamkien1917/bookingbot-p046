#!/usr/bin/env python3
"""Script trace chi tiết từng bước hoạt động của Agent để debug."""

import asyncio
import sys
import json
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Tắt log nhiễu từ thư viện
logging.getLogger("asyncpg").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

from src.services.knowledge_base import get_answer, search_property_by_name
from src.agents.nodes.supervisor import supervisor_node
from src.agents.state import create_initial_agent_state
from src.agents.graph import get_agent_graph


async def trace_query(query_text: str):
    print("\n" + "="*80)
    print(f" TRACE AGENT RUN: \"{query_text}\"")
    print("="*80)

    # -------------------------------------------------------------
    # BƯỚC 1: KNOWLEDGE BASE FAST-PATH
    # -------------------------------------------------------------
    print("\n[BƯỚC 1] Kiểm tra Knowledge Base Fast-path...")
    import re
    match = re.search(r'["\'](.*?)["\']', query_text)
    extracted_quote = match.group(1) if match else None
    print(f"  -> Trích xuất ngoặc kép: {repr(extracted_quote)}")
    
    kb_res = await get_answer(query_text)
    if kb_res:
        print("  [SUCCESS] Knowledge Base tìm thấy kết quả phù hợp!")
        print("  -> Kết quả trả về:")
        print("--------------------------------------------------")
        print(kb_res)
        print("--------------------------------------------------")
    else:
        print("  [SKIP] Knowledge Base không khớp hoặc không tìm thấy.")

    # -------------------------------------------------------------
    # BƯỚC 2: PHÂN LOẠI Ý ĐỊNH & TRÍCH XUẤT ENTITIES (SUPERVISOR)
    # -------------------------------------------------------------
    print("\n[BƯỚC 2] Phân loại ý định & Trích xuất Entities (Supervisor)...")
    messages = [{"role": "user", "content": query_text}]
    state = create_initial_agent_state(session_id="trace_session", query=query_text)
    state["messages"] = messages

    supervisor_out = await supervisor_node(state)

    print(f"  -> Intent:     {supervisor_out.get('intent')}")
    print(f"  -> Confidence: {supervisor_out.get('confidence')}")
    print(f"  -> Routing:    {supervisor_out.get('current_agent')}")
    print(f"  -> Criteria:   {json.dumps(supervisor_out.get('search_criteria', {}), ensure_ascii=False, indent=6)}")

    # -------------------------------------------------------------
    # BƯỚC 3: CHẠY TOÀN BỘ AGENT GRAPH (LANGGRAPH)
    # -------------------------------------------------------------
    print("\n[BƯỚC 3] Thực thi qua LangGraph Pipeline (Supervisor -> Inventory -> Respond)...")
    state = create_initial_agent_state(session_id="trace_session", query=query_text)
    state["messages"] = messages

    graph = get_agent_graph()
    final_state = await graph.ainvoke(state)

    print(f"\n  -> Current Agent routing: {final_state.get('current_agent')}")
    print(f"  -> Search Criteria dùng để tìm DB: {json.dumps(final_state.get('search_criteria', {}), ensure_ascii=False)}")
    
    selected_props = final_state.get("selected_properties", [])
    print(f"  -> Số bất động sản tìm thấy trong PostgreSQL: {len(selected_props)}")
    for idx, prop in enumerate(selected_props[:3], 1):
        print(f"     {idx}. {prop.get('title')} | Giá: {prop.get('list_price')} | {prop.get('bedrooms')}PN | {prop.get('bathrooms')}VS | {prop.get('district')}")

    # -------------------------------------------------------------
    # BƯỚC 4: KẾT QUẢ CUỐI CÙNG TRẢ VỀ CHO USER
    # -------------------------------------------------------------
    print("\n[BƯỚC 4] Câu trả lời cuối cùng của Agent:")
    print("--------------------------------------------------")
    print(final_state.get("response", "Không có câu trả lời nào."))
    print("--------------------------------------------------")
    print("="*80 + "\n")


async def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        await trace_query(query)
    else:
        # Default test cases
        test_cases = [
            'tôi muốn xem căn nhà "Bán CC Mini Nguyễn Trãi sau Royal City, Thoáng Đẹp Nội Thất Decor Xịn" ban cho tôi xin thêm thông tin',
            'cho tôi xem căn nhà Bán căn hộ Bluegem 3 pn ,2 vs được không',
        ]
        for tc in test_cases:
            await trace_query(tc)

if __name__ == "__main__":
    asyncio.run(main())
