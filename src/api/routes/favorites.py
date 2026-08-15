from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import Property, PropertyStatus, SavedProperty, User, UserRole
from src.schemas.property import PropertySchema

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("")
async def list_favorites(
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(SavedProperty)
        .join(SavedProperty.property)
        .options(selectinload(SavedProperty.property).selectinload(Property.media))
        .where(SavedProperty.customer_user_id == user.id)
        .order_by(SavedProperty.created_at.desc())
    )
    rows = result.scalars().all()
    return {
        "items": [PropertySchema.model_validate(row.property) for row in rows if row.property],
        "ids": [str(row.property_id) for row in rows],
        "total": len(rows),
    }


@router.get("/ids")
async def favorite_ids(
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    result = await db.scalars(
        select(SavedProperty.property_id).where(SavedProperty.customer_user_id == user.id)
    )
    return {"ids": [str(property_id) for property_id in result.all()]}


@router.put("/{property_id}", status_code=201)
async def save_favorite(
    property_id: UUID,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    property_row = await db.get(Property, property_id)
    if not property_row or property_row.status in {PropertyStatus.HIDDEN, PropertyStatus.SOLD}:
        raise HTTPException(status_code=404, detail="Bất động sản không còn khả dụng")
    existing = await db.scalar(
        select(SavedProperty).where(
            SavedProperty.customer_user_id == user.id,
            SavedProperty.property_id == property_id,
        )
    )
    if not existing:
        db.add(SavedProperty(customer_user_id=user.id, property_id=property_id))
        await db.flush()
    return {"saved": True, "property_id": str(property_id)}


@router.delete("/{property_id}", status_code=204)
async def remove_favorite(
    property_id: UUID,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    await db.execute(
        delete(SavedProperty).where(
            SavedProperty.customer_user_id == user.id,
            SavedProperty.property_id == property_id,
        )
    )
