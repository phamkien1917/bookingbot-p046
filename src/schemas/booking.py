from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TourRequestCreate(BaseModel):
    property_id: UUID
    sale_user_id: UUID
    preferred_start: datetime
    preferred_end: datetime
    pax_count: int = Field(default=1, ge=1, le=20)
    customer_note: str | None = Field(default=None, max_length=1000)
    is_reschedule: bool = False

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.preferred_end <= self.preferred_start:
            raise ValueError("preferred_end must be after preferred_start")
        return self


class BookingAction(BaseModel):
    reason: str | None = Field(default=None, max_length=500)


class UserStatusUpdate(BaseModel):
    status: str


class MediaResponse(BaseModel):
    url: str
    is_cover: bool
    caption: str | None = None

class PropertyResponse(BaseModel):
    id: UUID
    title: str
    address: str
    district: str | None = None
    province: str | None = None
    media: list[MediaResponse] = Field(default_factory=list)


class SaleResponse(BaseModel):
    id: UUID
    full_name: str
    phone: str
    email: str
    job_title: str | None = None

class AppointmentResponse(BaseModel):
    id: UUID
    booking_code: str
    status: str
    starts_at: datetime
    ends_at: datetime

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    request_code: str
    status: str
    tour_mode: str
    preferred_start: datetime
    preferred_end: datetime
    party_size: int
    customer_note: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    property: PropertyResponse | None = None
    sale: SaleResponse | None = None
    appointment: AppointmentResponse | None = None
