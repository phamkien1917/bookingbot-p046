"""Notification Service - Send notifications via email, SMS, push."""

import logging
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Appointment, DeliveryStatus, Notification, NotificationChannel, User
from src.utils.time import utcnow

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications to users.

    Supports multiple channels:
    - IN_APP: In-app notifications
    - EMAIL: Email notifications
    - SMS: SMS notifications
    - WEB_PUSH: Web push notifications
    """

    # Notification templates
    TEMPLATES = {
        "booking_confirmed": {
            "title": "Xác nhận đặt lịch thành công",
            "template_key": "booking_confirmed",
        },
        "booking_reminder_48h": {
            "title": "Nhắc nhở lịch xem nhà",
            "template_key": "booking_reminder_48h",
        },
        "booking_reminder_24h": {
            "title": "Xác nhận lịch xem nhà",
            "template_key": "booking_reminder_24h",
        },
        "booking_reminder_2h": {
            "title": "Chuẩn bị xem nhà",
            "template_key": "booking_reminder_2h",
        },
        "sale_assigned": {
            "title": "Đã phân công sale",
            "template_key": "sale_assigned",
        },
        "booking_cancelled": {
            "title": "Lịch đã bị hủy",
            "template_key": "booking_cancelled",
        },
        "reschedule_proposed": {
            "title": "Đề xuất dời lịch",
            "template_key": "reschedule_proposed",
        },
    }

    def __init__(self):
        """Initialize notification service."""
        pass

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
        """Create a notification for sending.

        Args:
            user_id: Target user ID
            template_key: Template identifier
            payload: Template payload data
            channel: Delivery channel
            scheduled_at: When to send (None = send immediately)
            appointment_id: Related appointment ID

        Returns:
            Notification ID
        """
        import uuid

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
            
            # Broadcast to WebSocket
            from src.services.redis_service import get_event_pubsub
            pubsub = get_event_pubsub()
            payload_data = {
                "id": str(notification.id),
                "template_key": notification.template_key,
                "payload": notification.payload or {},
                "status": notification.status.value if hasattr(notification.status, "value") else notification.status,
                "created_at": notification.created_at.isoformat() if notification.created_at else utcnow().isoformat(),
            }
            await pubsub.publish(f"notifications:{user_id}", payload_data)
            
            return str(notification.id)

    async def send_booking_confirmation(
        self,
        db: AsyncSession,
        appointment_id: UUID,
    ) -> dict:
        """Send booking confirmation notification.

        Args:
            appointment_id: Appointment UUID

        Returns:
            Result dict
        """
        # Get appointment with related data
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        result = await db.execute(stmt)
        apt = result.scalar_one_or_none()

            if not apt:
                return {"error": "Appointment not found"}

        # Get customer
        user_stmt = select(User).where(User.id == apt.customer_user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

            if not user:
                return {"error": "User not found"}

            payload = {
                "booking_code": apt.booking_code,
                "date": apt.starts_at.strftime("%d/%m/%Y"),
                "time": apt.starts_at.strftime("%H:%M"),
                "property_address": apt.meeting_address or "Sẽ được thông báo",
            }

        # Create in-app notification
        notif_id = await self.create_notification(
            db=db,
            user_id=user.id,
            template_key="booking_confirmed",
            payload=payload,
            channel=NotificationChannel.IN_APP,
            appointment_id=apt.id,
        )

        return {
            "success": True,
            "notification_id": notif_id,
            "customer_id": str(user.id),
        }

    async def schedule_reminders(
        self,
        db: AsyncSession,
        appointment_id: UUID,
    ) -> list[str]:
        """Schedule reminder notifications for an appointment.

        Args:
            appointment_id: Appointment UUID

        Returns:
            List of notification IDs
        """
        # Get appointment
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        result = await db.execute(stmt)
        apt = result.scalar_one_or_none()

            if not apt:
                return []

            notification_ids = []

            # T - 48h reminder
            reminder_48h = apt.starts_at - timedelta(hours=48)
            if reminder_48h > utcnow():
                notif_id = await self.create_notification(
                    db=db,
                    user_id=apt.customer_user_id,
                    template_key="booking_reminder_48h",
                    payload={
                        "booking_code": apt.booking_code,
                        "date": apt.starts_at.strftime("%d/%m/%Y"),
                        "time": apt.starts_at.strftime("%H:%M"),
                    },
                    channel=NotificationChannel.EMAIL,
                    scheduled_at=reminder_48h,
                    appointment_id=apt.id,
                )
                notification_ids.append(notif_id)

            # T - 24h confirmation request
            reminder_24h = apt.starts_at - timedelta(hours=24)
            if reminder_24h > utcnow():
                notif_id = await self.create_notification(
                    db=db,
                    user_id=apt.customer_user_id,
                    template_key="booking_reminder_24h",
                    payload={
                        "booking_code": apt.booking_code,
                        "date": apt.starts_at.strftime("%d/%m/%Y"),
                        "time": apt.starts_at.strftime("%H:%M"),
                        "message": "Bạn có thể xác nhận tham gia không?",
                    },
                    channel=NotificationChannel.SMS,
                    scheduled_at=reminder_24h,
                    appointment_id=apt.id,
                )
                notification_ids.append(notif_id)

            # T - 2h preparation
            reminder_2h = apt.starts_at - timedelta(hours=2)
            if reminder_2h > utcnow():
                notif_id = await self.create_notification(
                    db=db,
                    user_id=apt.customer_user_id,
                    template_key="booking_reminder_2h",
                    payload={
                        "booking_code": apt.booking_code,
                        "time": apt.starts_at.strftime("%H:%M"),
                        "address": apt.meeting_address or "Địa điểm sẽ được thông báo",
                    },
                    channel=NotificationChannel.WEB_PUSH,
                    scheduled_at=reminder_2h,
                    appointment_id=apt.id,
                )
                notification_ids.append(notif_id)

            return notification_ids

    async def get_pending_notifications(
        self,
        db: AsyncSession,
        limit: int = 100,
    ) -> list[dict]:
        """Get pending notifications for processing.

        Args:
            limit: Max notifications to return

        Returns:
            List of pending notifications
        """
        stmt = (
            select(Notification, User)
            .join(User, Notification.user_id == User.id)
            .where(
                Notification.status == DeliveryStatus.PENDING,
                Notification.scheduled_at <= utcnow(),
            )
            .order_by(Notification.scheduled_at)
            .limit(limit)
        )
        result = await db.execute(stmt)
        notifications = result.all()

            return [
                {
                    "notification_id": str(notif.id),
                    "user_id": str(notif.user_id),
                    "user_email": user.email if user else None,
                    "user_phone": user.phone if user else None,
                    "channel": notif.channel.value,
                    "template_key": notif.template_key,
                    "payload": notif.payload,
                }
                for notif, user in notifications
            ]

    async def mark_sent(
        self,
        db: AsyncSession,
        notification_id: UUID,
    ) -> None:
        """Mark notification as sent.

        Args:
            notification_id: Notification UUID
        """
        stmt = update(Notification).where(
            Notification.id == notification_id
        ).values(
            status=DeliveryStatus.SENT,
            sent_at=utcnow(),
        )
        await db.execute(stmt)

    async def mark_delivered(
        self,
        db: AsyncSession,
        notification_id: UUID,
    ) -> None:
        """Mark notification as delivered.

        Args:
            notification_id: Notification UUID
        """
        stmt = update(Notification).where(
            Notification.id == notification_id
        ).values(
            status=DeliveryStatus.DELIVERED,
            delivered_at=utcnow(),
        )
        await db.execute(stmt)

    async def mark_failed(
        self,
        db: AsyncSession,
        notification_id: UUID,
        error: str,
    ) -> None:
        """Mark notification as failed.

        Args:
            notification_id: Notification UUID
            error: Error message
        """
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await db.execute(stmt)
        notif = result.scalar_one_or_none()

            if notif:
                notif.status = DeliveryStatus.FAILED
                notif.last_error = error
                notif.retry_count += 1


# Singleton instance
_notification_service: NotificationService | None = None


def get_notification_service() -> NotificationService:
    """Get notification service singleton."""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
