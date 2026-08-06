from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database import get_db
from src.models import Property
from src.schemas.property import PropertyListResponse, PropertySchema

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("", response_model=PropertyListResponse)
async def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
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
