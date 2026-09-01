"""Token accounting: the measurement that unblocks the whole Cost axis.

Before this, cost per conversation could only be modelled by hand because nobody
read the `usage` block providers already send back. These tests pin the two
things that make the counter trustworthy: it reads both provider shapes, and one
turn's numbers never leak into another's.
"""

import asyncio
from types import SimpleNamespace

from src.services import token_usage


def langchain_style(input_tokens: int, output_tokens: int, cached: int = 0):
    """What LangChain normalises most providers into."""
    return SimpleNamespace(
        usage_metadata={
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_token_details": {"cache_read": cached},
        }
    )


def openai_style(prompt: int, completion: int, cached: int = 0):
    """The raw OpenAI-shaped block some OpenRouter models pass through unchanged."""
    return SimpleNamespace(
        usage_metadata=None,
        response_metadata={
            "token_usage": {
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "prompt_tokens_details": {"cached_tokens": cached},
            }
        },
    )


def test_reads_the_langchain_shape():
    token_usage.start()
    token_usage.record(langchain_style(1500, 300, cached=1200), "gpt-4o-mini")

    snapshot = token_usage.snapshot()
    assert snapshot["input_tokens"] == 1500
    assert snapshot["output_tokens"] == 300
    assert snapshot["cached_input_tokens"] == 1200
    assert snapshot["total_tokens"] == 1800
    assert snapshot["llm_calls"] == 1


def test_reads_the_raw_openai_shape():
    """OpenRouter does not normalise every model, so both shapes have to work."""
    token_usage.start()
    token_usage.record(openai_style(900, 120, cached=400), "gpt-4o-mini")

    snapshot = token_usage.snapshot()
    assert snapshot["input_tokens"] == 900
    assert snapshot["output_tokens"] == 120
    assert snapshot["cached_input_tokens"] == 400


def test_one_turn_sums_every_node_that_called_a_model():
    """A turn fans out over supervisor, inventory and respond."""
    token_usage.start()
    token_usage.record(langchain_style(1200, 200), "gpt-4o-mini")
    token_usage.record(langchain_style(2500, 350), "gpt-4o-mini")
    token_usage.record(langchain_style(800, 400), "gpt-4o-mini")

    snapshot = token_usage.snapshot()
    assert snapshot["llm_calls"] == 3
    assert snapshot["input_tokens"] == 4500
    assert snapshot["output_tokens"] == 950
    assert snapshot["models"] == ["gpt-4o-mini"], "one model used three times is still one model"


def test_a_result_without_usage_is_skipped_not_guessed():
    """A missing number beats an invented one."""
    token_usage.start()
    token_usage.record(SimpleNamespace(usage_metadata=None, response_metadata={}), "x")

    assert token_usage.snapshot()["llm_calls"] == 0


def test_a_broken_result_never_breaks_the_answer():
    """A metering bug must not cost the customer their reply."""
    class Hostile:
        @property
        def usage_metadata(self):
            raise RuntimeError("provider changed shape")

    token_usage.start()
    token_usage.record(Hostile(), "x")  # must not raise

    assert token_usage.snapshot()["llm_calls"] == 0


def test_recording_before_start_is_a_no_op():
    """Background jobs call the LLM outside any request."""
    token_usage._usage.set(None)
    token_usage.record(langchain_style(100, 100), "x")

    assert token_usage.snapshot()["total_tokens"] == 0


async def test_two_concurrent_turns_do_not_blend():
    """The LLM client is a shared singleton; the counter must not be."""

    async def turn(input_tokens: int, output_tokens: int) -> dict:
        token_usage.start()
        token_usage.record(langchain_style(input_tokens, output_tokens), "gpt-4o-mini")
        await asyncio.sleep(0)  # force interleaving
        token_usage.record(langchain_style(input_tokens, output_tokens), "gpt-4o-mini")
        return token_usage.snapshot()

    small, large = await asyncio.gather(turn(100, 10), turn(9000, 900))

    assert small["input_tokens"] == 200, "a big conversation leaked into a small one"
    assert large["input_tokens"] == 18000
