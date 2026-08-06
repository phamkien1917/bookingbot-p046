import uuid

from sqlalchemy import Column, String, Boolean, Numeric, Integer, SmallInteger, text, DateTime, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.orm import relationship

from src.database import Base

class TourRequest(Base):
    __tablename__ = "tour_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_code = Column(String(32), nullable=False, unique=True)
    conversation_id = Column(UUID(as_uuid=True))  # No FK for now, conversations model not yet created
    customer_user_id = Column(UUID(as_uuid=True), ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="RESTRICT"), nullable=False)
    status = Column(ENUM('DRAFT', 'COLLECTING', 'OPTIONS_PROPOSED', 'WAITING_APPROVAL', 'APPROVED', 'REJECTED', 'EXPIRED', 'CANCELLED', 'BOOKED', name='request_status_t', create_type=False), nullable=False, default='DRAFT')
    tour_mode = Column(ENUM('IN_PERSON', 'VIDEO', name='tour_mode_t', create_type=False), nullable=False, default='IN_PERSON')
    preferred_start = Column(DateTime(timezone=True))
    preferred_end = Column(DateTime(timezone=True))
    party_size = Column(SmallInteger, nullable=False, default=1)
    customer_note = Column(String)
    request_text_redacted = Column(String)
    extracted_requirements = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    submitted_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_code = Column(String(32), nullable=False, unique=True)
    tour_request_id = Column(UUID(as_uuid=True), ForeignKey("tour_requests.id"), nullable=False, unique=True)
    approval_request_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    customer_user_id = Column(UUID(as_uuid=True), ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="RESTRICT"), nullable=False)
    sale_user_id = Column(UUID(as_uuid=True), ForeignKey("sale_profiles.user_id", ondelete="RESTRICT"), nullable=False)
    status = Column(ENUM('CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'NO_SHOW', 'RESCHEDULED', 'CANCELLED', name='appointment_status_t', create_type=False), nullable=False, default='CONFIRMED')
    tour_mode = Column(ENUM('IN_PERSON', 'VIDEO', name='tour_mode_t', create_type=False), nullable=False, default='IN_PERSON')
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    party_size = Column(SmallInteger, nullable=False, default=1)
    meeting_address = Column(String)
    waiting_room_name = Column(String(100))
    customer_note = Column(String)
    internal_note = Column(String)
    external_calendar_event_id = Column(String)
    calendar_sync_status = Column(ENUM('NOT_REQUESTED', 'PENDING', 'SYNCED', 'FAILED', name='sync_status_t', create_type=False), nullable=False, default='NOT_REQUESTED')
    calendar_sync_error = Column(String)
    confirmation_sent_at = Column(DateTime(timezone=True))
    checked_in_at = Column(DateTime(timezone=True))
    checked_out_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    cancellation_reason = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))


class PropertyHold(Base):
    __tablename__ = "property_holds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hold_code = Column(String(32), nullable=False, unique=True)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="RESTRICT"), nullable=False, unique=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="RESTRICT"), nullable=False)
    customer_user_id = Column(UUID(as_uuid=True), ForeignKey("customer_profiles.user_id", ondelete="RESTRICT"), nullable=False)
    approved_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    status = Column(ENUM('ACTIVE', 'EXPIRED', 'RELEASED', 'CONVERTED', name='hold_status_t', create_type=False), nullable=False, default='ACTIVE')
    starts_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    max_expires_at = Column(DateTime(timezone=True), nullable=False)
    extension_count = Column(SmallInteger, nullable=False, default=0)
    released_at = Column(DateTime(timezone=True))
    release_reason = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
