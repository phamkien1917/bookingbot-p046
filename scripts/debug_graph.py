import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.graph import get_agent_graph
from src.agents.state import create_initial_state


async def main() -> None:
    state = create_initial_state(session_id='debug', query='Xin chao')
    state['messages'] = [{'role': 'user', 'content': 'Xin chao'}]
    graph = get_agent_graph()
    result = await graph.ainvoke(state)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
