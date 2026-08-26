"""MODEL_NAME must decide which model actually runs.

The selection used to leave the index at 0 whenever MODEL_NAME was absent from
MODEL_PRIORITY, so an unrecognised name silently served the first free model
instead. Combined with the hard-coded ai_model label in the response, nothing
would reveal that the configured model never ran.
"""

from unittest.mock import patch

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
