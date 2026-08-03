"""Property-related tools for the agent."""

import logging
from typing import Optional
from uuid import UUID

from langchain_core.tools import tool

from src.database.connection import get_session_context
from src.database.models import Property, PropertyHold, HoldStatus, PropertyStatus

logger = logging.getLogger(__name__)


@tool
def search_properties(
    district: Optional[str] = None,
    province: Optional[str] = None,
    property_kind: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    min_area: Optional[float] = None,
    limit: int = 10,
) -> str:
    """Tìm kiếm bất động sản theo các tiêu chí.

    Args:
        district: Quận/Huyện (ví dụ: "Quận 7", "Thành phố Thủ Đức")
        province: Tỉnh/Thành phố (ví dụ: "Hồ Chí Minh")
        property_kind: Loại bất động sản (APARTMENT, HOUSE, VILLA, TOWNHOUSE, LAND, COMMERCIAL)
        min_price: Giá tối thiểu (VND)
        max_price: Giá tối đa (VND)
        min_bedrooms: Số phòng ngủ tối thiểu
        min_area: Diện tích tối thiểu (m²)
        limit: Số lượng kết quả tối đa

    Returns:
        Danh sách các bất động sản phù hợp dạng JSON
    """
    import json
    from sqlalchemy import select, and_

    async def _search():
        async with get_session_context() as session:
            # Build query
            conditions = [Property.status == PropertyStatus.AVAILABLE]

            if district:
                conditions.append(Property.district.ilike(f"%{district}%"))
            if province:
                conditions.append(Property.province.ilike(f"%{province}%"))
            if property_kind:
                conditions.append(Property.property_kind == property_kind.upper())
            if min_price:
                conditions.append(Property.list_price >= min_price)
            if max_price:
                conditions.append(Property.list_price <= max_price)
            if min_bedrooms:
                conditions.append(Property.bedrooms >= min_bedrooms)
            if min_area:
                conditions.append(Property.area_sqm >= min_area)

            stmt = (
                select(Property)
                .where(and_(*conditions))
                .order_by(Property.list_price)
                .limit(limit)
            )

            result = await session.execute(stmt)
            properties = result.scalars().all()

            return [
                {
                    "id": str(p.id),
                    "code": p.code,
                    "title": p.title,
                    "property_kind": p.property_kind.value if p.property_kind else None,
                    "district": p.district,
                    "province": p.province,
                    "area_sqm": float(p.area_sqm) if p.area_sqm else None,
                    "bedrooms": p.bedrooms,
                    "bathrooms": p.bathrooms,
                    "list_price": float(p.list_price) if p.list_price else None,
                    "currency": p.currency,
                    "status": p.status.value if p.status else None,
                }
                for p in properties
            ]

    # Run sync wrapper (for LangChain tool)
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        results = loop.run_until_complete(_search())
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error searching properties: {e}")
        return json.dumps({"error": str(e)})


@tool
def check_property_availability(property_id: str) -> str:
    """Kiểm tra tình trạng sẵn sàng của một bất động sản.

    Args:
        property_id: UUID của bất động sản

    Returns:
        Thông tin về tình trạng bất động sản
    """
    import json
    from sqlalchemy import select, and_
    from datetime import datetime

    async def _check():
        async with get_session_context() as session:
            # Get property
            stmt = select(Property).where(Property.id == UUID(property_id))
            result = await session.execute(stmt)
            prop = result.scalar_one_or_none()

            if not prop:
                return {"error": "Property not found", "property_id": property_id}

            # Check for active hold
            hold_stmt = select(PropertyHold).where(
                and_(
                    PropertyHold.property_id == UUID(property_id),
                    PropertyHold.status == HoldStatus.ACTIVE,
                    PropertyHold.expires_at > datetime.utcnow(),
                )
            )
            hold_result = await session.execute(hold_stmt)
            active_hold = hold_result.scalar_one_or_none()

            return {
                "property_id": property_id,
                "code": prop.code,
                "title": prop.title,
                "status": prop.status.value if prop.status else None,
                "is_available": prop.status == PropertyStatus.AVAILABLE,
                "has_active_hold": active_hold is not None,
                "hold_expires_at": active_hold.expires_at.isoformat() if active_hold else None,
                "can_book": prop.status == PropertyStatus.AVAILABLE and active_hold is None,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_check())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error checking property: {e}")
        return json.dumps({"error": str(e)})


@tool
def hold_property(property_id: str, customer_id: str, hold_minutes: int = 15) -> str:
    """Giữ bất động sản tạm thời trong thời gian đặt lịch.

    Args:
        property_id: UUID của bất động sản
        customer_id: UUID của khách hàng
        hold_minutes: Số phút giữ căn (mặc định: 15)

    Returns:
        Thông tin về hold đã tạo
    """
    import json
    import uuid
    from sqlalchemy import select, and_
    from datetime import datetime, timedelta
    from src.database.models import PropertyHold, HoldStatus, Appointment, Property

    async def _hold():
        async with get_session_context() as session:
            # Check if property exists and is available
            prop_stmt = select(Property).where(Property.id == UUID(property_id))
            prop_result = await session.execute(prop_stmt)
            prop = prop_result.scalar_one_or_none()

            if not prop:
                return {"error": "Property not found"}

            # Check for existing active hold
            hold_check = select(PropertyHold).where(
                and_(
                    PropertyHold.property_id == UUID(property_id),
                    PropertyHold.status == HoldStatus.ACTIVE,
                    PropertyHold.expires_at > datetime.utcnow(),
                )
            )
            existing = await session.execute(hold_check)
            if existing.scalar_one_or_none():
                return {"error": "Property already has an active hold"}

            # Check if there's already an appointment (confirmed booking)
            apt_stmt = select(Appointment).where(
                and_(
                    Appointment.property_id == UUID(property_id),
                    Appointment.status.in_(["CONFIRMED", "IN_PROGRESS"]),
                )
            )
            apt_result = await session.execute(apt_stmt)
            if apt_result.scalar_one_or_none():
                return {"error": "Property is already booked"}

            # Create placeholder appointment for hold
            appointment_id = uuid.uuid4()
            booking_code = f"BK{uuid.uuid4().hex[:8].upper()}"

            appointment = Appointment(
                id=appointment_id,
                booking_code=booking_code,
                tour_request_id=uuid.uuid4(),  # Placeholder
                customer_user_id=UUID(customer_id),
                property_id=UUID(property_id),
                sale_user_id=uuid.uuid4(),  # Placeholder
                status="CONFIRMED",  # Placeholder
                starts_at=datetime.utcnow(),
                ends_at=datetime.utcnow() + timedelta(minutes=hold_minutes),
            )
            session.add(appointment)

            # Create hold
            now = datetime.utcnow()
            hold = PropertyHold(
                id=uuid.uuid4(),
                hold_code=f"HD{uuid.uuid4().hex[:8].upper()}",
                appointment_id=appointment_id,
                property_id=UUID(property_id),
                customer_user_id=UUID(customer_id),
                approved_by_user_id=uuid.uuid4(),  # System
                status=HoldStatus.ACTIVE,
                starts_at=now,
                expires_at=now + timedelta(minutes=hold_minutes),
                max_expires_at=now + timedelta(minutes=hold_minutes * 2),
            )
            session.add(hold)

            await session.flush()

            return {
                "success": True,
                "hold_id": str(hold.id),
                "hold_code": hold.hold_code,
                "property_id": property_id,
                "property_title": prop.title,
                "expires_at": hold.expires_at.isoformat(),
                "hold_minutes": hold_minutes,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_hold())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error holding property: {e}")
        return json.dumps({"error": str(e)})


@tool
def release_hold(hold_id: str, reason: str = "Manual release") -> str:
    """Giải phóng hold trên bất động sản.

    Args:
        hold_id: UUID của hold cần giải phóng
        reason: Lý do giải phóng

    Returns:
        Kết quả giải phóng
    """
    import json
    from datetime import datetime
    from sqlalchemy import select, update
    from src.database.models import PropertyHold, HoldStatus

    async def _release():
        async with get_session_context() as session:
            # Get hold
            stmt = select(PropertyHold).where(PropertyHold.id == UUID(hold_id))
            result = await session.execute(stmt)
            hold = result.scalar_one_or_none()

            if not hold:
                return {"error": "Hold not found"}

            if hold.status != HoldStatus.ACTIVE:
                return {"error": "Hold is not active", "current_status": hold.status.value}

            # Update hold status
            hold.status = HoldStatus.RELEASED
            hold.released_at = datetime.utcnow()
            hold.release_reason = reason

            await session.flush()

            return {
                "success": True,
                "hold_id": hold_id,
                "released_at": hold.released_at.isoformat(),
                "reason": reason,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_release())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error releasing hold: {e}")
        return json.dumps({"error": str(e)})


# Export all tools
__all__ = [
    "search_properties",
    "check_property_availability",
    "hold_property",
    "release_hold",
]
