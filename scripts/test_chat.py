#!/usr/bin/env python3
"""Script test chat truc tiep de debug."""

__test__ = False  # Debug CLI, not a pytest module.

import asyncio
import logging
import sys
import time
import traceback
from pathlib import Path

from langchain_core.messages import HumanMessage

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from src.agents.graph import get_agent_graph  # noqa: E402
from src.agents.state import create_initial_agent_state  # noqa: E402
from src.services.knowledge_base import get_answer  # noqa: E402
from src.services.llm import get_llm, reset_llm  # noqa: E402


async def test_single_message(message: str):
    """Test mot message don le."""
    print(f"\n{'='*60}")
    print(f"[TEST] {message}")
    print(f"{'='*60}")

    # Reset LLM de dung model dau tien
    reset_llm()

    # Create state
    state = create_initial_agent_state(
        session_id="test-session-001",
        query=message,
    )
    state["messages"] = [{"role": "user", "content": message}]

    print(f"\n[INIT] State keys: {list(state.keys())}")
    print(f"[INIT] Intent: {state.get('intent')}")
    print(f"[INIT] Next action: {state.get('next_action')}")

    # Run agent
    print("\n[RUN] Running agent...")
    start = time.time()

    try:
        graph = get_agent_graph()
        result = await graph.ainvoke(state)

        elapsed = time.time() - start
        print(f"\n[OK] Time elapsed: {elapsed:.2f}s")

        print(f"\n[RESULT] Keys: {list(result.keys())}")
        resp = result.get('response', '')
        if resp:
            print(f"[RESULT] Response: {resp[:200]}...")
        else:
            print("[RESULT] Response: EMPTY")
        print(f"[RESULT] Error: {result.get('error')}")
        print(f"[RESULT] Intent: {result.get('intent')}")
        print(f"[RESULT] Next action: {result.get('next_action')}")
        print(f"[RESULT] Current agent: {result.get('current_agent')}")

        # Check messages
        messages = result.get("messages", [])
        print(f"\n[RESULT] Messages count: {len(messages)}")
        for i, msg in enumerate(messages[-3:]):
            role = msg.get("role", "?")
            content = msg.get("content", "")[:100]
            print(f"   {i+1}. [{role}]: {content}...")

        return result

    except Exception as e:
        elapsed = time.time() - start
        print(f"\n[FAIL] Error after {elapsed:.2f}s: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None


async def test_llm_direct(message: str):
    """Test LLM truc tiep."""
    print(f"\n{'='*60}")
    print(f"[LLM] Direct: {message}")
    print(f"{'='*60}")

    reset_llm()
    llm = get_llm()

    print(f"\n[LLM] Model: {llm.model_name}")

    try:
        start = time.time()

        result = await llm.ainvoke([HumanMessage(content=message)])

        elapsed = time.time() - start
        print(f"\n[LLM] Time: {elapsed:.2f}s")
        content = result.content if hasattr(result, 'content') else result
        print(f"[LLM] Result: {content[:200]}...")

        return result

    except Exception as e:
        elapsed = time.time() - start
        print(f"\n[LLM-FAIL] Error after {elapsed:.2f}s: {type(e).__name__}: {e}")
        return None


async def test_knowledge_base(message: str):
    """Test knowledge base."""
    print(f"\n{'='*60}")
    print(f"[KB] Testing: {message}")
    print(f"{'='*60}")

    start = time.time()

    result = await get_answer(message)

    elapsed = time.time() - start
    print(f"\n[KB] Time: {elapsed*1000:.0f}ms")
    if result:
        # Remove emoji for console
        result_clean = result.encode('ascii', 'replace').decode('ascii')
        print(f"[KB] Result: {result_clean[:100]}...")
    else:
        print("[KB] Result: None")

    return result


async def main():
    """Main test."""
    print("\n" + "="*60)
    print("DEBUG SCRIPT - Testing Chat Flow")
    print("="*60)

    test_messages = [
        "Xin chao",
        "CCMN 13 o dau",
        "Doanh thu o dau",
        "Toi muon tim can ho 2 phong ngu o quan 7",
    ]

    # Test knowledge base first
    print("\n\n" + "="*60)
    print("TESTING KNOWLEDGE BASE")
    print("="*60)

    for msg in test_messages:
        await test_knowledge_base(msg)

    # Test LLM direct
    print("\n\n" + "="*60)
    print("TESTING LLM DIRECT")
    print("="*60)

    for msg in test_messages[:2]:
        await test_llm_direct(msg)

    # Test full agent
    print("\n\n" + "="*60)
    print("TESTING FULL AGENT")
    print("="*60)

    for msg in test_messages[:2]:
        await test_single_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
