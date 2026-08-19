from uuid import UUID

import asyncio
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import get_current_user
from src.database import get_session
from src.database.models import DeliveryStatus, Notification, User, UserStatus
from src.config import get_settings
from src.services.auth_service import ALGORITHM, SECRET_KEY
import jwt

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _serialize(notification: Notification) -> dict:
    return {
        "id": str(notification.id),
        "template_key": notification.template_key,
        "payload": notification.payload or {},
        "status": notification.status.value if hasattr(notification.status, "value") else notification.status,
        "created_at": notification.created_at,
    }


@router.get("")
async def list_notifications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await db.scalars(
        select(Notification)
        .where(Notification.user_id == user.id, Notification.scheduled_at <= func.now())
        .order_by(Notification.created_at.desc())
        .limit(30)
    )
    items = result.all()
    return {
        "items": [_serialize(item) for item in items],
        "unread": sum(1 for item in items if item.status == DeliveryStatus.PENDING),
    }


@router.post("/{notification_id}/read", status_code=204)
async def mark_notification_read(
    notification_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        update(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user.id)
        .values(status=DeliveryStatus.DELIVERED)
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    await db.commit()

@router.websocket("/ws")
async def websocket_notifications(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_session)
):
    await websocket.accept()
    settings = get_settings()
    
    token = websocket.cookies.get(settings.auth_cookie_name)
    if not token:
        token = websocket.query_params.get("token")
        
    if not token:
        await websocket.close(code=1008)
        return
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=1008)
            return
            
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or user.status != UserStatus.ACTIVE:
            await websocket.close(code=1008)
            return
    except jwt.PyJWTError:
        await websocket.close(code=1008)
        return
        
    from src.services.redis_service import get_event_pubsub
    pubsub = get_event_pubsub()
    channel = f"notifications:{user.id}"
    
    async def listen_to_redis():
        async for event in pubsub.subscribe(channel):
            try:
                await websocket.send_json(event)
            except Exception:
                break
                
    task = asyncio.create_task(listen_to_redis())
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        task.cancel()
