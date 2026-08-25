from types import SimpleNamespace
from uuid import uuid4

from src.services.auth_service import (
    create_password_reset_token,
    get_password_reset_subject,
    verify_password_reset_token,
)


def test_password_reset_token_is_tied_to_current_password_hash() -> None:
    user = SimpleNamespace(id=uuid4(), password_hash="old-password-hash")
    token = create_password_reset_token(user)

    assert get_password_reset_subject(token) == str(user.id)
    assert verify_password_reset_token(token, user) is True

    user.password_hash = "new-password-hash"
    assert verify_password_reset_token(token, user) is False
