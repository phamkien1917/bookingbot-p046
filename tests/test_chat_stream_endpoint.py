"""The SSE chat endpoint must report real progress and still return one turn.

These run the endpoint for an anonymous visitor with the graph replaced, so the
transport contract is checked without needing a database or an LLM.
"""

from __future__ import annotations

import json
import uuid
from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.api.routes import auth as auth_module
from src.database import get_session
from src.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Any:
    async def _no_db() -> Any:
        yield None

    app.dependency_overrides[get_session] = _no_db
    app.dependency_overrides[auth_module.get_optional_current_user] = lambda: None
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def _fake_run_agent(nodes: list[str], response: str):
    async def _run(state: dict[str, Any], on_stage: Any = None) -> dict[str, Any]:
        for node in nodes:
            if on_stage:
                on_stage(node)
        return {
            **state,
            "response": response,
            "response_kind": "DIRECT",
            "intent": "GREETING",
            "ai_mode": "llm_direct",
            "ai_model": "test-model",
            "ai_latency_ms": 5,
            "suggested_actions": [],
        }

    return _run


def _read_events(client: TestClient, message: str) -> list[tuple[str, dict[str, Any]]]:
    events: list[tuple[str, dict[str, Any]]] = []
    headers = {"X-Session-ID": str(uuid.uuid4())}
    with client.stream(
        "POST", "/api/v1/chat/stream", json={"message": message}, headers=headers
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        frame: list[str] = []
        for line in response.iter_lines():
            if line == "":
                if frame:
                    name = "message"
                    data = ""
                    for entry in frame:
                        if entry.startswith("event:"):
                            name = entry.split(":", 1)[1].strip()
                        elif entry.startswith("data:"):
                            data = entry.split(":", 1)[1].strip()
                    events.append((name, json.loads(data)))
                    frame = []
            else:
                frame.append(line)
    return events


def test_stages_arrive_before_the_result(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    monkeypatch.setattr(
        "src.api.routes.run_agent",
        _fake_run_agent(["supervisor", "inventory", "respond"], "Xong rồi nhé"),
    )

    events = _read_events(client, "chào Nera")
    names = [name for name, _ in events]

    assert names == ["stage", "stage", "stage", "result"]
    assert [data["stage"] for name, data in events if name == "stage"] == [
        "supervisor",
        "inventory",
        "respond",
    ]


def test_every_stage_carries_a_vietnamese_label(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(
        "src.api.routes.run_agent", _fake_run_agent(["supervisor", "inventory"], "ok")
    )

    labels = [data["label"] for name, data in _read_events(client, "tìm nhà") if name == "stage"]

    assert labels == ["Đang đọc nhu cầu của bạn", "Đang tìm trong kho nhà"]


def test_unknown_nodes_are_skipped_rather_than_mislabelled(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(
        "src.api.routes.run_agent",
        _fake_run_agent(["supervisor", "some_future_node"], "ok"),
    )

    names = [name for name, _ in _read_events(client, "xin chào")]

    assert names == ["stage", "result"]


def test_result_frame_carries_the_full_chat_response(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(
        "src.api.routes.run_agent", _fake_run_agent(["respond"], "Nera nghe đây")
    )

    result = next(data for name, data in _read_events(client, "hi") if name == "result")

    assert result["response"] == "Nera nghe đây"
    assert result["ai_mode"] == "llm_direct"
    assert "session_id" in result


def test_a_failing_turn_reports_an_error_frame_not_a_broken_stream(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    async def _boom(state: dict[str, Any], on_stage: Any = None) -> dict[str, Any]:
        if on_stage:
            on_stage("supervisor")
        raise RuntimeError("provider down")

    monkeypatch.setattr("src.api.routes.run_agent", _boom)

    events = _read_events(client, "tìm nhà")
    names = [name for name, _ in events]

    assert names[-1] == "error"
    assert events[-1][1]["status"] == 503


def test_invalid_session_id_is_rejected_through_the_stream(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr("src.api.routes.run_agent", _fake_run_agent(["respond"], "ok"))

    with client.stream(
        "POST",
        "/api/v1/chat/stream",
        json={"message": "hi"},
        headers={"X-Session-ID": "not-a-uuid"},
    ) as response:
        body = response.read().decode()

    assert "event: error" in body
    assert "422" in body
