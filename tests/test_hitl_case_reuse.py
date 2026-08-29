"""What happens to a coordinator case that is already open.

The case id now survives between turns, so hitl_agent is the node that has to
decide: report the queued case, deliver its decision once resolved, or open a new
one for a different request. Routing must therefore keep reaching it.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from importlib import import_module
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from src.agents.graph import _route_after_worker

# src.agents.nodes re-exports the function under this name, so reach the module itself.
hitl_module = import_module("src.agents.nodes.hitl_agent")

CASE_ID = str(uuid4())
CONTEXT = {"property_id": "prop-1", "requested_date": "2026-08-30"}


def _case(status: str, context: dict | None = None, decision: dict | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        id=CASE_ID,
        case_code="HC-EXISTING",
        status=status,
        context=context if context is not None else CONTEXT,
        decision=decision,
    )


@pytest.fixture
def hitl(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Run hitl_agent without a database; report what it tried to create."""
    created: list[dict[str, Any]] = []

    @asynccontextmanager
    async def fake_session() -> Any:
        yield None

    async def fake_create(db: Any, **kwargs: Any) -> SimpleNamespace:
        created.append(kwargs)
        return SimpleNamespace(id=uuid4(), case_code="HC-NEW", status="PENDING")

    monkeypatch.setattr(hitl_module, "get_session_context", fake_session)
    monkeypatch.setattr(hitl_module, "create_hitl_case", fake_create)
    return {"created": created, "monkeypatch": monkeypatch}


def _serve(monkeypatch: pytest.MonkeyPatch, case: SimpleNamespace | None) -> None:
    async def fake_get(db: Any, case_id: Any) -> SimpleNamespace | None:
        return case

    monkeypatch.setattr(hitl_module, "get_hitl_case", fake_get)


def test_routing_still_reaches_hitl_when_a_case_is_known() -> None:
    """The node decides what to do with the id; the edge must not decide for it."""
    state = {"awaiting_human": True, "hitl_case_id": CASE_ID}

    assert _route_after_worker(state) == "hitl"
    assert _route_after_worker({"awaiting_human": False, "hitl_case_id": CASE_ID}) == "respond"


@pytest.mark.asyncio
async def test_same_request_reports_the_queued_case(hitl: dict[str, Any]) -> None:
    _serve(hitl["monkeypatch"], _case("PENDING"))

    result = await hitl_module.hitl_agent(
        {"hitl_case_id": CASE_ID, "hitl_context": CONTEXT, "hitl_reason": "NO_SALE_AVAILABLE"}
    )

    assert hitl["created"] == []
    assert "HC-EXISTING" in result["response"]
    assert result["awaiting_human"] is True


@pytest.mark.asyncio
async def test_a_different_request_opens_its_own_case(hitl: dict[str, Any]) -> None:
    """A second property must not be folded into the case queued for the first."""
    _serve(hitl["monkeypatch"], _case("PENDING"))

    result = await hitl_module.hitl_agent(
        {
            "hitl_case_id": CASE_ID,
            "hitl_context": {"property_id": "prop-2", "requested_date": "2026-09-01"},
            "hitl_reason": "NO_SALE_AVAILABLE",
        }
    )

    assert len(hitl["created"]) == 1
    assert "HC-NEW" in result["response"]


@pytest.mark.asyncio
async def test_a_resolved_case_is_delivered_once_and_let_go(hitl: dict[str, Any]) -> None:
    _serve(hitl["monkeypatch"], _case("RESOLVED", decision={"message": "Sale Minh sẽ dẫn bạn đi xem."}))

    result = await hitl_module.hitl_agent({"hitl_case_id": CASE_ID, "hitl_context": CONTEXT})

    assert result["awaiting_human"] is False
    assert result["hitl_case_id"] is None
    assert result["response"] == "Sale Minh sẽ dẫn bạn đi xem."
