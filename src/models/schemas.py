"""Pydantic schemas for API requests and responses."""


from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Tin nhắn từ user"
    )
    session_id: str | None = Field(
        default=None,
        description="Session ID for conversation continuity"
    )


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str = Field(..., description="Phản hồi từ agent")
    analysis: str = Field(default="", description="Phân tích nội bộ")
    session_id: str | None = Field(default=None, description="Session ID")
    properties: list | None = Field(default_factory=list, description="Danh sách bất động sản gợi ý")
    insights: dict | None = Field(default_factory=dict, description="Thông tin AI thu thập được từ người dùng")


class HITLDecision(BaseModel):
    """Schema for HITL (Human-in-the-Loop) decisions."""

    action: str = Field(..., description="Action: APPROVE, REJECT, OVERRIDE")
    message: str = Field(default="", description="Message to send to customer")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")


class BookingStatusResponse(BaseModel):
    """Response schema for booking status."""

    booking_id: str
    booking_code: str
    status: str
    starts_at: str | None
    ends_at: str | None
    property: dict | None
    sale: dict | None


class PropertySearchRequest(BaseModel):
    """Request schema for property search."""

    district: str | None = None
    province: str | None = None
    property_kind: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_bedrooms: int | None = None
    limit: int = Field(default=10, ge=1, le=50)


class HealthResponse(BaseModel):
    """Response schema for health check."""

    status: str
    app: str
    env: str
    database: str = "connected"
    redis: str = "connected"
