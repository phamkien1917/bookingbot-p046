"""Assignment Engine - Sale agent assignment and routing optimization."""

import logging
from datetime import datetime
from src.utils.time import utcnow
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_session_context
from src.database.models import (
    Appointment,
    AppointmentStatus,
    SaleProfile,
    User,
)

logger = logging.getLogger(__name__)


class AssignmentEngine:
    """Engine for assigning sale agents to bookings.

    Uses a weighted scoring system:
    - Route Efficiency (30%): Phù hợp với lộ trình
    - Workload (20%): Ít booking trong ngày hơn được ưu tiên
    - Performance (20%): Dựa trên tỷ lệ chốt sale tháng
    - Response Time (15%): Sale phản hồi nhanh
    - Customer Rating (15%): Đánh giá từ khách
    """

    # Weights for scoring
    WEIGHTS = {
        "route_efficiency": 0.30,
        "workload": 0.20,
        "performance": 0.20,
        "response_time": 0.15,
        "customer_rating": 0.15,
    }

    def __init__(self):
        """Initialize the assignment engine."""
        pass

    async def calculate_route_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
        booking: Appointment,
    ) -> float:
        """Calculate route efficiency score.

        Args:
            session: Database session
            sale_id: Sale user ID
            booking: Target booking

        Returns:
            Score from 0-100
        """
        # Get sale's existing appointments for the day
        today = utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        stmt = select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == sale_id,
            Appointment.starts_at >= today_start,
            Appointment.starts_at <= today_end,
            Appointment.status.in_(["CONFIRMED", "IN_PROGRESS"]),
        )
        result = await session.execute(stmt)
        appointment_count = result.scalar() or 0

        # More appointments = lower route score
        # Assuming max ~8 appointments per day is reasonable
        base_score = max(0, 100 - (appointment_count * 12.5))
        return base_score

    async def calculate_workload_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
    ) -> float:
        """Calculate workload score.

        Args:
            session: Database session
            sale_id: Sale user ID

        Returns:
            Score from 0-100
        """
        # Get sale profile
        stmt = select(SaleProfile).where(SaleProfile.user_id == sale_id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            return 0.0

        max_tours = profile.max_daily_tours or 8

        # Get today's appointment count
        today = utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())

        count_stmt = select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == sale_id,
            Appointment.starts_at >= today_start,
            Appointment.status.in_(["CONFIRMED", "IN_PROGRESS"]),
        )
        count_result = await session.execute(count_stmt)
        current_count = count_result.scalar() or 0

        # Fewer bookings = higher score
        score = max(0, 100 - (current_count / max_tours * 100))
        return score

    async def calculate_performance_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
    ) -> float:
        """Calculate performance score.

        Args:
            session: Database session
            sale_id: Sale user ID

        Returns:
            Score from 0-100
        """
        # Simplified: Use appointment completion rate as proxy
        # In production, this would use actual sales conversion data
        start_of_month = utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Completed appointments this month
        completed_stmt = select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == sale_id,
            Appointment.starts_at >= start_of_month,
            Appointment.status == AppointmentStatus.COMPLETED,
        )
        completed_result = await session.execute(completed_stmt)
        completed = completed_result.scalar() or 0

        # Total appointments this month
        total_stmt = select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == sale_id,
            Appointment.starts_at >= start_of_month,
        )
        total_result = await session.execute(total_stmt)
        total = total_result.scalar() or 0

        if total == 0:
            return 75.0  # Default score for new sales

        completion_rate = (completed / total) * 100
        return min(100, completion_rate + 25)  # Boost base score

    async def calculate_response_time_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
    ) -> float:
        """Calculate response time score.

        Args:
            session: Database session
            sale_id: Sale user ID

        Returns:
            Score from 0-100
        """
        # Simplified: Return default score
        # In production, this would track actual response times
        return 85.0

    async def calculate_rating_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
    ) -> float:
        """Calculate customer rating score.

        Args:
            session: Database session
            sale_id: Sale user ID

        Returns:
            Score from 0-100
        """
        # Simplified: Return default score
        # In production, this would use actual customer ratings
        return 80.0

    async def calculate_total_score(
        self,
        session: AsyncSession,
        sale_id: UUID,
        booking: Appointment | None = None,
    ) -> dict:
        """Calculate total assignment score for a sale.

        Args:
            session: Database session
            sale_id: Sale user ID
            booking: Target booking

        Returns:
            Dict with total score and breakdown
        """
        # Get individual scores
        route_score = await self.calculate_route_score(session, sale_id, booking) if booking else 80
        workload_score = await self.calculate_workload_score(session, sale_id)
        perf_score = await self.calculate_performance_score(session, sale_id)
        response_score = await self.calculate_response_time_score(session, sale_id)
        rating_score = await self.calculate_rating_score(session, sale_id)

        # Calculate weighted total
        total = (
            route_score * self.WEIGHTS["route_efficiency"] +
            workload_score * self.WEIGHTS["workload"] +
            perf_score * self.WEIGHTS["performance"] +
            response_score * self.WEIGHTS["response_time"] +
            rating_score * self.WEIGHTS["customer_rating"]
        )

        return {
            "total": round(total, 2),
            "breakdown": {
                "route_efficiency": round(route_score, 2),
                "workload": round(workload_score, 2),
                "performance": round(perf_score, 2),
                "response_time": round(response_score, 2),
                "customer_rating": round(rating_score, 2),
            },
        }

    async def get_available_sales(
        self,
        session: AsyncSession,
        booking: Appointment | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """Get available sales with scores.

        Args:
            session: Database session
            booking: Target booking
            limit: Max results

        Returns:
            List of sales with scores
        """
        # Get active, accepting tours sales
        stmt = (
            select(SaleProfile, User)
            .join(User, SaleProfile.user_id == User.id)
            .where(
                SaleProfile.is_accepting_tours.is_(True),
                User.status == "ACTIVE",
            )
        )
        result = await session.execute(stmt)
        sales = result.all()

        scored_sales = []
        for profile, user in sales:
            score_data = await self.calculate_total_score(session, profile.user_id, booking)
            scored_sales.append({
                "sale_id": str(profile.user_id),
                "sale_name": user.full_name,
                "employee_code": profile.employee_code,
                "branch_name": profile.branch_name,
                "score": score_data["total"],
                "score_breakdown": score_data["breakdown"],
            })

        # Sort by score descending
        scored_sales.sort(key=lambda x: x["score"], reverse=True)

        return scored_sales[:limit]

    async def assign_best_sale(
        self,
        booking_id: UUID,
    ) -> dict:
        """Assign the best available sale to a booking.

        Args:
            booking_id: Booking UUID

        Returns:
            Assignment result
        """
        async with get_session_context() as session:
            # Get booking
            apt_stmt = select(Appointment).where(Appointment.id == booking_id)
            apt_result = await session.execute(apt_stmt)
            booking = apt_result.scalar_one_or_none()

            if not booking:
                return {"error": "Booking not found"}

            # Get available sales
            available = await self.get_available_sales(session, booking, limit=1)

            if not available:
                return {"error": "No sales available"}

            best = available[0]

            # Update booking
            booking.sale_user_id = UUID(best["sale_id"])
            await session.flush()

            return {
                "success": True,
                "booking_id": str(booking_id),
                "sale_id": best["sale_id"],
                "sale_name": best["sale_name"],
                "score": best["score"],
            }


# Singleton instance
_assignment_engine: AssignmentEngine | None = None


def get_assignment_engine() -> AssignmentEngine:
    """Get assignment engine singleton."""
    global _assignment_engine
    if _assignment_engine is None:
        _assignment_engine = AssignmentEngine()
    return _assignment_engine
