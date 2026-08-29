"""What one chat turn must hand to the next.

A booking conversation is several turns long, so the shortlist and any open
coordinator case have to survive turns that are about neither. Both used to be
dropped: a single FALLBACK turn wiped the shortlist, and the HITL case id was
rebuilt as None every turn, so repeating a request opened a second case.

The graph is replaced here, so these run without a database or an LLM.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.api import routes as routes_module
from src.api.routes import auth as auth_module
from src.database import get_session
from src.main import app

PROPERTY = {
    "id": "11111111-1111-1111-1111-111111111111",
    "title": "Chung cư Q7 Saigon Riverside",
    "price": 3_100_000_000,
}


@pytest.fixture
def client() -> Any:
    async def _no_db() -> Any:
        yield None

    app.dependency_overrides[get_session] = _no_db
    app.dependency_overrides[auth_module.get_optional_current_user] = lambda: None
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def _record_turns(monkeypatch: pytest.MonkeyPatch, replies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Replace the graph with canned replies and keep the state each turn was given."""
    seen: list[dict[str, Any]] = []

    async def fake_run_agent(state: dict[str, Any], on_stage: Any = None) -> dict[str, Any]:
        seen.append(dict(state))
        return {**state, **replies[len(seen) - 1]}

    monkeypatch.setattr(routes_module, "run_agent", fake_run_agent)
    return seen


def _say(client: TestClient, session_id: str, message: str) -> None:
    res = client.post(
        "/api/v1/chat",
        json={"message": message, "session_id": session_id},
        headers={"X-Session-ID": session_id},
    )
    assert res.status_code == 200, res.text


def test_shortlist_survives_a_turn_that_is_not_about_properties(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A FALLBACK turn between search and booking must not empty the shortlist."""
    seen = _record_turns(
        monkeypatch,
        [
            {
                "response": "Nera tìm được 1 căn.",
                "response_kind": "SEARCH_RESULTS",
                "intent": "SEARCH_PROPERTY",
                "selected_properties": [PROPERTY],
                "search_results": [PROPERTY],
                "current_property_id": PROPERTY["id"],
            },
            # The supervisor could not classify this one — exactly what happens when
            # the provider fails and the regex heuristic answers instead.
            {
                "response": "Bạn muốn xem căn nào?",
                "response_kind": "DIRECT",
                "intent": "FALLBACK",
                "selected_properties": [],
                "search_results": [],
                "current_property_id": None,
            },
            {"response": "ok", "response_kind": "DIRECT", "intent": "BOOK_APPOINTMENT"},
        ],
    )

    session_id = str(uuid.uuid4())
    _say(client, session_id, "tìm căn hộ Quận 7")
    _say(client, session_id, "vậy 2h chiều mai đi")
    _say(client, session_id, "căn số 1 lúc nãy ấy")

    assert seen[2]["selected_properties"] == [PROPERTY]


def test_an_open_coordinator_case_is_carried_into_the_next_turn(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Repeating a request must reach the same HITL case, not open a second one."""
    seen = _record_turns(
        monkeypatch,
        [
            {
                "response": "Yêu cầu cần điều phối viên kiểm tra.",
                "response_kind": "DIRECT",
                "intent": "BOOK_APPOINTMENT",
                "awaiting_human": True,
                "hitl_case_id": "22222222-2222-2222-2222-222222222222",
            },
            {"response": "ok", "response_kind": "DIRECT", "intent": "BOOK_APPOINTMENT"},
        ],
    )

    session_id = str(uuid.uuid4())
    _say(client, session_id, "chủ nhật tuần này 12h trưa")
    _say(client, session_id, "chủ nhật tuần này 12h trưa")

    assert seen[1]["hitl_case_id"] == "22222222-2222-2222-2222-222222222222"
