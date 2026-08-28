from unittest.mock import patch

from src.services.auth_service import DEMO_PASSWORD_HASH, verify_password


def test_verify_password_demo_guard_development():
    """Test demo password is accepted only in development environment."""
    with patch("src.services.auth_service.settings.app_env", "development"):
        assert verify_password("Demo@123", DEMO_PASSWORD_HASH) is True
        assert verify_password("123456", DEMO_PASSWORD_HASH) is True
        assert verify_password("WrongPassword", DEMO_PASSWORD_HASH) is False


def test_verify_password_demo_guard_production():
    """Test demo password is rejected in production environment."""
    with patch("src.services.auth_service.settings.app_env", "production"):
        assert verify_password("Demo@123", DEMO_PASSWORD_HASH) is False
        assert verify_password("123456", DEMO_PASSWORD_HASH) is False


def test_verify_password_demo_guard_staging():
    """Test demo password is rejected in staging environment."""
    with patch("src.services.auth_service.settings.app_env", "staging"):
        assert verify_password("Demo@123", DEMO_PASSWORD_HASH) is False
        assert verify_password("123456", DEMO_PASSWORD_HASH) is False
