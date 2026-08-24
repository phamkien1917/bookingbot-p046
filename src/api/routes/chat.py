"""Chat transport endpoints.

The application currently uses the durable HTTP chat endpoint. The previous
WebSocket implementation returned scripted mock text, which was unsafe to expose
as a production AI path. Keep an explicit compatibility endpoint until real
streaming can share the same persistence transaction as POST /chat.
"""

import json

from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_text(json.dumps({
        "type": "error",
        "code": "STREAMING_NOT_AVAILABLE",
        "content": "Streaming chưa được bật. Vui lòng dùng API POST /api/v1/chat.",
    }, ensure_ascii=False))
    await websocket.close(code=1008, reason="Use the durable HTTP chat endpoint")
