"""Notification creation and delivery-state helpers."""

import logging
import uuid
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Appointment, DeliveryStatus, Notification, NotificationChannel, User
from src.utils.time import utcnow

logger = logging.getLogger(__name__)


class NotificationService:
    """Create in-app notifications and schedule reminders."""

    async def create_notification(
        self,
        db: AsyncSession,
        user_id: UUID,
        template_key: str,
        payload: dict,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        scheduled_at: datetime | None = None,
        appointment_id: UUID | None = None,
    ) -> str:
        notification = Notification(
            id=uuid.uuid4(),
            user_id=user_id,
            appointment_id=appointment_id,
            channel=channel,
            template_key=template_key,
            payload=payload,
            scheduled_at=scheduled_at or utcnow(),
            status=DeliveryStatus.PENDING,
        )
        db.add(notification)
        await db.flush()

        try:
            from src.services.redis_service import get_event_pubsub

            event = {
                "id": str(notification.id),
                "template_key": notification.template_key,
                "payload": notification.payload or {},
                "status": notification.status.value,
                "created_at": (
                    notification.created_at.isoformat() if notification.created_at else utcnow().isoformat()
                ),
            }
            await get_event_pubsub().publish(f"notifications:{user_id}", event)
        except Exception:
            logger.warning("Notification event broadcast unavailable", exc_info=True)

        return str(notification.id)

    async def send_booking_confirmation(self, db: AsyncSession, appointment_id: UUID) -> dict:
        appointment = await db.get(Appointment, appointment_id)
        if not appointment:
            return {"error": "Appointment not found"}

        user = await db.get(User, appointment.customer_user_id)
        if not user:
            return {"error": "User not found"}

        notification_id = await self.create_notification(
            db=db,
            user_id=user.id,
            template_key="booking_confirmed",
            payload={
                "booking_code": appointment.booking_code,
                "date": appointment.starts_at.strftime("%d/%m/%Y"),
                "time": appointment.starts_at.strftime("%H:%M"),
                "property_address": appointment.meeting_address or "Sẽ được thông báo",
            },
            appointment_id=appointment.id,
        )
        return {
            "success": True,
            "notification_id": notification_id,
            "customer_id": str(user.id),
        }

    async def schedule_reminders(self, db: AsyncSession, appointment_id: UUID) -> list[str]:
        appointment = await db.get(Appointment, appointment_id)
        if not appointment:
            return []

        reminders = (
            (48, "booking_reminder_48h", NotificationChannel.EMAIL),
            (24, "booking_reminder_24h", NotificationChannel.SMS),
            (2, "booking_reminder_2h", NotificationChannel.WEB_PUSH),
        )
        notification_ids: list[str] = []
        for hours, template_key, channel in reminders:
            scheduled_at = appointment.starts_at - timedelta(hours=hours)
            if scheduled_at <= utcnow().astimezone(scheduled_at.tzinfo):
                continue
            notification_ids.append(
                await self.create_notification(
                    db=db,
                    user_id=appointment.customer_user_id,
                    template_key=template_key,
                    payload={
                        "booking_code": appointment.booking_code,
                        "date": appointment.starts_at.strftime("%d/%m/%Y"),
                        "time": appointment.starts_at.strftime("%H:%M"),
                        "address": appointment.meeting_address or "Địa điểm sẽ được thông báo",
                    },
                    channel=channel,
                    scheduled_at=scheduled_at,
                    appointment_id=appointment.id,
                )
            )
        return notification_ids

    async def get_pending_notifications(self, db: AsyncSession, limit: int = 100) -> list[dict]:
        statement = (
            select(Notification, User)
            .join(User, Notification.user_id == User.id)
            .where(
                Notification.status == DeliveryStatus.PENDING,
                Notification.scheduled_at <= utcnow(),
            )
            .order_by(Notification.scheduled_at)
            .limit(limit)
        )
        notifications = (await db.execute(statement)).all()
        return [
            {
                "notification_id": str(notification.id),
                "user_id": str(notification.user_id),
                "user_email": user.email,
                "user_phone": user.phone,
                "channel": notification.channel.value,
                "template_key": notification.template_key,
                "payload": notification.payload,
            }
            for notification, user in notifications
        ]

    async def mark_sent(self, db: AsyncSession, notification_id: UUID) -> None:
        await db.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=DeliveryStatus.SENT, sent_at=utcnow())
        )

    async def mark_delivered(self, db: AsyncSession, notification_id: UUID) -> None:
        await db.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=DeliveryStatus.DELIVERED, delivered_at=utcnow())
        )

    async def mark_failed(self, db: AsyncSession, notification_id: UUID, error: str) -> None:
        notification = await db.get(Notification, notification_id)
        if notification:
            notification.status = DeliveryStatus.FAILED
            notification.last_error = error
            notification.retry_count += 1


_notification_service: NotificationService | None = None


def get_notification_service() -> NotificationService:
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
