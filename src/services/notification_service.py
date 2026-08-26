"""Booking confirmation/reminder scheduling and multi-channel delivery."""

from __future__ import annotations

import logging
from datetime import timedelta

import httpx
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database.models import (
    Appointment,
    DeliveryStatus,
    Notification,
    NotificationChannel,
    User,
)
from src.services.analytics_service import record_event
from src.services.email_service import send_transactional_email
from src.utils.time import utcnow

logger = logging.getLogger(__name__)


def _message(payload: dict, template_key: str) -> tuple[str, str]:
    booking_code = payload.get("booking_code", "")
    property_title = payload.get("property_title", "căn nhà")
    starts_at = payload.get("starts_at", "")
    confirmed = template_key == "booking_confirmed"
    subject = f"{'Xác nhận' if confirmed else 'Nhắc'} lịch xem nhà {booking_code}".strip()
    body = (
        f"Nera Home {'đã xác nhận' if confirmed else 'nhắc bạn'} lịch xem {property_title}.\n"
        f"Thời gian: {starts_at}\nMã lịch: {booking_code}\n"
        "Nếu cần dời hoặc hủy lịch, vui lòng thao tác trong ứng dụng."
    )
    return subject, body


def _configured_channels() -> list[NotificationChannel]:
    settings = get_settings()
    channels: list[NotificationChannel] = []
    if settings.smtp_host and settings.smtp_from_email:
        channels.append(NotificationChannel.EMAIL)
    if settings.sms_provider_url and settings.sms_provider_token:
        channels.append(NotificationChannel.SMS)
    if settings.zalo_oa_url and settings.zalo_oa_token:
        channels.append(NotificationChannel.ZALO)
    return channels


async def schedule_booking_reminders(db: AsyncSession, appointment: Appointment, property_title: str) -> int:
    """Create idempotent reminder jobs for configured external channels and in-app."""
    settings = get_settings()
    try:
        reminder_hours = sorted({int(item.strip()) for item in settings.reminder_hours_before.split(",") if item.strip()}, reverse=True)
    except ValueError:
        reminder_hours = [24, 2]
    channels = [NotificationChannel.IN_APP, *_configured_channels()]
    now = utcnow()
    created = 0
    confirmation_payload = {
        "booking_code": appointment.booking_code,
        "property_title": property_title,
        "starts_at": appointment.starts_at.isoformat(),
    }
    for channel in _configured_channels():
        exists = await db.scalar(select(Notification.id).where(
            Notification.appointment_id == appointment.id,
            Notification.channel == channel,
            Notification.template_key == "booking_confirmed",
        ))
        if not exists:
            db.add(Notification(
                user_id=appointment.customer_user_id,
                appointment_id=appointment.id,
                channel=channel,
                template_key="booking_confirmed",
                payload=confirmation_payload,
                scheduled_at=now,
                status=DeliveryStatus.PENDING,
            ))
            created += 1
    for hours in reminder_hours:
        scheduled_at = appointment.starts_at - timedelta(hours=hours)
        if scheduled_at <= now:
            continue
        template_key = f"booking_reminder_{hours}h"
        for channel in channels:
            exists = await db.scalar(select(Notification.id).where(
                Notification.appointment_id == appointment.id,
                Notification.channel == channel,
                Notification.template_key == template_key,
            ))
            if exists:
                continue
            db.add(Notification(
                user_id=appointment.customer_user_id,
                appointment_id=appointment.id,
                channel=channel,
                template_key=template_key,
                payload={
                    "booking_code": appointment.booking_code,
                    "property_title": property_title,
                    "starts_at": appointment.starts_at.isoformat(),
                    "hours_before": hours,
                },
                scheduled_at=scheduled_at,
                status=DeliveryStatus.PENDING,
            ))
            created += 1
    record_event(
        db,
        "reminders_scheduled",
        customer_user_id=appointment.customer_user_id,
        appointment_id=appointment.id,
        properties={"count": created, "hours": reminder_hours},
    )
    return created


async def cancel_appointment_notifications(db: AsyncSession, appointment_id) -> None:
    await db.execute(
        update(Notification)
        .where(
            Notification.appointment_id == appointment_id,
            Notification.status == DeliveryStatus.PENDING,
            Notification.template_key.like("booking_reminder_%"),
        )
        .values(status=DeliveryStatus.CANCELLED)
    )


async def _send_provider(
    channel: NotificationChannel,
    recipient: User,
    payload: dict,
    template_key: str,
) -> bool:
    settings = get_settings()
    subject, body = _message(payload, template_key)
    if channel == NotificationChannel.EMAIL:
        return await send_transactional_email(recipient.email, subject, body)

    if channel == NotificationChannel.SMS:
        url, token = settings.sms_provider_url, settings.sms_provider_token
        provider_payload = {"to": recipient.phone, "message": body}
    elif channel == NotificationChannel.ZALO:
        url, token = settings.zalo_oa_url, settings.zalo_oa_token
        provider_payload = {
            "recipient": {"user_id": payload.get("zalo_user_id") or recipient.phone},
            "message": {"text": body},
        }
    else:
        return False
    if not url or not token or not recipient.phone:
        return False
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=provider_payload,
        )
        response.raise_for_status()
    return True


async def dispatch_due_notifications(db: AsyncSession, *, limit: int = 100) -> tuple[int, int]:
    """Deliver due external notifications with bounded retries."""
    rows = (await db.execute(
        select(Notification, User)
        .join(User, User.id == Notification.user_id)
        .where(
            Notification.status == DeliveryStatus.PENDING,
            Notification.scheduled_at <= utcnow(),
            Notification.channel.in_([
                NotificationChannel.EMAIL,
                NotificationChannel.SMS,
                NotificationChannel.ZALO,
            ]),
            Notification.retry_count < 3,
        )
        .order_by(Notification.scheduled_at)
        .limit(limit)
        .with_for_update(skip_locked=True)
    )).all()
    sent = failed = 0
    for notification, recipient in rows:
        try:
            delivered = await _send_provider(
                notification.channel,
                recipient,
                notification.payload or {},
                notification.template_key,
            )
            if not delivered:
                raise RuntimeError("Provider is not configured or recipient is missing")
            notification.status = DeliveryStatus.SENT
            notification.sent_at = utcnow()
            notification.last_error = None
            sent += 1
            record_event(
                db,
                "reminder_sent",
                customer_user_id=notification.user_id,
                appointment_id=notification.appointment_id,
                properties={"channel": notification.channel.value, "template": notification.template_key},
            )
        except Exception as exc:
            logger.warning("Notification %s delivery failed: %s", notification.id, exc)
            notification.retry_count += 1
            notification.last_error = str(exc)[:1000]
            if notification.retry_count >= 3:
                notification.status = DeliveryStatus.FAILED
            failed += 1
    return sent, failed
