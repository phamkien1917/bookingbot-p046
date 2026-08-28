import re
from pathlib import Path

from src.services.auth_service import get_password_hash, verify_password

OAUTH_ROUTE = Path("src/api/routes/google_oauth.py")


def test_oauth_user_password_is_random_not_derived_from_email():
    """Regression: OAuth accounts once used a password derived from the email.

    Anyone who knew the address could then log in with a password form.
    The placeholder password must come from secrets, never from user data.
    """
    source = OAUTH_ROUTE.read_text(encoding="utf-8")
    creation = re.search(r"password_hash=get_password_hash\((.+?)\)\,", source)

    assert creation, "OAuth route no longer sets password_hash the expected way"
    assert "secrets.token_urlsafe" in creation.group(1)
    assert "email" not in creation.group(1)


def test_predictable_password_does_not_verify():
    """A hash built from a random secret must reject the old guessable form."""
    import secrets

    email = "oauth.user@example.com"
    hashed = get_password_hash(secrets.token_urlsafe(32))

    assert verify_password(f"gauth_{email}", hashed) is False
    assert verify_password(email, hashed) is False
