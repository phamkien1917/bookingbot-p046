"""API routes for BookingBot AI Agent."""

import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse

from src.agents.state import create_initial_state
from src.agents.graph import get_agent_graph
from src.models.schemas import ChatRequest, ChatResponse
from src.services.memory import get_short_term_memory

router = APIRouter()

from .properties import router as properties_router
from .chat import router as chat_router
from .auth import router as auth_router
from .bookings import router as bookings_router

router.include_router(auth_router)
router.include_router(properties_router)
router.include_router(bookings_router)
router.include_router(chat_router)

def get_session_id(x_session_id: Optional[str] = Header(None)) -> str:
    """Get or create session ID from header."""
    if x_session_id:
        return x_session_id
    return str(uuid.uuid4())


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session_id: str = Depends(get_session_id),
) -> ChatResponse:
    """Chat với AI agent.

    Args:
        request: Chat request with message
        session_id: Optional session ID for conversation continuity

    Returns:
        Chat response with agent reply
    """
    try:
        # Get short-term memory for session context
        memory = get_short_term_memory()
        session_data = await memory.get_session(session_id)

        # Create initial state
        messages = []
        if session_data:
            messages = session_data.get("messages", [])

        # Add current message
        messages.append({"role": "user", "content": request.message})

        # Create state
        state = create_initial_state(
            session_id=session_id,
            query=request.message,
            customer_id=session_data.get("metadata", {}).get("customer_id") if session_data else None,
        )
        state["messages"] = messages

        # Run agent
        graph = get_agent_graph()
        result = await graph.ainvoke(state)

        # Save session
        response_msg = result.get("response", "").strip()
        if not response_msg:
            next_action = result.get("next_action")
            if next_action == "greet":
                response_msg = "Xin chào! Tôi là BookingBot. Tôi có thể giúp bạn tìm bất động sản, đặt lịch xem nhà hoặc kiểm tra booking."
            elif next_action == "clarify":
                response_msg = "Xin lỗi, tôi chưa hiểu rõ ý bạn. Bạn có thể mô tả lại yêu cầu hoặc hỏi về dịch vụ của chúng tôi."
            elif next_action == "check_booking_status":
                response_msg = "Để kiểm tra trạng thái booking, vui lòng cung cấp mã booking hoặc số điện thoại đã đăng ký."
            else:
                response_msg = "Xin chào! Tôi đang ở chế độ thử nghiệm. Nếu bạn đã thêm API key nhưng vẫn không nhận được phản hồi, hãy kiểm tra log backend để xác nhận model đang được gọi."

        messages.append({"role": "assistant", "content": response_msg})

        await memory.save_session(
            session_id=session_id,
            messages=messages,
            metadata=session_data.get("metadata", {}) if session_data else {},
        )

        return ChatResponse(
            response=response_msg,
            analysis=result.get("analysis", ""),
            session_id=session_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ui", response_class=HTMLResponse)
async def serve_ui() -> HTMLResponse:
    """Serve the mock test UI for manual interaction."""
    ui_path = Path(__file__).resolve().parents[1] / "MOCKUI" / "test_ui" / "index.html"
    return HTMLResponse(content=ui_path.read_text(encoding="utf-8"), status_code=200)


@router.get("/status")
async def agent_status():
    """Kiểm tra trạng thái agent."""
    return {
        "status": "ready",
        "agent": "BookingBot Multi-Agent v1.0",
        "model": "OpenRouter (free tier + fallback)",
    }


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session data.

    Args:
        session_id: Session identifier

    Returns:
        Session data including messages
    """
    memory = get_short_term_memory()
    session_data = await memory.get_session(session_id)

    if not session_data:
        return {"error": "Session not found", "session_id": session_id}

    return {
        "session_id": session_id,
        "messages": session_data.get("messages", []),
        "metadata": session_data.get("metadata", {}),
    }


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete session data.

    Args:
        session_id: Session identifier

    Returns:
        Deletion confirmation
    """
    memory = get_short_term_memory()
    await memory.delete_session(session_id)
    return {"success": True, "session_id": session_id}
