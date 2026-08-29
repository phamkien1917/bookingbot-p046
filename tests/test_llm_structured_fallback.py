"""Structured-output calls must fall back to the next model, like plain calls do.

OpenRouter answers a struggling upstream with HTTP 200 and a body of just
{"error": ...}; the OpenAI SDK then raises TypeError on the missing `choices`.
The supervisor used to build its own chat model, so that error ended the call and
the turn was classified by a regex heuristic instead.
"""

from __future__ import annotations

from typing import Any

import pytest

from src.services.llm import OpenRouterLLM


class _Model:
    """Stands in for a chat model: either raises or returns a canned answer."""

    def __init__(self, error: Exception | None, answer: Any = None) -> None:
        self._error = error
        self._answer = answer
        self.tried = False

    def with_structured_output(self, schema: type, **kwargs: Any) -> _Model:
        return self

    async def ainvoke(self, messages: list[Any]) -> Any:
        self.tried = True
        if self._error:
            raise self._error
        return self._answer


def _llm(monkeypatch: pytest.MonkeyPatch, models: list[_Model]) -> OpenRouterLLM:
    llm = OpenRouterLLM()
    llm.models = ["model-a", "model-b", "model-c"]
    llm.current_model_index = 0
    llm.current_model = "model-a"
    calls = iter(models)
    monkeypatch.setattr(llm, "_create_chat_model", lambda: next(calls))
    return llm


@pytest.mark.asyncio
async def test_falls_through_to_a_model_that_answers(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = _llm(
        monkeypatch,
        [
            _Model(TypeError("'NoneType' object is not iterable")),
            _Model(None, {"intent": "BOOK_APPOINTMENT"}),
        ],
    )

    result = await llm.ainvoke_structured(dict, [])

    assert result == {"intent": "BOOK_APPOINTMENT"}
    assert llm.model_name == "model-b"


@pytest.mark.asyncio
async def test_raises_once_every_model_has_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    """The caller still gets an error when nothing works — it just is not the first one."""
    models = [_Model(TypeError("upstream overloaded")) for _ in range(3)]
    llm = _llm(monkeypatch, models)

    with pytest.raises(TypeError):
        await llm.ainvoke_structured(dict, [])

    # Every model in the list was tried before giving up, not just the first.
    assert all(model.tried for model in models)
