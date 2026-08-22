import pytest
from fastapi import HTTPException

from src.api.routes.google_oauth import _create_oauth_state, _decode_oauth_state


def test_oauth_state_round_trip() -> None:
    state = _create_oauth_state("sale-user-id")
    assert _decode_oauth_state(state) == "sale-user-id"


def test_oauth_state_rejects_tampering() -> None:
    state = _create_oauth_state("sale-user-id")
    replacement = "a" if state[-1] != "a" else "b"

    with pytest.raises(HTTPException) as exc_info:
        _decode_oauth_state(f"{state[:-1]}{replacement}")

    assert exc_info.value.status_code == 400


def test_login_oauth_state() -> None:
    from src.api.routes.google_oauth import _create_login_oauth_state, _decode_oauth_payload

    state = _create_login_oauth_state()
    payload = _decode_oauth_payload(state)
    assert payload.get("purpose") == "google_login"

