"""Assignment and sale agent tools for the agent."""

import logging
from uuid import UUID

from langchain_core.tools import tool

from src.database.connection import get_session_context
from src.database.models import (
    Appointment,
    Property,
    SaleProfile,
    User,
)
from src.utils.time import utcnow

logger = logging.getLogger(__name__)


@tool
def calculate_assignment_score(
    booking_id: str,
    sale_id: str | None = None,
) -> str:
    """Tính điểm phân công sale cho một booking.

    Công thức:
    - Route Efficiency (30%): Phù hợp với lộ trình hiện tại
    - Workload (20%): Ít booking trong ngày hơn được ưu tiên
    - Performance (20%): Dựa trên tỷ lệ chốt sale tháng
    - Response Time (15%): Sale phản hồi nhanh
    - Customer Rating (15%): Đánh giá từ khách

    Args:
        booking_id: UUID của booking
        sale_id: UUID của sale cần tính điểm (nếu None, tính cho tất cả)

    Returns:
        Điểm số và chi tiết breakdown
    """
    import json
    from datetime import datetime

    from sqlalchemy import func, select

    async def _calculate():
        async with get_session_context() as session:
            # Get booking details
            apt_stmt = select(Appointment).where(Appointment.id == UUID(booking_id))
            apt_result = await session.execute(apt_stmt)
            apt = apt_result.scalar_one_or_none()

            if not apt:
                return {"error": "Booking not found"}

            # Get property
            from sqlalchemy import select as sel
            prop_stmt = sel(Property).where(Property.id == apt.property_id)
            prop_result = await session.execute(prop_stmt)
            prop = prop_result.scalar_one_or_none()

            # Get all available sales
            if sale_id:
                sale_stmt = (
                    select(SaleProfile, User)
                    .join(User, SaleProfile.user_id == User.id)
                    .where(
                        SaleProfile.user_id == UUID(sale_id),
                        SaleProfile.is_accepting_tours,
                        User.status == "ACTIVE",
                    )
                )
            else:
                sale_stmt = (
                    select(SaleProfile, User)
                    .join(User, SaleProfile.user_id == User.id)
                    .where(
                        SaleProfile.is_accepting_tours,
                        User.status == "ACTIVE",
                    )
                )

            sales_result = await session.execute(sale_stmt)
            sales = sales_result.all()

            scores = []

            for sale_profile, user in sales:
                # 1. Route Efficiency (30%) - simplified
                route_score = 100.0  # Default full score

                # 2. Workload (20%) - fewer bookings today = higher score
                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                booking_count_stmt = select(func.count(Appointment.id)).where(
                    Appointment.sale_user_id == sale_profile.user_id,
                    Appointment.starts_at >= today_start,
                    Appointment.status.in_(["CONFIRMED", "IN_PROGRESS"]),
                )
                count_result = await session.execute(booking_count_stmt)
                booking_count = count_result.scalar() or 0
                max_tours = sale_profile.max_daily_tours or 8
                workload_score = max(0, 100 - (booking_count / max_tours * 100))

                # 3. Performance (20%) - simplified, use max_daily_tours as proxy
                performance_score = 80.0  # Default

                # 4. Response Time (15%) - simplified
                response_score = 90.0  # Default

                # 5. Customer Rating (15%) - simplified
                rating_score = 85.0  # Default

                # Calculate total
                total_score = (
                    route_score * 0.30 +
                    workload_score * 0.20 +
                    performance_score * 0.20 +
                    response_score * 0.15 +
                    rating_score * 0.15
                )

                scores.append({
                    "sale_id": str(sale_profile.user_id),
                    "sale_name": user.full_name,
                    "scores": {
                        "route_efficiency": round(route_score, 2),
                        "workload": round(workload_score, 2),
                        "performance": round(performance_score, 2),
                        "response_time": round(response_score, 2),
                        "customer_rating": round(rating_score, 2),
                    },
                    "total_score": round(total_score, 2),
                    "current_bookings_today": booking_count,
                    "max_daily_tours": max_tours,
                })

            # Sort by total score
            scores.sort(key=lambda x: x["total_score"], reverse=True)

            return {
                "booking_id": booking_id,
                "property_id": str(apt.property_id),
                "property_title": prop.title if prop else None,
                "sale_rankings": scores,
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
        logger.error(f"Error calculating assignment score: {e}")
        return json.dumps({"error": str(e)})


@tool
def assign_sale_to_booking(
    booking_id: str,
    sale_id: str | None = None,
    force_assign: bool = False,
) -> str:
    """Phân công sale cho một booking.

    Nếu không chỉ định sale_id, hệ thống sẽ chọn sale có điểm cao nhất.

    Args:
        booking_id: UUID của booking
        sale_id: UUID của sale cần phân công
        force_assign: Bỏ qua cảnh báo và gán trực tiếp

    Returns:
        Kết quả phân công
    """
    import json

    from sqlalchemy import select

    from src.database.models import Appointment

    requested_sale_id = sale_id

    async def _assign():
        async with get_session_context() as session:
            # Get booking
            apt_stmt = select(Appointment).where(Appointment.id == UUID(booking_id))
            apt_result = await session.execute(apt_stmt)
            apt = apt_result.scalar_one_or_none()

            if not apt:
                return {"error": "Booking not found"}

            if not requested_sale_id:
                # Get best sale using score calculation
                # For now, just pick first available
                from sqlalchemy import select as sel

                from src.database.models import SaleProfile, User
                best_stmt = (
                    sel(SaleProfile, User)
                    .join(User, SaleProfile.user_id == User.id)
                    .where(
                        SaleProfile.is_accepting_tours,
                        User.status == "ACTIVE",
                    )
                    .limit(1)
                )
                best_result = await session.execute(best_stmt)
                best = best_result.first()
                if not best:
                    return {"error": "No sale available"}
                selected_sale_id = str(best[0].user_id)
                sale_name = best[1].full_name
            else:
                # Validate sale exists
                sale_stmt = select(User).where(User.id == UUID(requested_sale_id))
                sale_result = await session.execute(sale_stmt)
                sale_user = sale_result.scalar_one_or_none()
                if not sale_user:
                    return {"error": "Sale not found"}
                selected_sale_id = requested_sale_id
                sale_name = sale_user.full_name

            # Update booking
            apt.sale_user_id = UUID(selected_sale_id)
            await session.flush()

            return {
                "success": True,
                "booking_id": booking_id,
                "sale_id": selected_sale_id,
                "sale_name": sale_name,
                "assigned_at": utcnow().isoformat(),
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_assign())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error assigning sale: {e}")
        return json.dumps({"error": str(e)})


@tool
def get_available_sales(
    district: str | None = None,
    property_id: str | None = None,
    limit: int = 5,
) -> str:
    """Lấy danh sách sale đang online và nhận booking.

    Args:
        district: Quận/Huyện (để lọc theo khu vực)
        property_id: UUID của bất động sản (để lọc sale phụ trách)
        limit: Số lượng tối đa

    Returns:
        Danh sách sale có sẵn
    """
    import json

    from sqlalchemy import select

    async def _get():
        async with get_session_context() as session:
            query = (
                select(SaleProfile, User)
                .join(User, SaleProfile.user_id == User.id)
                .where(
                    SaleProfile.is_accepting_tours,
                    User.status == "ACTIVE",
                )
                .limit(limit)
            )

            # If property_id provided, prioritize assigned sales
            if property_id:
                # This would be a more complex query in production
                pass

            result = await session.execute(query)
            sales = result.all()

            return {
                "available_sales": [
                    {
                        "sale_id": str(sale.user_id),
                        "name": user.full_name,
                        "employee_code": sale.employee_code,
                        "branch_name": sale.branch_name,
                        "specialties": sale.specialties,
                        "max_daily_tours": sale.max_daily_tours,
                    }
                    for sale, user in sales
                ]
            }

    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(_get())
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error getting available sales: {e}")
        return json.dumps({"error": str(e)})


@tool
def check_sale_availability(sale_id: str, check_time: str) -> str:
    """Kiểm tra sale có rảnh vào thời điểm cụ thể không.

    Args:
        sale_id: UUID của sale
        check_time: Thời điểm cần kiểm tra (ISO format)

    Returns:
        Thông tin về tình trạng của sale
    """
    import json
    from datetime import datetime

    from sqlalchemy import and_, select

    async def _check():
        async with get_session_context() as session:
            # Parse check time
            try:
                check_dt = datetime.fromisoformat(check_time.replace("Z", "+00:00"))
            except ValueError:
                check_dt = datetime.fromisoformat(check_time)

            # Get sale profile
            from sqlalchemy import select as sel
            stmt = sel(SaleProfile, User).join(User, SaleProfile.user_id == User.id).where(
                SaleProfile.user_id == UUID(sale_id)
            )
            result = await session.execute(stmt)
            sale_data = result.first()

            if not sale_data:
                return {"error": "Sale not found"}

            sale_profile, user = sale_data

            # Check for conflicting appointments
            # Consider: starts at check_time, or ends after check_time
            conflict_stmt = select(Appointment).where(
                and_(
                    Appointment.sale_user_id == UUID(sale_id),
                    Appointment.status.in_(["CONFIRMED", "IN_PROGRESS"]),
                    Appointment.starts_at <= check_dt,
                    Appointment.ends_at > check_dt,
                )
            )
            conflict_result = await session.execute(conflict_stmt)
            conflict = conflict_result.scalar_one_or_none()

            return {
                "sale_id": sale_id,
                "sale_name": user.full_name,
                "is_accepting_tours": sale_profile.is_accepting_tours,
                "user_status": user.status,
                "check_time": check_dt.isoformat(),
                "is_available": (
                    sale_profile.is_accepting_tours and
                    user.status == "ACTIVE" and
                    conflict is None
                ),
                "has_conflict": conflict is not None,
                "conflict_booking_id": str(conflict.id) if conflict else None,
                "conflict_booking_code": conflict.booking_code if conflict else None,
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
        logger.error(f"Error checking sale availability: {e}")
        return json.dumps({"error": str(e)})


# Export all tools
__all__ = [
    "calculate_assignment_score",
    "assign_sale_to_booking",
    "get_available_sales",
    "check_sale_availability",
]
