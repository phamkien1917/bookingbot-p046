from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database import get_session
from src.database.models import Property
from src.schemas.property import PropertyListResponse, PropertySchema

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=PropertyListResponse)
async def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
):
    # Fetch properties with media
    stmt = select(Property).options(selectinload(Property.media)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    properties = result.scalars().all()
    
    # Just a mock total for now, in real app you do a count query
    total = skip + len(properties)
    if len(properties) == limit:
        total += 1 # indicate there is more
        
    return {"items": properties, "total": total}

@router.get("/{property_id}", response_model=PropertySchema)
async def get_property_by_id(property_id: str, db: AsyncSession = Depends(get_session)):
    stmt = select(Property).options(selectinload(Property.media)).where(Property.id == property_id)
    result = await db.execute(stmt)
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop
