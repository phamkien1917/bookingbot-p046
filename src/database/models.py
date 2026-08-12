"""SQLAlchemy ORM models for BookingBot.

These models mirror the 001_schema.sql structure but in Python ORM format.
Only essential tables for MVP are implemented here.
"""

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base

# ============== Enums ==============

class UserRole(enum.StrEnum):
    """User role enumeration."""

    CUSTOMER = "CUSTOMER"
    SALE = "SALE"
    COORDINATOR = "COORDINATOR"
    ADMIN = "ADMIN"


class UserStatus(enum.StrEnum):
    """User status enumeration."""

    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    DISABLED = "DISABLED"


class PropertyKind(enum.StrEnum):
    """Property kind enumeration."""

    LAND = "LAND"
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    VILLA = "VILLA"
    TOWNHOUSE = "TOWNHOUSE"
    COMMERCIAL = "COMMERCIAL"


class PropertyStatus(enum.StrEnum):
    """Property status enumeration."""

    DRAFT = "DRAFT"
    AVAILABLE = "AVAILABLE"
    UNDER_OFFER = "UNDER_OFFER"
    SOLD = "SOLD"
    HIDDEN = "HIDDEN"
    MAINTENANCE = "MAINTENANCE"


class RequestStatus(enum.StrEnum):
    """Tour request status enumeration."""

    DRAFT = "DRAFT"
    COLLECTING = "COLLECTING"
    OPTIONS_PROPOSED = "OPTIONS_PROPOSED"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    BOOKED = "BOOKED"


class SlotStatus(enum.StrEnum):
    """Tour slot option status."""

    PROPOSED = "PROPOSED"
    SELECTED = "SELECTED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"


class AppointmentStatus(enum.StrEnum):
    """Appointment/booking status."""

    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"
    RESCHEDULED = "RESCHEDULED"
    CANCELLED = "CANCELLED"


class HoldStatus(enum.StrEnum):
    """Property hold status."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    RELEASED = "RELEASED"
    CONVERTED = "CONVERTED"


class MessageRole(enum.StrEnum):
    """Message role in conversation."""

    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"
    SYSTEM = "SYSTEM"


class NotificationChannel(enum.StrEnum):
    """Notification delivery channel."""

    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    SMS = "SMS"
    WEB_PUSH = "WEB_PUSH"


class DeliveryStatus(enum.StrEnum):
    """Notification delivery status."""

    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TourMode(enum.StrEnum):
    """Tour mode."""

    IN_PERSON = "IN_PERSON"
    VIDEO = "VIDEO"


# ============== Enum name mapping ==============
# Map ORM enum classes sang đúng tên type có sẵn trong PostgreSQL schema
# (do 001_schema.sql tạo). Nếu không map đúng, SQLAlchemy sẽ ép kiểu về
# enum type do chính nó tạo (vd: 'propertystatus') — DB báo lỗi
# "operator does not exist: property_status_t = propertystatus".
# name=... bảo SQLAlchemy KHÔNG tạo type mới (create_type=False)
# và dùng đúng type name có sẵn trong DB.

ENUM_USER_ROLE = Enum(UserRole, name="user_role_t", create_type=False, native_enum=True)
ENUM_USER_STATUS = Enum(UserStatus, name="user_status_t", create_type=False, native_enum=True)
ENUM_PROPERTY_KIND = Enum(PropertyKind, name="property_kind_t", create_type=False, native_enum=True)
ENUM_PROPERTY_STATUS = Enum(PropertyStatus, name="property_status_t", create_type=False, native_enum=True)
ENUM_REQUEST_STATUS = Enum(RequestStatus, name="request_status_t", create_type=False, native_enum=True)
ENUM_SLOT_STATUS = Enum(SlotStatus, name="slot_status_t", create_type=False, native_enum=True)
ENUM_APPOINTMENT_STATUS = Enum(AppointmentStatus, name="appointment_status_t", create_type=False, native_enum=True)
ENUM_HOLD_STATUS = Enum(HoldStatus, name="hold_status_t", create_type=False, native_enum=True)
ENUM_MESSAGE_ROLE = Enum(MessageRole, name="message_role_t", create_type=False, native_enum=True)
ENUM_NOTIFICATION_CHANNEL = Enum(NotificationChannel, name="notification_channel_t", create_type=False, native_enum=True)
ENUM_DELIVERY_STATUS = Enum(DeliveryStatus, name="delivery_status_t", create_type=False, native_enum=True)
ENUM_TOUR_MODE = Enum(TourMode, name="tour_mode_t", create_type=False, native_enum=True)


# ============== Base Models ==============

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ============== User & Profiles ==============

class User(Base, TimestampMixin):
    """User account model."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    role: Mapped[UserRole] = mapped_column(ENUM_USER_ROLE, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        ENUM_USER_STATUS,
        default=UserStatus.ACTIVE,
        nullable=False,
    )
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Ho_Chi_Minh")
    locale: Mapped[str] = mapped_column(String(16), default="vi-VN")
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    phone_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    customer_profile: Mapped[Optional["CustomerProfile"]] = relationship(
        "CustomerProfile",
        back_populates="user",
        uselist=False,
    )
    sale_profile: Mapped[Optional["SaleProfile"]] = relationship(
        "SaleProfile",
        back_populates="user",
        uselist=False,
    )


class CustomerProfile(Base, TimestampMixin):
    """Customer profile with preferences."""

    __tablename__ = "customer_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    customer_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    identity_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    preferred_contact_channel: Mapped[NotificationChannel] = mapped_column(
        ENUM_NOTIFICATION_CHANNEL,
        default=NotificationChannel.IN_APP,
    )
    budget_min: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    budget_max: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    desired_move_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    marketing_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    internal_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="customer_profile")
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
    )
    tour_requests: Mapped[list["TourRequest"]] = relationship(
        "TourRequest",
        back_populates="customer",
    )
    preferences: Mapped[list["CustomerPreference"]] = relationship(
        "CustomerPreference",
        back_populates="customer",
    )


class SaleProfile(Base, TimestampMixin):
    """Sale agent profile."""

    __tablename__ = "sale_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    employee_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    branch_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specialties: Mapped[list] = mapped_column(JSONB, default=list)
    working_hours: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {
            "mon": ["08:00", "18:00"],
            "tue": ["08:00", "18:00"],
            "wed": ["08:00", "18:00"],
            "thu": ["08:00", "18:00"],
            "fri": ["08:00", "18:00"],
            "sat": ["08:00", "18:00"],
        },
    )
    max_daily_tours: Mapped[int] = mapped_column(Integer, default=8)
    is_accepting_tours: Mapped[bool] = mapped_column(Boolean, default=True)
    calendar_provider: Mapped[str | None] = mapped_column(String(20), nullable=True)
    external_calendar_id: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sale_profile")
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="sale",
    )
    slot_options: Mapped[list["TourSlotOption"]] = relationship(
        "TourSlotOption",
        back_populates="sale",
    )
    property_assignments: Mapped[list["PropertySaleAssignment"]] = relationship(
        "PropertySaleAssignment",
        back_populates="sale",
    )


# ============== Properties ==============

class Project(Base, TimestampMixin):
    """Real estate project."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    developer_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    address_line: Mapped[str] = mapped_column(Text, nullable=False)
    ward: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    default_hold_minutes: Mapped[int] = mapped_column(Integer, default=30)
    hold_warning_minutes: Mapped[int] = mapped_column(Integer, default=5)
    max_hold_extensions: Mapped[int] = mapped_column(Integer, default=1)
    extra_data: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    # Relationships
    properties: Mapped[list["Property"]] = relationship(
        "Property",
        back_populates="project",
    )


class Property(Base, TimestampMixin):
    """Individual property listing."""

    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    property_kind: Mapped[PropertyKind] = mapped_column(
        ENUM_PROPERTY_KIND,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[PropertyStatus] = mapped_column(
        ENUM_PROPERTY_STATUS,
        default=PropertyStatus.DRAFT,
    )
    address_line: Mapped[str | None] = mapped_column(Text, nullable=True)
    ward: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    area_sqm: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    usable_area_sqm: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    floor_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    orientation: Mapped[str | None] = mapped_column(String(32), nullable=True)
    legal_status: Mapped[str | None] = mapped_column(String(150), nullable=True)
    list_price: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="VND")
    features: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship(
        "Project",
        back_populates="properties",
    )
    media: Mapped[list["PropertyMedia"]] = relationship(
        "PropertyMedia",
        back_populates="property",
        cascade="all, delete-orphan",
    )
    sale_assignments: Mapped[list["PropertySaleAssignment"]] = relationship(
        "PropertySaleAssignment",
        back_populates="property",
    )
    tour_requests: Mapped[list["TourRequest"]] = relationship(
        "TourRequest",
        back_populates="property",
    )
    holds: Mapped[list["PropertyHold"]] = relationship(
        "PropertyHold",
        back_populates="property",
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="property",
    )

    __table_args__ = (
        Index("ix_properties_search", "project_id", "status", "property_kind", "list_price"),
    )


class PropertyMedia(Base):
    """Property images and media."""

    __tablename__ = "property_media"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
    )
    media_type: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    caption: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    property: Mapped["Property"] = relationship("Property", back_populates="media")


class PropertySaleAssignment(Base):
    """Assignment of sale agents to properties."""

    __tablename__ = "property_sale_assignments"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        primary_key=True,
    )
    sale_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sale_profiles.user_id", ondelete="RESTRICT"),
        primary_key=True,
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    property: Mapped["Property"] = relationship(
        "Property",
        back_populates="sale_assignments",
    )
    sale: Mapped["SaleProfile"] = relationship(
        "SaleProfile",
        back_populates="property_assignments",
    )


# ============== Conversations & Messages ==============

class Conversation(Base, TimestampMixin):
    """Customer conversation session."""

    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    customer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    customer: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="conversations",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        order_by="Message.created_at",
    )
    tour_requests: Mapped[list["TourRequest"]] = relationship(
        "TourRequest",
        back_populates="conversation",
    )


class Message(Base):
    """Individual message in a conversation."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[MessageRole] = mapped_column(ENUM_MESSAGE_ROLE, nullable=False)
    content_redacted: Mapped[str | None] = mapped_column(Text, nullable=True)
    structured_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tool_call_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )

    __table_args__ = (
        Index("ix_messages_conversation_timeline", "conversation_id", "created_at"),
    )


# ============== Tour Requests & Slots ==============

class TourRequest(Base, TimestampMixin):
    """Customer's request to view a property."""

    __tablename__ = "tour_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
    )
    customer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[RequestStatus] = mapped_column(
        ENUM_REQUEST_STATUS,
        default=RequestStatus.DRAFT,
    )
    tour_mode: Mapped[TourMode] = mapped_column(
        ENUM_TOUR_MODE,
        default=TourMode.IN_PERSON,
    )
    preferred_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    preferred_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    party_size: Mapped[int] = mapped_column(Integer, default=1)
    customer_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_text_redacted: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    conversation: Mapped[Optional["Conversation"]] = relationship(
        "Conversation",
        back_populates="tour_requests",
    )
    customer: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="tour_requests",
    )
    property: Mapped["Property"] = relationship(
        "Property",
        back_populates="tour_requests",
    )
    slot_options: Mapped[list["TourSlotOption"]] = relationship(
        "TourSlotOption",
        back_populates="tour_request",
        cascade="all, delete-orphan",
    )
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        back_populates="tour_request",
        uselist=False,
    )

    __table_args__ = (
        Index("ix_tour_requests_customer_status", "customer_user_id", "status"),
        Index("ix_tour_requests_property_status", "property_id", "status"),
    )


class TourSlotOption(Base, TimestampMixin):
    """Proposed time slot for a tour request."""

    __tablename__ = "tour_slot_options"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    tour_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tour_requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    sale_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sale_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[SlotStatus] = mapped_column(
        ENUM_SLOT_STATUS,
        default=SlotStatus.PROPOSED,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    waiting_room_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    score: Mapped[float | None] = mapped_column(Numeric(7, 4), nullable=True)
    score_explanation: Mapped[dict] = mapped_column(JSONB, default=dict)
    valid_until: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    selected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    tour_request: Mapped["TourRequest"] = relationship(
        "TourRequest",
        back_populates="slot_options",
    )
    sale: Mapped["SaleProfile"] = relationship(
        "SaleProfile",
        back_populates="slot_options",
    )

    __table_args__ = (
        UniqueConstraint("id", "tour_request_id", name="uq_tour_slot_id_request"),
        Index("ix_tour_slot_options_request", "tour_request_id", "status", "starts_at"),
    )


# ============== Appointments & Holds ==============

class Appointment(Base, TimestampMixin):
    """Confirmed booking/appointment."""

    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    booking_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    tour_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tour_requests.id"),
        nullable=False,
        unique=True,
    )
    approval_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )
    customer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sale_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sale_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[AppointmentStatus] = mapped_column(
        ENUM_APPOINTMENT_STATUS,
        default=AppointmentStatus.CONFIRMED,
    )
    tour_mode: Mapped[TourMode] = mapped_column(
        ENUM_TOUR_MODE,
        default=TourMode.IN_PERSON,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    party_size: Mapped[int] = mapped_column(Integer, default=1)
    meeting_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    waiting_room_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    customer_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    internal_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_calendar_event_id: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    confirmation_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    checked_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    tour_request: Mapped["TourRequest"] = relationship(
        "TourRequest",
        back_populates="appointment",
    )
    property: Mapped["Property"] = relationship(
        "Property",
        back_populates="appointments",
    )
    sale: Mapped["SaleProfile"] = relationship(
        "SaleProfile",
        back_populates="appointments",
    )
    hold: Mapped[Optional["PropertyHold"]] = relationship(
        "PropertyHold",
        back_populates="appointment",
        uselist=False,
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="appointment",
    )

    __table_args__ = (
        Index("ix_appointments_customer", "customer_user_id", "starts_at"),
        Index("ix_appointments_sale", "sale_user_id", "starts_at"),
        Index("ix_appointments_property", "property_id", "starts_at"),
    )


class PropertyHold(Base, TimestampMixin):
    """Soft hold on a property during booking process."""

    __tablename__ = "property_holds"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    hold_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    appointment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
    )
    customer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
    )
    approved_by_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[HoldStatus] = mapped_column(
        ENUM_HOLD_STATUS,
        default=HoldStatus.ACTIVE,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    max_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    extension_count: Mapped[int] = mapped_column(Integer, default=0)
    released_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    release_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        "Appointment",
        back_populates="hold",
    )
    property: Mapped["Property"] = relationship(
        "Property",
        back_populates="holds",
    )

    __table_args__ = (
        Index("ix_property_holds_expiry", "expires_at"),
    )


# ============== Customer Preferences ==============

class CustomerPreference(Base, TimestampMixin):
    """Stored customer preferences (long-term memory)."""

    __tablename__ = "customer_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    customer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    preference_key: Mapped[str] = mapped_column(String(100), nullable=False)
    preference_value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(5, 4), default=1.0)
    source: Mapped[str] = mapped_column(String(20), default="EXPLICIT")
    last_confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    customer: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="preferences",
    )

    __table_args__ = (
        UniqueConstraint("customer_user_id", "preference_key"),
    )


# ============== Notifications ==============

class Notification(Base):
    """Notification delivery record."""

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=True,
    )
    channel: Mapped[NotificationChannel] = mapped_column(
        ENUM_NOTIFICATION_CHANNEL,
        nullable=False,
    )
    template_key: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    status: Mapped[DeliveryStatus] = mapped_column(
        ENUM_DELIVERY_STATUS,
        default=DeliveryStatus.PENDING,
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        back_populates="notifications",
    )

    __table_args__ = (
        Index("ix_notifications_due", "scheduled_at"),
    )


# ============== Analytics & Audit ==============

class AnalyticsEvent(Base):
    """Analytics event tracking."""

    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    tour_request_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    session_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    properties: Mapped[dict] = mapped_column(JSONB, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        Index("ix_analytics_events_name_time", "event_name", "occurred_at"),
    )


class AuditLog(Base):
    """Audit log for tracking changes."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    before_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    after_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
