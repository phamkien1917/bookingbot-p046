"""Persistent chat history backed by PostgreSQL."""

import json
from src.utils.time import utcnow
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Conversation, Message, MessageRole


def _as_uuid(value: str) -> UUID | None:
    try:
        return UUID(value)
    except (TypeError, ValueError):
        return None


def _metadata(summary: str | None) -> dict:
    if not summary:
        return {}
    try:
        value = json.loads(summary)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def _message_dict(message: Message) -> dict:
    return {
        "role": message.role.value.lower(),
        "content": message.content_redacted or "",
        **(message.structured_payload or {}),
    }


async def get_persistent_session(db: AsyncSession, session_id: str, customer_id: str) -> dict | None:
    conversation_id, customer_uuid = _as_uuid(session_id), _as_uuid(customer_id)
    if not conversation_id or not customer_uuid:
        return None
    row = await db.scalar(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conversation_id, Conversation.customer_user_id == customer_uuid)
    )
    if not row:
        return None
    meta = _metadata(row.summary)
    meta["customer_id"] = str(row.customer_user_id)
    return {
        "messages": [_message_dict(message) for message in row.messages],
        "metadata": meta,
    }


async def save_persistent_session(
    db: AsyncSession,
    session_id: str,
    customer_id: str,
    messages: list[dict],
    metadata: dict | None = None,
) -> None:
    conversation_id, customer_uuid = _as_uuid(session_id), _as_uuid(customer_id)
    if not conversation_id or not customer_uuid:
        return
    row = await db.get(Conversation, conversation_id)
    if row and row.customer_user_id != customer_uuid:
        raise PermissionError("Session does not belong to this user")
    if not row:
        row = Conversation(id=conversation_id, customer_user_id=customer_uuid, status="OPEN")
        db.add(row)
        await db.flush()
    row.summary = json.dumps(metadata or {}, ensure_ascii=False, default=str)
    row.updated_at = utcnow()
    await db.execute(delete(Message).where(Message.conversation_id == conversation_id))

    role_map = {
        "user": MessageRole.USER,
        "assistant": MessageRole.ASSISTANT,
        "bot": MessageRole.ASSISTANT,
        "tool": MessageRole.TOOL,
        "system": MessageRole.SYSTEM,
    }
    for item in messages:
        payload = {key: value for key, value in item.items() if key not in {"role", "content", "text"}}
        db.add(Message(
            conversation_id=conversation_id,
            role=role_map.get(str(item.get("role", "assistant")).lower(), MessageRole.ASSISTANT),
            content_redacted=str(item.get("content") or item.get("text") or ""),
            structured_payload=payload,
        ))
    await db.flush()


async def list_persistent_sessions(db: AsyncSession, customer_id: str) -> list[dict]:
    customer_uuid = _as_uuid(customer_id)
    if not customer_uuid:
        return []
    rows = (await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.customer_user_id == customer_uuid)
        .order_by(Conversation.updated_at.desc())
    )).scalars().all()
    sessions = []
    for row in rows:
        messages = [_message_dict(message) for message in row.messages]
        metadata = _metadata(row.summary)
        first_user = next((item["content"] for item in messages if item["role"] == "user"), "Cuộc trò chuyện mới")
        custom_title = str(metadata.get("title") or "").strip()
        title = custom_title or first_user[:50] + ("..." if len(first_user) > 50 else "")
        sessions.append({
            "session_id": str(row.id),
            "preview": title,
            "title": title,
            "message_count": len(messages),
            "last_active": row.updated_at.isoformat() if row.updated_at else "",
        })
    return sessions


async def delete_persistent_session(db: AsyncSession, session_id: str, customer_id: str) -> bool:
    conversation_id, customer_uuid = _as_uuid(session_id), _as_uuid(customer_id)
    if not conversation_id or not customer_uuid:
        return False
    result = await db.execute(delete(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.customer_user_id == customer_uuid,
    ))
    await db.flush()
    return bool(result.rowcount)


async def rename_persistent_session(
    db: AsyncSession,
    session_id: str,
    customer_id: str,
    title: str,
) -> dict | None:
    """Rename a conversation while preserving its existing metadata."""
    conversation_id, customer_uuid = _as_uuid(session_id), _as_uuid(customer_id)
    if not conversation_id or not customer_uuid:
        return None
    row = await db.scalar(select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.customer_user_id == customer_uuid,
    ))
    if not row:
        return None
    metadata = _metadata(row.summary)
    metadata["title"] = title.strip()
    row.summary = json.dumps(metadata, ensure_ascii=False, default=str)
    row.updated_at = utcnow()
    await db.flush()
    return metadata
