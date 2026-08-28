"""MODEL_NAME must decide which model actually runs.

The selection used to leave the index at 0 whenever MODEL_NAME was absent from
MODEL_PRIORITY, so an unrecognised name silently served the first free model
instead. Combined with the hard-coded ai_model label in the response, nothing
would reveal that the configured model never ran.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from src.agents.state import Intent
from src.services.llm import OpenRouterLLM
from src.services.models import MODEL_PRIORITY


def _llm(model_name: str) -> OpenRouterLLM:
    with patch("src.services.llm.get_settings") as settings:
        settings.return_value.model_name = model_name
        settings.return_value.openrouter_api_key = "test-key"
        settings.return_value.openai_api_key = ""
        return OpenRouterLLM()


def test_a_known_model_starts_at_its_own_position() -> None:
    llm = _llm("openai/gpt-4o-mini")

    assert llm.models[llm.current_model_index] == "openai/gpt-4o-mini"
    assert llm.models is MODEL_PRIORITY


def test_the_rest_of_the_list_stays_available_as_fallbacks() -> None:
    llm = _llm("openai/gpt-4o-mini")

    remaining = llm.models[llm.current_model_index + 1 :]
    assert remaining, "a configured model must still have somewhere to fall back to"


def test_an_unknown_model_is_used_instead_of_being_swapped_out() -> None:
    llm = _llm("deepseek/deepseek-chat")

    assert llm.models[llm.current_model_index] == "deepseek/deepseek-chat"
    assert llm.models[llm.current_model_index] != MODEL_PRIORITY[0]


def test_an_unknown_model_keeps_the_known_list_behind_it() -> None:
    llm = _llm("some-vendor/some-model")

    assert llm.models[0] == "some-vendor/some-model"
    assert llm.models[1:] == list(MODEL_PRIORITY)


def test_an_explicit_preferred_model_wins_over_settings() -> None:
    with patch("src.services.llm.get_settings") as settings:
        settings.return_value.model_name = "openai/gpt-4o-mini"
        settings.return_value.openrouter_api_key = "test-key"
        settings.return_value.openai_api_key = ""
        llm = OpenRouterLLM(preferred_model="anthropic/claude-3.5-sonnet")

    assert llm.models == ["anthropic/claude-3.5-sonnet"]


def test_direct_openai_ignores_the_openrouter_list() -> None:
    with patch("src.services.llm.get_settings") as settings:
        settings.return_value.model_name = "nvidia/nemotron-3-ultra-550b-a55b:free"
        settings.return_value.openrouter_api_key = ""
        settings.return_value.openai_api_key = "sk-test"
        llm = OpenRouterLLM()

    assert llm.is_direct_openai
    assert llm.models == ["gpt-4o-mini", "gpt-4o"]


@pytest.mark.asyncio
async def test_respond_node_reports_the_model_that_answered() -> None:
    """The response must name the model that ran, not a hard-coded label.

    supervisor.py used to set ai_model = "gpt-4o-mini" and never reassign it,
    so every turn claimed OpenAI even while OpenRouter served the answer.
    """
    from src.agents.nodes.respond_node import respond_node

    class FakeLLM:
        model_name = "nvidia/nemotron-3-ultra-550b-a55b:free"

        async def ainvoke(self, messages):
            return SimpleNamespace(content="Chào bạn!")

    with patch("src.agents.nodes.respond_node.get_llm", return_value=FakeLLM()):
        result = await respond_node({
            "query": "xin chào",
            "intent": Intent.GREETING,
            "messages": [],
            "response": "",
        })

    assert result["ai_model"] == "nvidia/nemotron-3-ultra-550b-a55b:free"


@pytest.mark.asyncio
async def test_no_model_is_claimed_when_the_llm_never_ran() -> None:
    """A heuristic answer must not borrow a model name it did not use."""
    from src.agents.nodes.respond_node import respond_node

    result = await respond_node({
        "query": "xin chào",
        "intent": Intent.GREETING,
        "messages": [],
        "response": "",
        "direct_response": "Chào bạn, mình là Nera.",
    })

    assert result["ai_model"] is None
