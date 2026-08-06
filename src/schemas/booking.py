from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class TourRequestCreate(BaseModel):
    property_id: UUID
    preferred_start: Optional[datetime] = None
    preferred_end: Optional[datetime] = None
    pax_count: int = 1
    customer_note: Optional[str] = None

class TourRequestResponse(BaseModel):
    id: UUID
    request_code: str
    customer_user_id: UUID
    property_id: UUID
    status: str
    tour_mode: str
    preferred_start: Optional[datetime]
    preferred_end: Optional[datetime]
    party_size: int
    customer_note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
