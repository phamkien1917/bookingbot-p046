"""Scheduler Service - Background jobs for BookingBot."""

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import and_, select

from src.database.connection import get_session_context
from src.database.models import (
    Appointment,
    AppointmentStatus,
    HoldStatus,
    PropertyHold,
    SlotStatus,
    TourSlotOption,
)

logger = logging.getLogger(__name__)

# Global scheduler instance
_scheduler: AsyncIOScheduler | None = None


async def cleanup_expired_holds() -> None:
    """Release holds that have expired.

    This job runs every minute to release property holds
    that have passed their expiration time.
    """
    async with get_session_context() as session:
        now = datetime.utcnow()

        # Find expired holds
        stmt = select(PropertyHold).where(
            and_(
                PropertyHold.status == HoldStatus.ACTIVE,
                PropertyHold.expires_at <= now,
            )
        )
        result = await session.execute(stmt)
        expired_holds = result.scalars().all()

        for hold in expired_holds:
            hold.status = HoldStatus.EXPIRED
            hold.released_at = now
            hold.release_reason = "AUTO_EXPIRED"
            logger.info(f"Released expired hold: {hold.hold_code}")

        if expired_holds:
            logger.info(f"Cleaned up {len(expired_holds)} expired holds")


async def check_running_late() -> None:
    """Check for sales that are running late.

    This job runs every 5 minutes to check if any sale
    is past their estimated end time and mark them as late.
    """
    async with get_session_context() as session:
        now = datetime.utcnow()

        # Find appointments that are past their end time but not completed
        stmt = select(Appointment).where(
            and_(
                Appointment.ends_at < now,
                Appointment.status.in_([
                    AppointmentStatus.CONFIRMED,
                    AppointmentStatus.IN_PROGRESS,
                ]),
            )
        )
        result = await session.execute(stmt)
        late_appointments = result.scalars().all()

        for apt in late_appointments:
            # In production, this would update the sale's status
            # For now, just log
            delay_minutes = (now - apt.ends_at).total_seconds() / 60
            logger.warning(
                f"Sale {apt.sale_user_id} is running late on booking {apt.booking_code}. "
                f"Delay: {delay_minutes:.1f} minutes"
            )

        if late_appointments:
            logger.info(f"Found {len(late_appointments)} running late appointments")


async def expire_stale_slots() -> None:
    """Expire proposed slots that are past their valid time.

    This job runs every minute to expire slot options
    that were proposed but not selected in time.
    """
    async with get_session_context() as session:
        now = datetime.utcnow()

        # Find expired proposed slots
        stmt = select(TourSlotOption).where(
            and_(
                TourSlotOption.status == SlotStatus.PROPOSED,
                TourSlotOption.valid_until <= now,
            )
        )
        result = await session.execute(stmt)
        expired_slots = result.scalars().all()

        for slot in expired_slots:
            slot.status = SlotStatus.EXPIRED
            logger.info(f"Expired slot: {slot.id}")

        if expired_slots:
            logger.info(f"Expired {len(expired_slots)} stale slot options")


async def check_no_shows() -> None:
    """Check for no-show appointments.

    This job runs at the end of each day to mark appointments
    where the customer didn't show up.
    """
    async with get_session_context() as session:
        now = datetime.utcnow()

        # Find confirmed appointments that ended more than 30 minutes ago
        cutoff = now - timedelta(minutes=30)

        stmt = select(Appointment).where(
            and_(
                Appointment.status == AppointmentStatus.CONFIRMED,
                Appointment.ends_at < cutoff,
                Appointment.checked_in_at.is_(None),
            )
        )
        result = await session.execute(stmt)
        potential_no_shows = result.scalars().all()

        for apt in potential_no_shows:
            apt.status = AppointmentStatus.NO_SHOW
            logger.info(f"Marked no-show for booking: {apt.booking_code}")

        if potential_no_shows:
            logger.info(f"Marked {len(potential_no_shows)} no-show appointments")


def get_scheduler() -> AsyncIOScheduler:
    """Get or create the scheduler instance.

    Returns:
        AsyncIOScheduler instance
    """
    global _scheduler

    if _scheduler is None:
        _scheduler = AsyncIOScheduler()

    return _scheduler


async def start_scheduler() -> None:
    """Start the background scheduler.

    Adds all scheduled jobs to the scheduler.
    """
    scheduler = get_scheduler()

    if scheduler.running:
        logger.info("Scheduler already running")
        return

    # Add jobs
    # Hold expiration - every 1 minute
    scheduler.add_job(
        cleanup_expired_holds,
        trigger=IntervalTrigger(minutes=1),
        id="cleanup_expired_holds",
        name="Cleanup expired holds",
        replace_existing=True,
    )

    # Running late check - every 5 minutes
    scheduler.add_job(
        check_running_late,
        trigger=IntervalTrigger(minutes=5),
        id="check_running_late",
        name="Check running late",
        replace_existing=True,
    )

    # Slot expiration - every 1 minute
    scheduler.add_job(
        expire_stale_slots,
        trigger=IntervalTrigger(minutes=1),
        id="expire_stale_slots",
        name="Expire stale slots",
        replace_existing=True,
    )

    # No-show check - every 30 minutes
    scheduler.add_job(
        check_no_shows,
        trigger=IntervalTrigger(minutes=30),
        id="check_no_shows",
        name="Check no-shows",
        replace_existing=True,
    )

    # Start scheduler
    scheduler.start()
    logger.info("Background scheduler started")


async def stop_scheduler() -> None:
    """Stop the background scheduler."""
    global _scheduler

    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Background scheduler stopped")


def run_job_now(job_id: str) -> None:
    """Manually trigger a job by ID.

    Args:
        job_id: The job ID to run
    """
    scheduler = get_scheduler()
    job = scheduler.get_job(job_id)

    if job:
        job.modify(next_run_time=datetime.utcnow())
        logger.info(f"Triggered job: {job_id}")
    else:
        logger.warning(f"Job not found: {job_id}")
