import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        # Gửi thông điệp mở đầu
        await websocket.send_text(json.dumps({
            "role": "ASSISTANT",
            "content": "Chào bạn, tôi là AI Assistant của XHome. Bạn đang tìm mua nhà ở khu vực nào ạ?",
            "type": "text"
        }))

        while True:
            # Nhận tin nhắn từ client
            data = await websocket.receive_text()
            json.loads(data)

            # Logic gọi AI model (Mock)
            # Ở đây bạn sẽ đưa nội dung `user_msg['content']` vào LangGraph/CrewAI

            # Giả lập luồng gõ từng chữ (Streaming)
            response_text = "Tôi hiểu rồi. Đợi tôi kiểm tra giỏ hàng nhé..."
            for word in response_text.split(" "):
                await websocket.send_text(json.dumps({
                    "role": "ASSISTANT",
                    "content": word + " ",
                    "type": "stream"
                }))
                await asyncio.sleep(0.1) # Simulate network delay

            # Gửi tín hiệu kết thúc luồng chat
            await websocket.send_text(json.dumps({
                "type": "stream_end"
            }))

    except WebSocketDisconnect:
        print("Client disconnected")
