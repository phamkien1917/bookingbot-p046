from pydantic import BaseModel


class PropertyCreate(BaseModel):
    title: str
    property_kind: str
    area_sqm: float
    list_price: float | None = None
    address_line: str
    province: str
    district: str | None = None
    ward: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    status: str = "AVAILABLE"
    description: str | None = None


class PropertyUpdate(BaseModel):
    title: str | None = None
    property_kind: str | None = None
    area_sqm: float | None = None
    list_price: float | None = None
    address_line: str | None = None
    province: str | None = None
    district: str | None = None
    ward: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    status: str | None = None
    description: str | None = None


class SaleProfileUpdate(BaseModel):
    job_title: str | None = None
    branch_name: str | None = None
    max_daily_tours: int | None = None
    is_accepting_tours: bool | None = None
