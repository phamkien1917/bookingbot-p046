from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from src.utils.property_text import clean_property_description, clean_property_title


class PropertyMediaSchema(BaseModel):
    id: UUID
    media_type: str
    url: str
    source: str | None = None
    caption: str | None = None
    sort_order: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)

class PropertySchema(BaseModel):
    id: UUID
    code: str
    property_kind: str
    title: str
    description: str | None = None
    status: str
    address_line: str | None = None
    ward: str | None = None
    district: str | None = None
    province: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    area_sqm: float
    usable_area_sqm: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    floor_number: int | None = None
    orientation: str | None = None
    legal_status: str | None = None
    list_price: float | None = None
    currency: str
    features: Any
    published_at: datetime | None = None

    media: list[PropertyMediaSchema] = []

    model_config = ConfigDict(from_attributes=True)

    @field_validator("title", mode="before")
    @classmethod
    def format_title(cls, v: Any) -> Any:
        if isinstance(v, str):
            return clean_property_title(v) or v
        return v

    @field_validator("description", mode="before")
    @classmethod
    def format_description(cls, v: Any) -> Any:
        if isinstance(v, str):
            return clean_property_description(v)
        return v

class PropertyListResponse(BaseModel):
    items: list[PropertySchema]
    total: int
