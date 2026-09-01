"""POST /api/v1/chat — the endpoint contract, with the graph replaced.

The endpoint's job is narrow: validate the request, run one turn, and turn the
final AgentState into a ChatResponse. What the model decides is out of scope
here; what matters is that a valid request comes back shaped correctly, a bad
one is refused before any work is done, and a failing turn does not hand the
caller a stack trace.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.api import routes as routes_module


@pytest.mark.asyncio
async def test_a_valid_turn_returns_the_agent_reply(client, fake_run_agent, sample_chat_request):
    reply = "Mình tìm được 3 căn 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ."

    with patch.object(routes_module, "run_agent", fake_run_agent(reply)):
        response = await client.post("/api/v1/chat", json=sample_chat_request)

    assert response.status_code == 200
    body = response.json()
    assert body["response"] == reply
    assert body["ai_mode"] in {"llm_grounded", "llm_direct", "fallback"}


@pytest.mark.asyncio
async def test_the_response_carries_the_cost_of_the_turn(client, fake_run_agent):
    """Token counts are part of the contract, not a debug extra.

    They are what makes cost per conversation measurable rather than modelled,
    so dropping them from the schema has to fail a test.
    """
    with patch.object(routes_module, "run_agent", fake_run_agent()):
        response = await client.post("/api/v1/chat", json={"message": "Xin chào"})

    body = response.json()
    for field in ("input_tokens", "output_tokens", "cached_input_tokens", "llm_calls"):
        assert field in body, f"{field} disappeared from ChatResponse"
        assert isinstance(body[field], int)


@pytest.mark.asyncio
async def test_an_empty_message_is_refused_before_the_agent_runs(client):
    """Validation comes first; an empty turn should cost nothing."""
    never_called = AsyncMock()

    with patch.object(routes_module, "run_agent", never_called):
        response = await client.post("/api/v1/chat", json={"message": ""})

    assert response.status_code == 422
    never_called.assert_not_awaited()


@pytest.mark.asyncio
async def test_an_oversized_message_is_refused(client):
    response = await client.post("/api/v1/chat", json={"message": "A" * 10001})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_a_missing_message_is_refused(client):
    response = await client.post("/api/v1/chat", json={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_a_failing_turn_does_not_leak_the_exception(client):
    """The customer gets a refusal, not the provider's error text."""
    failing = AsyncMock(side_effect=RuntimeError("OPENROUTER_API_KEY=sk-secret expired"))

    with patch.object(routes_module, "run_agent", failing):
        response = await client.post("/api/v1/chat", json={"message": "Xin chào"})

    assert response.status_code >= 500
    assert "sk-secret" not in response.text
