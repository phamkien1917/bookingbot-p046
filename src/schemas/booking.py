from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class TourRequestCreate(BaseModel):
    property_id: UUID
    sale_user_id: UUID
    preferred_start: datetime
    preferred_end: datetime
    pax_count: int = Field(default=1, ge=1, le=20)
    customer_note: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.preferred_end <= self.preferred_start:
            raise ValueError("preferred_end must be after preferred_start")
        return self


class BookingAction(BaseModel):
    reason: str | None = Field(default=None, max_length=500)


class UserStatusUpdate(BaseModel):
    status: str
