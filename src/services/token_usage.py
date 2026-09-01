"""Per-request token accounting for the LLM calls a single turn makes.

Cost per conversation was the one axis of Accuracy–Performance–Cost that could
not be measured at all: nothing read the `usage` block providers already return,
so every cost figure the team had was a hand-built model rather than an
observation.

The counter lives in a ContextVar rather than on the LLM singleton. One turn
fans out across several nodes and several LLM calls, and the server handles
turns concurrently on one shared client, so an instance attribute would blend
two customers' conversations together.
"""

from __future__ import annotations

import logging
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

logger = logging.getLogger(__name__)


@dataclass
class TokenUsage:
    """What one turn spent, summed across every node that called a model."""

    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    calls: int = 0
    models: list[str] = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def as_dict(self) -> dict[str, Any]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "total_tokens": self.total_tokens,
            "llm_calls": self.calls,
            "models": self.models,
        }


_usage: ContextVar[TokenUsage | None] = ContextVar("nera_token_usage", default=None)


def start() -> TokenUsage:
    """Begin counting for one turn. Safe to call again; the old total is dropped."""
    usage = TokenUsage()
    _usage.set(usage)
    return usage


def current() -> TokenUsage | None:
    return _usage.get()


def snapshot() -> dict[str, Any]:
    """What has been spent so far, or zeros when nobody called start()."""
    usage = _usage.get()
    return usage.as_dict() if usage else TokenUsage().as_dict()


def extract(result: Any) -> tuple[int, int, int] | None:
    """Pull (input, output, cached) out of whatever the provider handed back.

    LangChain normalises most providers into `usage_metadata`, but OpenRouter
    passes some models through with only the raw OpenAI-shaped block, so both
    shapes are read before giving up. Returning None means this call is simply
    not counted — an unusable number is worse than a missing one.
    """
    meta = getattr(result, "usage_metadata", None)
    if isinstance(meta, dict) and meta.get("input_tokens") is not None:
        details = meta.get("input_token_details") or {}
        return (
            int(meta.get("input_tokens") or 0),
            int(meta.get("output_tokens") or 0),
            int(details.get("cache_read") or 0),
        )

    response_meta = getattr(result, "response_metadata", None)
    if isinstance(response_meta, dict):
        raw = response_meta.get("token_usage") or response_meta.get("usage") or {}
        if isinstance(raw, dict) and raw.get("prompt_tokens") is not None:
            details = raw.get("prompt_tokens_details") or {}
            return (
                int(raw.get("prompt_tokens") or 0),
                int(raw.get("completion_tokens") or 0),
                int(details.get("cached_tokens") or 0),
            )
    return None


def record(result: Any, model: str | None = None) -> None:
    """Add one LLM call to this turn's total. Never raises into the caller."""
    usage = _usage.get()
    if usage is None:
        return
    try:
        counted = extract(result)
    except Exception:  # a metering bug must not break a customer's answer
        logger.debug("Could not read token usage from %s", type(result).__name__)
        return
    if counted is None:
        return
    input_tokens, output_tokens, cached = counted
    usage.input_tokens += input_tokens
    usage.output_tokens += output_tokens
    usage.cached_input_tokens += cached
    usage.calls += 1
    if model and model not in usage.models:
        usage.models.append(model)


class UsageCallback(BaseCallbackHandler):
    """Count tokens from the provider event rather than the return value.

    `ainvoke` hands back an AIMessage that carries usage, but
    `with_structured_output` hands back the parsed schema object, which carries
    nothing — so reading return values missed every supervisor call. The
    callback fires for both, because it sits at the model boundary.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        usage = _usage.get()
        if usage is None:
            return
        try:
            raw = (getattr(response, "llm_output", None) or {}).get("token_usage") or {}
            if not raw:
                # Some providers only fill the per-generation message.
                for generations in getattr(response, "generations", []) or []:
                    for generation in generations:
                        message = getattr(generation, "message", None)
                        counted = extract(message) if message is not None else None
                        if counted:
                            _add(usage, *counted, self.model)
                            return
                return
            details = raw.get("prompt_tokens_details") or {}
            _add(
                usage,
                int(raw.get("prompt_tokens") or 0),
                int(raw.get("completion_tokens") or 0),
                int(details.get("cached_tokens") or 0),
                self.model,
            )
        except Exception:  # metering must never break a customer's answer
            logger.debug("Could not read token usage from an on_llm_end event")


def _add(usage: TokenUsage, input_tokens: int, output_tokens: int, cached: int, model: str | None) -> None:
    usage.input_tokens += input_tokens
    usage.output_tokens += output_tokens
    usage.cached_input_tokens += cached
    usage.calls += 1
    if model and model not in usage.models:
        usage.models.append(model)
