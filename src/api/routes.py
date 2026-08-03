"""API routes for BookingBot AI Agent."""

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Depends

from src.agents.state import create_initial_state
from src.agents.graph import get_agent_graph
from src.models.schemas import ChatRequest, ChatResponse
from src.services.memory import get_short_term_memory

router = APIRouter()


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
        response_msg = result.get("response", "")
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
