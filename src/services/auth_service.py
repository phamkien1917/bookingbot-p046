from datetime import timedelta
from hashlib import sha256

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database.models import CustomerProfile, User
from src.schemas.auth import UserRegister
from src.utils.time import utcnow

settings = get_settings()

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DEMO_PASSWORD_HASH = "DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH"
DEMO_PASSWORD = "Demo@123"
LEGACY_DEMO_PASSWORD = "123456"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password == DEMO_PASSWORD_HASH:
        if settings.app_env != "development":
            return False
        return plain_password in {DEMO_PASSWORD, LEGACY_DEMO_PASSWORD}
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_password_reset_token(user: User) -> str:
    """Create a short-lived token tied to the user's current password hash.

    The fingerprint makes the token effectively single-use: changing the
    password invalidates every previously issued reset token.
    """
    payload = {
        "sub": str(user.id),
        "purpose": "password_reset",
        "password_fingerprint": sha256(user.password_hash.encode("utf-8")).hexdigest(),
        "exp": utcnow() + timedelta(minutes=settings.password_reset_expire_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_password_reset_token(token: str, user: User) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return False
    expected = sha256(user.password_hash.encode("utf-8")).hexdigest()
    return (
        payload.get("purpose") == "password_reset"
        and payload.get("sub") == str(user.id)
        and payload.get("password_fingerprint") == expected
    )


def get_password_reset_subject(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    if payload.get("purpose") != "password_reset":
        return None
    subject = payload.get("sub")
    return str(subject) if subject else None


async def register_user(db: AsyncSession, user_data: UserRegister):
    # Check email exists
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise ValueError("Email đã được đăng ký")

    # Check phone exists
    stmt = select(User).where(User.phone == user_data.phone)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise ValueError("Số điện thoại đã được đăng ký")

    # Create User
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        role='CUSTOMER'
    )
    db.add(new_user)
    await db.flush()  # To get new_user.id

    # Create CustomerProfile with correct column names matching DB schema
    short_id = str(new_user.id).replace("-", "")[:8].upper()
    new_profile = CustomerProfile(
        user_id=new_user.id,
        customer_code=f"CUS-{short_id}",
        preferred_contact_channel="IN_APP"
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_user)

    return new_user
