import jwt
import uuid
import bcrypt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import User, CustomerProfile
from src.schemas.auth import UserRegister
from src.config import get_settings

settings = get_settings()

SECRET_KEY = "supersecretkey"  # In production, get from env/settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(db: AsyncSession, user_data: UserRegister):
    # Check email exists
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        return None

    # Check phone exists
    stmt = select(User).where(User.phone == user_data.phone)
    result = await db.execute(stmt)
    if result.scalars().first():
        return None

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
