"""API routes for BookingBot AI Agent."""

import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.graph import get_agent_graph
from src.agents.state import create_initial_state
from src.api.routes.auth import get_current_user, get_optional_current_user
from src.database import get_session
from src.database.models import Property, User, UserRole
from src.models.schemas import ChatRequest, ChatResponse
from src.services.conversation_service import (
    delete_persistent_session,
    get_persistent_session,
    list_persistent_sessions,
    rename_persistent_session,
    save_persistent_session,
)
from src.services.customer_memory_service import (
    get_customer_memory,
    memory_summary,
    remember_feedback,
    remember_search_criteria,
)
from src.services.memory import get_short_term_memory
from src.services.search_criteria_service import build_search_criteria

from .admin import router as admin_router
from .auth import router as auth_router
from .bookings import router as bookings_router
from .chat import router as chat_router
from .favorites import router as favorites_router
from .memory import router as memory_router
from .notifications import router as notifications_router
from .properties import router as properties_router
from .sale import router as sale_router

router = APIRouter()
logger = logging.getLogger(__name__)


class RenameSessionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)

router.include_router(auth_router)
router.include_router(properties_router)
router.include_router(favorites_router)
router.include_router(memory_router)
router.include_router(bookings_router)
router.include_router(chat_router)
router.include_router(sale_router)
router.include_router(admin_router)
router.include_router(notifications_router)

def get_session_id(x_session_id: str | None = Header(None)) -> str:
    """Get or create session ID from header."""
    if x_session_id:
        return x_session_id
    return str(uuid.uuid4())


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session_id: str = Depends(get_session_id),
    user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_session),
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
        customer_id = str(user.id) if user and user.role == UserRole.CUSTOMER else None
        if not session_data and customer_id:
            session_data = await get_persistent_session(db, session_id, customer_id)
            if session_data:
                await memory.save_session(
                    session_id,
                    session_data.get("messages", []),
                    session_data.get("metadata", {}),
                )
        if session_data:
            owner_id = session_data.get("metadata", {}).get("customer_id")
            if owner_id and str(owner_id) != str(customer_id):
                raise HTTPException(status_code=403, detail="Session does not belong to this user")

        # Load durable preferences before invoking the agent. Redis is only a
        # speed layer; PostgreSQL remains the source of truth for memory.
        customer_memory = await get_customer_memory(db, customer_id) if customer_id else {}

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
            customer_id=customer_id,
        )
        # The graph appends to its message list; keep the API-owned list separate
        # so the assistant reply is persisted exactly once.
        state["messages"] = [*messages]
        state["preferences"] = [
            {"key": key, "value": value}
            for key, value in customer_memory.items()
        ]
        state["search_criteria"] = build_search_criteria(request.message, customer_memory)
        if user:
            state["customer_profile"] = {
                "full_name": user.full_name,
                "memory_summary": memory_summary(customer_memory),
            }

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

        # Get previous metadata and insights
        metadata = session_data.get("metadata", {}) if session_data else {}
        if customer_id:
            metadata["customer_id"] = customer_id
        metadata["last_active"] = datetime.now(UTC).isoformat()
        insights = metadata.get("insights", {})

        # Merge new insights from search_criteria
        search_criteria_res = result.get("search_criteria")
        if isinstance(search_criteria_res, dict):
            # Only update non-None values
            for k, v in search_criteria_res.items():
                if v is not None:
                    insights[k] = v

        if customer_id:
            await remember_search_criteria(db, customer_id, search_criteria_res if isinstance(search_criteria_res, dict) else None)
            await remember_feedback(db, customer_id, request.message)

        # Attach properties if any
        properties = result.get("selected_properties") or []
        # Agent tools deliberately hide internal identifiers from the LLM. Enrich
        # the final trusted API response so UI actions can open/book a property.
        titles = [item.get("title") for item in properties if isinstance(item, dict) and item.get("title")]
        if titles:
            property_rows = (await db.execute(
                select(Property.id, Property.title).where(Property.title.in_(titles))
            )).all()
            ids_by_title = {title: str(property_id) for property_id, title in property_rows}
            properties = [
                {**item, "id": ids_by_title[item["title"]]}
                if isinstance(item, dict) and item.get("title") in ids_by_title else item
                for item in properties
            ]
        messages.append({
            "role": "assistant",
            "content": response_msg,
            "properties": properties
        })

        # Save merged insights into metadata
        metadata["insights"] = insights

        if customer_id:
            await save_persistent_session(db, session_id, customer_id, messages, metadata)
        try:
            await memory.save_session(
                session_id=session_id,
                messages=messages,
                metadata=metadata,
            )
        except Exception as exc:
            logger.warning("Chat cache unavailable; history remains in PostgreSQL: %s", exc)

        return ChatResponse(
            response=response_msg,
            analysis="",
            session_id=session_id,
            properties=properties,
            insights=insights,
            memory_summary=memory_summary(await get_customer_memory(db, customer_id)) if customer_id else "",
        )

    except HTTPException:
        raise
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
async def get_chat_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get session data.

    Args:
        session_id: Session identifier

    Returns:
        Session data including messages
    """
    memory = get_short_term_memory()
    session_data = await memory.get_session(session_id)
    if not session_data:
        session_data = await get_persistent_session(db, session_id, str(user.id))

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    if str(session_data.get("metadata", {}).get("customer_id")) != str(user.id):
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "messages": session_data.get("messages", []),
        "metadata": session_data.get("metadata", {}),
    }

@router.get("/sessions")
async def get_all_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get all chat sessions.

    Args:
        customer_id: Optional customer UUID
    """
    return {"sessions": await list_persistent_sessions(db, str(user.id))}



@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Delete session data.

    Args:
        session_id: Session identifier

    Returns:
        Deletion confirmation
    """
    memory = get_short_term_memory()
    session_data = await memory.get_session(session_id)
    persistent = await get_persistent_session(db, session_id, str(user.id))
    if not persistent and (
        not session_data
        or str(session_data.get("metadata", {}).get("customer_id")) != str(user.id)
    ):
        raise HTTPException(status_code=404, detail="Session not found")
    await delete_persistent_session(db, session_id, str(user.id))
    try:
        await memory.delete_session(session_id)
    except Exception:
        pass
    return {"success": True, "session_id": session_id}


@router.patch("/session/{session_id}")
async def rename_session(
    session_id: str,
    payload: RenameSessionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Rename one conversation owned by the current user."""
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Tên cuộc trò chuyện không được để trống")
    metadata = await rename_persistent_session(db, session_id, str(user.id), title)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Session not found")

    memory = get_short_term_memory()
    try:
        session_data = await memory.get_session(session_id)
        if session_data and str(session_data.get("metadata", {}).get("customer_id")) == str(user.id):
            cache_metadata = {**session_data.get("metadata", {}), "title": title}
            await memory.save_session(session_id, session_data.get("messages", []), cache_metadata)
    except Exception:
        pass
    return {"success": True, "session_id": session_id, "title": title}
