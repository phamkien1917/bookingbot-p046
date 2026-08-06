import uuid

from sqlalchemy import Column, String, Boolean, Numeric, Integer, SmallInteger, text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(32), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    developer_name = Column(String(200))
    description = Column(String)
    status = Column(String(20), nullable=False, default='ACTIVE')
    address_line = Column(String, nullable=False)
    ward = Column(String(100))
    district = Column(String(100))
    province = Column(String(100), nullable=False)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    default_hold_minutes = Column(SmallInteger, nullable=False, default=30)
    hold_warning_minutes = Column(SmallInteger, nullable=False, default=5)
    max_hold_extensions = Column(SmallInteger, nullable=False, default=1)
    metadata_col = Column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    properties = relationship("Property", back_populates="project")

class Property(Base):
    __tablename__ = "properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"))
    code = Column(String(50), nullable=False, unique=True)
    property_kind = Column(String, nullable=False) # property_kind_t
    title = Column(String(200), nullable=False)
    description = Column(String)
    status = Column(String, nullable=False, default='DRAFT') # property_status_t
    address_line = Column(String)
    ward = Column(String(100))
    district = Column(String(100))
    province = Column(String(100))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    area_sqm = Column(Numeric(12, 2), nullable=False)
    usable_area_sqm = Column(Numeric(12, 2))
    bedrooms = Column(SmallInteger)
    bathrooms = Column(SmallInteger)
    floor_number = Column(Integer)
    orientation = Column(String(50))
    legal_status = Column(String(100))
    list_price = Column(Numeric(18, 2))
    currency = Column(String(10), nullable=False, default='VND')
    parcel_number = Column(String(50))
    map_sheet_number = Column(String(50))
    land_use_purpose = Column(String(100))
    land_use_term = Column(String(100))
    frontage_m = Column(Numeric(10, 2))
    road_width_m = Column(Numeric(10, 2))
    features = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    project = relationship("Project", back_populates="properties")
    media = relationship("PropertyMedia", back_populates="property_rel", cascade="all, delete-orphan")


class PropertyMedia(Base):
    __tablename__ = "property_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String(20), nullable=False, default='IMAGE')
    url = Column(String, nullable=False)
    source = Column(String(50), nullable=False, default='INTERNAL')
    caption = Column(String(200))
    sort_order = Column(SmallInteger, nullable=False, default=0)
    is_cover = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    property_rel = relationship("Property", back_populates="media")
