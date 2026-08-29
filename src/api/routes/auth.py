import logging
from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import get_session
from src.database.models import User, UserRole, UserStatus
from src.schemas.auth import (
    ForgotPasswordRequest,
    PasswordUpdate,
    ResetPasswordRequest,
    Token,
    UserRegister,
    UserResponse,
    UserUpdate,
)
from src.services.auth_service import (
    create_access_token,
    create_password_reset_token,
    get_password_hash,
    get_password_reset_subject,
    register_user,
    verify_password,
    verify_password_reset_token,
)
from src.services.email_service import send_password_reset_email
from src.utils.time import utcnow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
settings = get_settings()

def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_session)):
    try:
        new_user = await register_user(db, user_data)
        return new_user
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        logger.exception("Registration error")
        raise HTTPException(status_code=500, detail="Đã xảy ra lỗi khi đăng ký. Vui lòng thử lại sau.")

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(User).where(User.email == form_data.username.lower().strip())
    result = await db.execute(stmt)
    user = result.scalars().first()

    if (
        not user
        or user.status != UserStatus.ACTIVE
        or not verify_password(form_data.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.last_login_at = utcnow()
    access_token = create_access_token(
        data={"user_id": str(user.id), "role": user.role.value}
    )
    set_auth_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer", "user": user}

async def get_optional_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session),
) -> User | None:
    import jwt

    from src.services.auth_service import ALGORITHM, SECRET_KEY

    token = token or request.cookies.get(settings.auth_cookie_name)
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or user.status != UserStatus.ACTIVE:
            return None
        return user
    except jwt.PyJWTError:
        return None

async def get_current_user(
    user: User | None = Depends(get_optional_current_user),
) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_user_id(user: User = Depends(get_current_user)) -> str:
    return str(user.id)

def require_roles(*roles: UserRole) -> Callable:
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return dependency

@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout() -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(settings.auth_cookie_name, path="/")
    return response

@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.phone is not None:
        user.phone = user_data.phone

    await db.commit()
    await db.refresh(user)
    return user

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    password_data: PasswordUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")

    user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_session),
):
    stmt = select(User).where(User.email == data.email.lower().strip())
    result = await db.execute(stmt)
    user = result.scalars().first()
    response = {
        "message": "Nếu email tồn tại trong hệ thống, liên kết đặt lại mật khẩu đã được gửi."
    }
    if user and user.status == UserStatus.ACTIVE:
        token = create_password_reset_token(user)
        reset_url = f"{settings.frontend_url.rstrip('/')}/forgot-password?token={token}"
        await send_password_reset_email(user.email, reset_url)
        # Local development remains usable without an SMTP account. Never leak
        # this token from a production response.
        if settings.app_env == "development":
            response["dev_reset_token"] = token
    return response

@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_session),
):
    user_id = get_password_reset_subject(data.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.")
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password_reset_token(data.token, user):
        raise HTTPException(status_code=400, detail="Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.")

    user.password_hash = get_password_hash(data.new_password)
    user.updated_at = utcnow()
    await db.commit()
    return {"message": "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập bằng mật khẩu mới."}
