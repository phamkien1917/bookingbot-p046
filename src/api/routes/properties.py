
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_session
from src.database.models import Property, PropertyKind, PropertyStatus
from src.schemas.property import PropertyListResponse, PropertySchema

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("", response_model=PropertyListResponse)
async def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None, min_length=1, max_length=120),
    district: str | None = Query(None, min_length=1, max_length=100),
    province: str | None = Query(None, min_length=1, max_length=100),
    property_kind: PropertyKind | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    min_bedrooms: int | None = Query(None, ge=0, le=20),
    min_area: float | None = Query(None, ge=0),
    max_area: float | None = Query(None, ge=0),
    sort: Literal["newest", "price_asc", "price_desc", "area_desc"] = "newest",
    db: AsyncSession = Depends(get_session)
):
    filters = [Property.status == PropertyStatus.AVAILABLE]
    if keyword:
        pattern = f"%{keyword.strip()}%"
        filters.append(
            or_(
                Property.title.ilike(pattern),
                Property.address_line.ilike(pattern),
                Property.ward.ilike(pattern),
                Property.district.ilike(pattern),
                Property.province.ilike(pattern),
            )
        )
    if district:
        filters.append(Property.district.ilike(f"%{district.strip()}%"))
    if province:
        filters.append(Property.province.ilike(f"%{province.strip()}%"))
    if property_kind:
        filters.append(Property.property_kind == property_kind)
    if min_price is not None:
        filters.append(Property.list_price >= min_price)
    if max_price is not None:
        filters.append(Property.list_price <= max_price)
    if min_bedrooms is not None:
        filters.append(Property.bedrooms >= min_bedrooms)
    if min_area is not None:
        filters.append(Property.area_sqm >= min_area)
    if max_area is not None:
        filters.append(Property.area_sqm <= max_area)

    order_by = {
        "newest": Property.published_at.desc().nullslast(),
        "price_asc": Property.list_price.asc().nullslast(),
        "price_desc": Property.list_price.desc().nullslast(),
        "area_desc": Property.area_sqm.desc().nullslast(),
    }[sort]
    stmt = (
        select(Property)
        .options(selectinload(Property.media))
        .where(*filters)
        .order_by(order_by, Property.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    properties = result.scalars().all()

    total = await db.scalar(select(func.count(Property.id)).where(*filters)) or 0

    return {"items": properties, "total": total}

@router.get("/{property_id}", response_model=PropertySchema)
async def get_property_by_id(property_id: str, db: AsyncSession = Depends(get_session)):
    stmt = select(Property).options(selectinload(Property.media)).where(Property.id == property_id)
    result = await db.execute(stmt)
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop
