from src.services.auth_service import DEMO_PASSWORD_HASH, verify_password


def test_demo_hash_accepts_current_and_legacy_demo_passwords() -> None:
    assert verify_password("Demo@123", DEMO_PASSWORD_HASH)
    assert verify_password("123456", DEMO_PASSWORD_HASH)


def test_demo_hash_rejects_unknown_password() -> None:
    assert not verify_password("not-the-demo-password", DEMO_PASSWORD_HASH)
