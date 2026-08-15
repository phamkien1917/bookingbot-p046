import asyncio
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import get_settings
from src.services.llm import get_llm


async def main() -> None:
    settings = get_settings()
    print('env_loaded', bool(settings.openrouter_api_key), settings.openrouter_api_key[:10] if settings.openrouter_api_key else None)
    print('model', settings.model_name)
    llm = get_llm()
    print('llm_model', llm.current_model)
    try:
        result = await llm.ainvoke([HumanMessage(content='Xin chao')])
        print('result', getattr(result, 'content', None))
    except Exception as exc:
        print('ERR', type(exc).__name__, exc)


if __name__ == '__main__':
    asyncio.run(main())
