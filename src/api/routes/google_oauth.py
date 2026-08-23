from datetime import timedelta
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.config import get_settings
from src.database import get_session
from src.database.models import CustomerProfile, SaleProfile, User, UserRole, UserStatus
from src.services.auth_service import ALGORITHM, SECRET_KEY, create_access_token, get_password_hash
from src.utils.time import utcnow

router = APIRouter(prefix="/auth/google", tags=["oauth"])


def _oauth_settings():
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google OAuth chưa được cấu hình Client ID và Client Secret.")
    return settings


def _create_calendar_oauth_state(user_id: str) -> str:
    return jwt.encode(
        {
            "user_id": user_id,
            "purpose": "google_calendar_oauth",
            "exp": utcnow() + timedelta(minutes=15),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def _create_oauth_state(user_id: str) -> str:
    return _create_calendar_oauth_state(user_id)


def _create_login_oauth_state() -> str:
    return jwt.encode(
        {
            "purpose": "google_login",
            "exp": utcnow() + timedelta(minutes=15),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def _decode_oauth_payload(state: str) -> dict:
    try:
        return jwt.decode(state, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=400, detail="OAuth state không hợp lệ hoặc đã hết hạn.") from exc


def _decode_oauth_state(state: str) -> str:
    payload = _decode_oauth_payload(state)
    if payload.get("purpose") != "google_calendar_oauth" or not payload.get("user_id"):
        raise HTTPException(status_code=400, detail="OAuth state không hợp lệ.")
    return str(payload["user_id"])


@router.get("/login")
async def google_login(user: User = Depends(require_roles(UserRole.SALE))):
    """Google Calendar connection for Sale agents."""
    settings = _oauth_settings()
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar.events",
        "access_type": "offline",
        "prompt": "consent",
        "state": _create_calendar_oauth_state(str(user.id)),
    }
    return {"url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"}


@router.get("/signin-url")
async def google_signin_url():
    """Generate Google Sign-in URL for users."""
    settings = _oauth_settings()
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
        "state": _create_login_oauth_state(),
    }
    return {"url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"}


@router.get("/callback")
async def google_callback(
    code: str,
    state: str,
    db: AsyncSession = Depends(get_session),
):
    settings = _oauth_settings()
    payload = _decode_oauth_payload(state)
    purpose = payload.get("purpose")

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": settings.google_redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status()
            token_data = token_response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Không thể xác thực với Google OAuth.") from exc

    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=502, detail="Google không trả về access token.")

    # 1. Handle User Login / Register with Google
    if purpose == "google_login":
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                userinfo_resp = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                userinfo_resp.raise_for_status()
                user_info = userinfo_resp.json()
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Không thể lấy thông tin tài khoản Google.") from exc

        email = (user_info.get("email") or "").lower().strip()
        full_name = user_info.get("name") or email.split("@")[0]
        if not email:
            raise HTTPException(status_code=400, detail="Tài khoản Google không có email hợp lệ.")

        # Check existing user
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            # Auto-create customer user
            user = User(
                email=email,
                full_name=full_name,
                password_hash=get_password_hash(f"gauth_{email}"),
                role=UserRole.CUSTOMER,
                status=UserStatus.ACTIVE,
            )
            db.add(user)
            await db.flush()

            short_id = str(user.id).replace("-", "")[:8].upper()
            profile = CustomerProfile(
                user_id=user.id,
                customer_code=f"CUS-{short_id}",
                preferred_contact_channel="IN_APP",
            )
            db.add(profile)
            await db.commit()
            await db.refresh(user)
        else:
            user.last_login_at = utcnow()
            # Ensure CustomerProfile exists if user is customer
            if user.role == UserRole.CUSTOMER or str(user.role) == "CUSTOMER":
                cust_profile = (
                    await db.execute(select(CustomerProfile).where(CustomerProfile.user_id == user.id))
                ).scalar_one_or_none()
                if not cust_profile:
                    short_id = str(user.id).replace("-", "")[:8].upper()
                    profile = CustomerProfile(
                        user_id=user.id,
                        customer_code=f"CUS-{short_id}",
                        preferred_contact_channel="IN_APP",
                    )
                    db.add(profile)
            await db.commit()

        jwt_token = create_access_token(
            data={"user_id": str(user.id), "role": user.role.value}
        )

        redirect_url = f"{settings.frontend_url.rstrip('/')}/login?google_token={jwt_token}"
        response = RedirectResponse(url=redirect_url)
        response.set_cookie(
            key=settings.auth_cookie_name,
            value=jwt_token,
            httponly=True,
            secure=settings.app_env == "production",
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60,
            path="/",
        )
        return response

    # 2. Handle Sale Google Calendar Sync
    if purpose == "google_calendar_oauth":
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Thiếu user_id cho Google Calendar.")

        profile = (
            await db.execute(select(SaleProfile).where(SaleProfile.user_id == user_id))
        ).scalar_one_or_none()
        if not profile:
            raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ Sale.")

        profile.calendar_provider = "GOOGLE"
        profile.calendar_access_token = access_token
        if token_data.get("refresh_token"):
            profile.calendar_refresh_token = token_data["refresh_token"]
        profile.calendar_token_expires_at = utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
        await db.commit()

        return RedirectResponse(url=f"{settings.frontend_url.rstrip('/')}/sale")

    raise HTTPException(status_code=400, detail="Mục đích OAuth không hợp lệ.")
