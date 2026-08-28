from src.services.auth_service import decrypt_token, encrypt_token


def test_encrypt_decrypt_token():
    raw_token = "ya29.a0AfH6SMD_SampleGoogleOAuthRefreshToken12345"
    cipher_token = encrypt_token(raw_token)

    # Token must be encrypted (not plaintext)
    assert cipher_token is not None
    assert cipher_token != raw_token
    assert not cipher_token.startswith("ya29.")

    # Decrypt must recover the exact token
    decrypted = decrypt_token(cipher_token)
    assert decrypted == raw_token


def test_encrypt_none_or_empty():
    assert encrypt_token(None) is None
    assert encrypt_token("") is None
    assert decrypt_token(None) is None
    assert decrypt_token("") is None


def test_decrypt_fallback_on_plain():
    # If the token is plain or invalid cipher, it gracefully returns the plain text
    plain_sample = "plain_token_fallback"
    assert decrypt_token(plain_sample) == plain_sample
