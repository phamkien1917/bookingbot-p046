import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, Numeric, Date, ForeignKey, JSON, Integer, SmallInteger, text, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.orm import relationship

from src.database import Base
from src.models.enums import UserRole, UserStatus

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(ENUM('CUSTOMER', 'SALE', 'COORDINATOR', 'ADMIN', name='user_role_t', create_type=False), nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(150), nullable=False)
    avatar_url = Column(String)
    status = Column(ENUM('ACTIVE', 'LOCKED', 'DISABLED', name='user_status_t', create_type=False), nullable=False, default='ACTIVE')
    timezone = Column(String(64), nullable=False, default='Asia/Ho_Chi_Minh')
    locale = Column(String(16), nullable=False, default='vi-VN')
    email_verified_at = Column(DateTime(timezone=True))
    phone_verified_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    customer_profile = relationship("CustomerProfile", back_populates="user", uselist=False)
    sale_profile = relationship("SaleProfile", back_populates="user", uselist=False)


class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    customer_code = Column(String(32), nullable=False, unique=True)
    identity_verified_at = Column(DateTime(timezone=True))
    preferred_contact_channel = Column(ENUM('IN_APP', 'EMAIL', 'SMS', 'WEB_PUSH', name='notification_channel_t', create_type=False), nullable=False, default='IN_APP')
    budget_min = Column(Numeric(18, 2))
    budget_max = Column(Numeric(18, 2))
    desired_move_date = Column(Date)
    marketing_consent = Column(Boolean, nullable=False, default=False)
    internal_note = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="customer_profile")


class SaleProfile(Base):
    __tablename__ = "sale_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    employee_code = Column(String(32), nullable=False, unique=True)
    branch_name = Column(String(150))
    job_title = Column(String(100))
    specialties = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    working_hours = Column(JSONB, nullable=False)
    max_daily_tours = Column(SmallInteger, nullable=False, default=8)
    is_accepting_tours = Column(Boolean, nullable=False, default=True)
    calendar_provider = Column(String(20))
    external_calendar_id = Column(String)
    calendar_credentials_secret_ref = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="sale_profile")
