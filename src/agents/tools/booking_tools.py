"""Booking and scheduling tools for the agent."""

import logging
from datetime import datetime, timedelta
from uuid import UUID

from langchain_core.tools import tool

from src.database.connection import get_session_context
from src.database.models import (
    Appointment,
    AppointmentStatus,
    Property,
)

logger = logging.getLogger(__name__)


@tool
def calculate_viewing_time(
    property_id: str,
    start_time: str,
    buffer_minutes: int | None = None,
) -> str:
    """Tính toán thời gian xem nhà dự kiến.

    Bao gồm thời gian cơ bản cho việc xem + buffer + thời gian di chuyển.

    Args:
        property_id: UUID của bất động sản
        start_time: Thời gian bắt đầu (ISO format)
        buffer_minutes: Thời gian buffer tùy chỉnh (mặc định: tự động tính)

    Returns:
        Thông tin về thời gian xem nhà
    """
    import json

    async def _calculate():
        async with get_session_context() as session:
            # Get property for base time
            from sqlalchemy import select
            stmt = select(Property).where(Property.id == UUID(property_id))
            result = await session.execute(stmt)
            prop = result.scalar_one_or_none()

            if not prop:
                return {"error": "Property not found"}

            # Base viewing time by property type
            base_minutes = {
                "APARTMENT": 30,
                "HOUSE": 45,
                "VILLA": 60,
                "TOWNHOUSE": 45,
                "LAND": 30,
                "COMMERCIAL": 30,
            }
            base_time = base_minutes.get(prop.property_kind.value, 30) if prop.property_kind else 30

            # Default buffer (can be customized)
            buffer = buffer_minutes or 15

            # Parse start time
            try:
                start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            except ValueError:
                start_dt = datetime.fromisoformat(start_time)

            # Calculate end time
            estimated_end = start_dt + timedelta(minutes=base_time + buffer)

            return {
                "property_id": property_id,
                "property_title": prop.title,
                "property_kind": prop.property_kind.value if prop.property_kind else None,
                "start_time": start_dt.isoformat(),
                "base_minutes": base_time,
                "buffer_minutes": buffer,
                "estimated_end": estimated_end.isoformat(),
                "total_minutes": base_time + buffer,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_calculate())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error calculating viewing time: {e}")
        return json.dumps({"error": str(e)})


@tool
def create_booking(
    customer_id: str,
    property_id: str,
    sale_user_id: str,
    starts_at: str,
    ends_at: str,
    customer_note: str | None = None,
    party_size: int = 1,
    pickup_address: str | None = None,
) -> str:
    """Tạo booking/appointment mới.

    Args:
        customer_id: UUID của khách hàng
        property_id: UUID của bất động sản
        sale_user_id: UUID của sale phụ trách
        starts_at: Thời gian bắt đầu (ISO format)
        ends_at: Thời gian kết thúc (ISO format)
        customer_note: Ghi chú từ khách hàng
        party_size: Số người đi cùng
        pickup_address: Địa chỉ đón (nếu cần)

    Returns:
        Thông tin booking đã tạo
    """
    import json
    import uuid


    async def _create():
        async with get_session_context() as session:
            # Generate booking code
            booking_code = f"BK{uuid.uuid4().hex[:8].upper()}"

            # Parse times
            try:
                start_dt = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
            except ValueError:
                return {"error": "Invalid datetime format"}

            # Create appointment
            appointment = Appointment(
                id=uuid.uuid4(),
                booking_code=booking_code,
                tour_request_id=uuid.uuid4(),  # Will be linked properly
                customer_user_id=UUID(customer_id),
                property_id=UUID(property_id),
                sale_user_id=UUID(sale_user_id),
                status=AppointmentStatus.CONFIRMED,
                starts_at=start_dt,
                ends_at=end_dt,
                party_size=party_size,
                customer_note=customer_note,
                pickup_address=pickup_address,
            )
            session.add(appointment)

            await session.flush()

            return {
                "success": True,
                "booking_id": str(appointment.id),
                "booking_code": appointment.booking_code,
                "property_id": property_id,
                "sale_user_id": sale_user_id,
                "starts_at": start_dt.isoformat(),
                "ends_at": end_dt.isoformat(),
                "status": appointment.status.value,
                "party_size": party_size,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_create())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        return json.dumps({"error": str(e)})


@tool
def propose_time_slots(
    property_id: str,
    customer_id: str,
    preferred_date: str,
    num_slots: int = 3,
) -> str:
    """Đề xuất các khung giờ xem nhà có sẵn.

    Args:
        property_id: UUID của bất động sản
        customer_id: UUID của khách hàng
        preferred_date: Ngày mong muốn (YYYY-MM-DD)
        num_slots: Số lượng khung giờ đề xuất (mặc định: 3)

    Returns:
        Danh sách các khung giờ đề xuất
    """
    import json
    import uuid

    from sqlalchemy import select

    from src.database.models import SaleProfile, User

    async def _propose():
        async with get_session_context() as session:
            # Parse preferred date
            try:
                pref_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Invalid date format, use YYYY-MM-DD"}

            # Get available sales (simplified - get first available)
            sales_stmt = select(SaleProfile, User).join(
                User, SaleProfile.user_id == User.id
            ).where(
                SaleProfile.is_accepting_tours.is_(True),
                User.status == "ACTIVE"
            ).limit(5)
            sales_result = await session.execute(sales_stmt)
            sales = sales_result.all()

            if not sales:
                return {"error": "No sale agents available"}

            # Generate time slots (9:00, 11:00, 14:00, 16:00)
            available_hours = [9, 11, 14, 16]
            slots = []

            for i, hour in enumerate(available_hours[:num_slots]):
                slot_start = datetime.combine(pref_date, datetime.min.time().replace(hour=hour))
                # End time = start + 1 hour
                slot_end = slot_start + timedelta(hours=1)

                # Calculate viewing time
                from sqlalchemy import select as sel
                prop_stmt = sel(Property).where(Property.id == UUID(property_id))
                prop_result = await session.execute(prop_stmt)
                prop = prop_result.scalar_one_or_none()
                base_minutes = 30
                if prop and prop.property_kind:
                    base_minutes = {"APARTMENT": 30, "HOUSE": 45, "VILLA": 60}.get(
                        prop.property_kind.value, 30
                    )

                slot_end = slot_start + timedelta(minutes=base_minutes + 15)

                slots.append({
                    "slot_id": str(uuid.uuid4()),
                    "sale_id": str(sales[0][0].user_id),  # First available sale
                    "sale_name": sales[0][1].full_name,
                    "starts_at": slot_start.isoformat(),
                    "ends_at": slot_end.isoformat(),
                    "estimated_duration_minutes": base_minutes + 15,
                    "score": 100 - (i * 10),  # Higher score for earlier slots
                })

            return {
                "property_id": property_id,
                "preferred_date": preferred_date,
                "available_slots": slots,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_propose())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error proposing slots: {e}")
        return json.dumps({"error": str(e)})


@tool
def get_booking_status(booking_id: str) -> str:
    """Lấy trạng thái của một booking.

    Args:
        booking_id: UUID của booking

    Returns:
        Thông tin trạng thái booking
    """
    import json

    from sqlalchemy import joinedload, select

    from src.database.models import User

    async def _get_status():
        async with get_session_context() as session:
            stmt = (
                select(Appointment)
                .options(
                    joinedload(Appointment.property),
                    joinedload(Appointment.sale),
                )
                .where(Appointment.id == UUID(booking_id))
            )
            result = await session.execute(stmt)
            apt = result.scalar_one_or_none()

            if not apt:
                return {"error": "Booking not found"}

            # Get sale name
            from sqlalchemy import select as sel
            user_stmt = sel(User).where(User.id == apt.sale_user_id)
            user_result = await session.execute(user_stmt)
            sale_user = user_result.scalar_one_or_none()

            return {
                "booking_id": booking_id,
                "booking_code": apt.booking_code,
                "status": apt.status.value,
                "starts_at": apt.starts_at.isoformat() if apt.starts_at else None,
                "ends_at": apt.ends_at.isoformat() if apt.ends_at else None,
                "property": {
                    "id": str(apt.property.id),
                    "code": apt.property.code,
                    "title": apt.property.title,
                    "address": apt.property.address_line,
                } if apt.property else None,
                "sale": {
                    "id": str(apt.sale_user_id),
                    "name": sale_user.full_name if sale_user else "Unknown",
                },
                "meeting_address": apt.meeting_address,
                "checked_in_at": apt.checked_in_at.isoformat() if apt.checked_in_at else None,
                "checked_out_at": apt.checked_out_at.isoformat() if apt.checked_out_at else None,
                "cancelled_at": apt.cancelled_at.isoformat() if apt.cancelled_at else None,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_get_status())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error getting booking status: {e}")
        return json.dumps({"error": str(e)})


@tool
def cancel_booking(booking_id: str, reason: str = "Customer requested") -> str:
    """Hủy một booking.

    Args:
        booking_id: UUID của booking cần hủy
        reason: Lý do hủy

    Returns:
        Kết quả hủy booking
    """
    import json

    from sqlalchemy import select

    from src.database.models import HoldStatus, PropertyHold

    async def _cancel():
        async with get_session_context() as session:
            # Get appointment
            stmt = select(Appointment).where(Appointment.id == UUID(booking_id))
            result = await session.execute(stmt)
            apt = result.scalar_one_or_none()

            if not apt:
                return {"error": "Booking not found"}

            if apt.status == AppointmentStatus.COMPLETED:
                return {"error": "Cannot cancel a completed booking"}

            if apt.status == AppointmentStatus.CANCELLED:
                return {"error": "Booking is already cancelled"}

            # Update status
            apt.status = AppointmentStatus.CANCELLED
            apt.cancelled_at = datetime.utcnow()
            apt.cancellation_reason = reason

            # Release any holds
            hold_stmt = select(PropertyHold).where(
                PropertyHold.appointment_id == apt.id,
                PropertyHold.status == HoldStatus.ACTIVE,
            )
            hold_result = await session.execute(hold_stmt)
            hold = hold_result.scalar_one_or_none()

            if hold:
                hold.status = HoldStatus.RELEASED
                hold.released_at = datetime.utcnow()
                hold.release_reason = f"Booking cancelled: {reason}"

            await session.flush()

            return {
                "success": True,
                "booking_id": booking_id,
                "booking_code": apt.booking_code,
                "status": "CANCELLED",
                "cancelled_at": apt.cancelled_at.isoformat(),
                "reason": reason,
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_cancel())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error cancelling booking: {e}")
        return json.dumps({"error": str(e)})


# Export all tools
__all__ = [
    "calculate_viewing_time",
    "create_booking",
    "propose_time_slots",
    "get_booking_status",
    "cancel_booking",
]
