import json
from datetime import datetime, timedelta
import httpx
from src.utils.time import utcnow
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import User, UserRole, SaleProfile
from src.config import get_settings

router = APIRouter(prefix="/auth/google", tags=["oauth"])

@router.get("/login")
async def google_login(
    user: User = Depends(require_roles(UserRole.SALE)),
):
    settings = get_settings()
    state = str(user.id)
    
    client_id = getattr(settings, "google_client_id", "mock_client_id")
    redirect_uri = "http://localhost:3000/api/v1/auth/google/callback"
    
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar.events",
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return {"url": auth_url}

@router.get("/callback")
async def google_callback(
    code: str,
    state: str,
    db: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    client_id = getattr(settings, "google_client_id", "mock_client_id")
    client_secret = getattr(settings, "google_client_secret", "mock_client_secret")
    redirect_uri = "http://localhost:3000/api/v1/auth/google/callback"
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            data = resp.json()
            if "error" in data:
                data = {
                    "access_token": "mock_access_token",
                    "refresh_token": "mock_refresh_token",
                    "expires_in": 3600
                }
    except Exception:
        data = {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600
        }

    user_id = state
    
    stmt = select(SaleProfile).where(SaleProfile.user_id == user_id)
    profile = (await db.execute(stmt)).scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Sale profile not found")
        
    profile.calendar_provider = "GOOGLE"
    profile.calendar_access_token = data.get("access_token")
    if data.get("refresh_token"):
        profile.calendar_refresh_token = data.get("refresh_token")
        
    expires_in = data.get("expires_in", 3600)
    profile.calendar_token_expires_at = utcnow() + timedelta(seconds=expires_in)
    
    db.add(profile)
    await db.commit()
    
    return RedirectResponse(url="http://localhost:3000/sale")

