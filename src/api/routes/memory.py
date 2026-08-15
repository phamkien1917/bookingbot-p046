"""Customer-controlled long-term memory endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import User, UserRole
from src.services.customer_memory_service import (
    forget_customer_memory,
    get_customer_memory,
    memory_summary,
    remember_feedback,
)

router = APIRouter(prefix="/memory", tags=["memory"])


class FeedbackRequest(BaseModel):
    message: str = Field(min_length=2, max_length=500)


@router.get("")
async def read_memory(
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    memory = await get_customer_memory(db, str(user.id))
    return {"items": memory, "summary": memory_summary(memory)}


@router.post("/feedback")
async def add_feedback(
    request: FeedbackRequest,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    if not await remember_feedback(db, str(user.id), request.message):
        raise HTTPException(status_code=422, detail="Hãy mô tả sở thích, ví dụ: Tôi ưu tiên căn có ban công.")
    memory = await get_customer_memory(db, str(user.id))
    return {"items": memory, "summary": memory_summary(memory)}


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_memory(
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    await forget_customer_memory(db, str(user.id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_memory_item(
    key: str,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    await forget_customer_memory(db, str(user.id), key)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
