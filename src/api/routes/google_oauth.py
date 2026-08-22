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
from src.database.models import SaleProfile, User, UserRole
from src.services.auth_service import ALGORITHM, SECRET_KEY
from src.utils.time import utcnow

router = APIRouter(prefix="/auth/google", tags=["oauth"])


def _oauth_settings():
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google Calendar chưa được cấu hình")
    return settings


def _create_oauth_state(user_id: str) -> str:
    return jwt.encode(
        {
            "user_id": user_id,
            "purpose": "google_calendar_oauth",
            "exp": utcnow() + timedelta(minutes=10),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def _decode_oauth_state(state: str) -> str:
    try:
        payload = jwt.decode(state, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=400, detail="OAuth state không hợp lệ hoặc đã hết hạn") from exc
    if payload.get("purpose") != "google_calendar_oauth" or not payload.get("user_id"):
        raise HTTPException(status_code=400, detail="OAuth state không hợp lệ")
    return str(payload["user_id"])


@router.get("/login")
async def google_login(user: User = Depends(require_roles(UserRole.SALE))):
    settings = _oauth_settings()
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar.events",
        "access_type": "offline",
        "prompt": "consent",
        "state": _create_oauth_state(str(user.id)),
    }
    return {"url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"}


@router.get("/callback")
async def google_callback(
    code: str,
    state: str,
    db: AsyncSession = Depends(get_session),
):
    settings = _oauth_settings()
    user_id = _decode_oauth_state(state)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": settings.google_redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Không thể kết nối Google Calendar") from exc

    access_token = data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=502, detail="Google không trả về access token")

    profile = (
        await db.execute(select(SaleProfile).where(SaleProfile.user_id == user_id))
    ).scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Sale profile not found")

    profile.calendar_provider = "GOOGLE"
    profile.calendar_access_token = access_token
    if data.get("refresh_token"):
        profile.calendar_refresh_token = data["refresh_token"]
    profile.calendar_token_expires_at = utcnow() + timedelta(seconds=data.get("expires_in", 3600))
    await db.commit()

    return RedirectResponse(url=f"{settings.frontend_url.rstrip('/')}/sale")
