from typing import List, Optional, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PropertyMediaSchema(BaseModel):
    id: UUID
    media_type: str
    url: str
    source: Optional[str] = None
    caption: Optional[str] = None
    sort_order: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)

class PropertySchema(BaseModel):
    id: UUID
    code: str
    property_kind: str
    title: str
    description: Optional[str] = None
    status: str
    address_line: Optional[str] = None
    ward: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_sqm: float
    usable_area_sqm: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    list_price: Optional[float] = None
    currency: str
    features: Any
    published_at: Optional[datetime] = None

    media: List[PropertyMediaSchema] = []

    model_config = ConfigDict(from_attributes=True)

class PropertyListResponse(BaseModel):
    items: List[PropertySchema]
    total: int
