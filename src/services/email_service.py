"""Minimal transactional email delivery used by security-sensitive flows."""

import asyncio
import logging
import smtplib
from email.message import EmailMessage

from src.config import get_settings

logger = logging.getLogger(__name__)


def _send_email_sync(recipient: str, subject: str, body: str) -> bool:
    settings = get_settings()
    if not settings.smtp_host or not settings.smtp_from_email or not recipient:
        return False
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from_email
    message["To"] = recipient
    message.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            if settings.smtp_username:
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
        return True
    except (OSError, smtplib.SMTPException):
        logger.exception("Transactional email delivery failed")
        return False


async def send_transactional_email(recipient: str, subject: str, body: str) -> bool:
    return await asyncio.to_thread(_send_email_sync, recipient, subject, body)


def _send_password_reset_email_sync(recipient: str, reset_url: str) -> bool:
    settings = get_settings()
    if not settings.smtp_host or not settings.smtp_from_email:
        return False

    message = EmailMessage()
    message["Subject"] = "Đặt lại mật khẩu Nera Home"
    message["From"] = settings.smtp_from_email
    message["To"] = recipient
    message.set_content(
        "Bạn đã yêu cầu đặt lại mật khẩu Nera Home.\n\n"
        f"Mở liên kết sau trong {settings.password_reset_expire_minutes} phút:\n{reset_url}\n\n"
        "Nếu bạn không yêu cầu thao tác này, hãy bỏ qua email."
    )

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            if settings.smtp_username:
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
        return True
    except (OSError, smtplib.SMTPException):
        logger.exception("Password reset email delivery failed")
        return False


async def send_password_reset_email(recipient: str, reset_url: str) -> bool:
    return await asyncio.to_thread(_send_password_reset_email_sync, recipient, reset_url)
