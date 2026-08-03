"""Notification Service - Send notifications via email, SMS, push."""

import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_session_context
from src.database.models import Notification, NotificationChannel, DeliveryStatus, Appointment, User

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
        user_id: UUID,
        template_key: str,
        payload: dict,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        scheduled_at: Optional[datetime] = None,
        appointment_id: Optional[UUID] = None,
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

        async with get_session_context() as session:
            notification = Notification(
                id=uuid.uuid4(),
                user_id=user_id,
                appointment_id=appointment_id,
                channel=channel,
                template_key=template_key,
                payload=payload,
                scheduled_at=scheduled_at or datetime.utcnow(),
                status=DeliveryStatus.PENDING,
            )
            session.add(notification)
            await session.flush()
            return str(notification.id)

    async def send_booking_confirmation(
        self,
        appointment_id: UUID,
    ) -> dict:
        """Send booking confirmation notification.

        Args:
            appointment_id: Appointment UUID

        Returns:
            Result dict
        """
        async with get_session_context() as session:
            # Get appointment with related data
            stmt = select(Appointment).where(Appointment.id == appointment_id)
            result = await session.execute(stmt)
            apt = result.scalar_one_or_none()

            if not apt:
                return {"error": "Appointment not found"}

            # Get customer
            user_stmt = select(User).where(User.id == apt.customer_user_id)
            user_result = await session.execute(user_stmt)
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
        appointment_id: UUID,
    ) -> list[str]:
        """Schedule reminder notifications for an appointment.

        Args:
            appointment_id: Appointment UUID

        Returns:
            List of notification IDs
        """
        async with get_session_context() as session:
            # Get appointment
            stmt = select(Appointment).where(Appointment.id == appointment_id)
            result = await session.execute(stmt)
            apt = result.scalar_one_or_none()

            if not apt:
                return []

            notification_ids = []

            # T - 48h reminder
            reminder_48h = apt.starts_at - timedelta(hours=48)
            if reminder_48h > datetime.utcnow():
                notif_id = await self.create_notification(
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
            if reminder_24h > datetime.utcnow():
                notif_id = await self.create_notification(
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
            if reminder_2h > datetime.utcnow():
                notif_id = await self.create_notification(
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
        limit: int = 100,
    ) -> list[dict]:
        """Get pending notifications for processing.

        Args:
            limit: Max notifications to return

        Returns:
            List of pending notifications
        """
        async with get_session_context() as session:
            stmt = (
                select(Notification, User)
                .join(User, Notification.user_id == User.id)
                .where(
                    Notification.status == DeliveryStatus.PENDING,
                    Notification.scheduled_at <= datetime.utcnow(),
                )
                .order_by(Notification.scheduled_at)
                .limit(limit)
            )
            result = await session.execute(stmt)
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
        notification_id: UUID,
    ) -> None:
        """Mark notification as sent.

        Args:
            notification_id: Notification UUID
        """
        async with get_session_context() as session:
            stmt = update(Notification).where(
                Notification.id == notification_id
            ).values(
                status=DeliveryStatus.SENT,
                sent_at=datetime.utcnow(),
            )
            await session.execute(stmt)

    async def mark_delivered(
        self,
        notification_id: UUID,
    ) -> None:
        """Mark notification as delivered.

        Args:
            notification_id: Notification UUID
        """
        async with get_session_context() as session:
            stmt = update(Notification).where(
                Notification.id == notification_id
            ).values(
                status=DeliveryStatus.DELIVERED,
                delivered_at=datetime.utcnow(),
            )
            await session.execute(stmt)

    async def mark_failed(
        self,
        notification_id: UUID,
        error: str,
    ) -> None:
        """Mark notification as failed.

        Args:
            notification_id: Notification UUID
            error: Error message
        """
        async with get_session_context() as session:
            stmt = select(Notification).where(Notification.id == notification_id)
            result = await session.execute(stmt)
            notif = result.scalar_one_or_none()

            if notif:
                notif.status = DeliveryStatus.FAILED
                notif.last_error = error
                notif.retry_count += 1


# Singleton instance
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """Get notification service singleton."""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
