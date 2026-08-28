"""API routes for BookingBot AI Agent."""

import asyncio
import json
import logging
import re
import uuid
from collections.abc import AsyncIterator, Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents import create_initial_agent_state, run_agent
from src.api.routes.auth import get_current_user, get_optional_current_user
from src.database import get_session
from src.database.models import User, UserRole
from src.models.schemas import ChatRequest, ChatResponse
from src.services.analytics_service import record_event
from src.services.chat_state_service import normalize_text
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
    remember_time_preferences,
)
from src.services.memory import get_short_term_memory
from src.utils.time import utcnow

from .admin import router as admin_router
from .auth import router as auth_router
from .bookings import router as bookings_router
from .chat import router as chat_router
from .favorites import router as favorites_router
from .google_oauth import router as google_oauth_router
from .memory import router as memory_router
from .notifications import router as notifications_router
from .properties import router as properties_router
from .sale import router as sale_router

router = APIRouter()
logger = logging.getLogger(__name__)


class RenameSessionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)


_PROPERTY_RELEVANT_KINDS = {
    "SEARCH_RESULTS", "PROPERTY_SELECTED", "PROPERTY_ADVICE",
    "PROPERTY_LIST", "COMPARISON",
}
_PROPERTY_RELEVANT_INTENTS = {
    "SEARCH_PROPERTY", "SELECT_PROPERTY", "PROPERTY_DETAILS",
    "COMPARE_PROPERTIES", "BOOK_APPOINTMENT",
}

router.include_router(auth_router)
router.include_router(properties_router)
router.include_router(favorites_router)
router.include_router(memory_router)
router.include_router(bookings_router)
router.include_router(chat_router)
router.include_router(sale_router)
router.include_router(admin_router)
router.include_router(notifications_router)
router.include_router(google_oauth_router)

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
    """Chat through the LangGraph Multi-Agent System."""
    return await _execute_chat_turn(request, session_id, user, db)


async def _execute_chat_turn(
    request: ChatRequest,
    session_id: str,
    user: User | None,
    db: AsyncSession,
    on_stage: Callable[[str], None] | None = None,
) -> ChatResponse:
    """Run one chat turn end to end.

    Both the plain POST and the streaming endpoint go through here, so there is a
    single persistence path: whichever transport a client uses, the session is
    written exactly once and in the same way.

    `on_stage` receives each graph node name as it finishes. It only reports
    progress; it must not change what the turn produces.
    """
    try:
        session_id = request.session_id or session_id
        try:
            UUID(session_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Session ID không hợp lệ") from exc

        memory = get_short_term_memory()
        session_data = await memory.get_session(session_id)
        customer_uuid = user.id if user and user.role == UserRole.CUSTOMER else None
        customer_id = str(customer_uuid) if customer_uuid else None

        from src.config import get_settings
        from src.services.redis_service import get_rate_limiter

        settings = get_settings()
        rate_limiter = get_rate_limiter()
        allowed = await rate_limiter.is_allowed(
            f"chat:{customer_id or session_id}",
            settings.rate_limit_requests,
            settings.rate_limit_window
        )
        if not allowed:
            raise HTTPException(status_code=429, detail="Bạn gửi tin nhắn quá nhanh. Vui lòng thử lại sau ít phút.")

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

        customer_memory = await get_customer_memory(db, customer_id) if customer_id else {}
        current_mem_summary = memory_summary(customer_memory) if customer_memory else ""
        messages = list(session_data.get("messages", [])) if session_data else []
        metadata = session_data.get("metadata", {}) if session_data else {}
        if customer_id:
            metadata["customer_id"] = customer_id
        metadata["last_active"] = utcnow().isoformat()

        # Create AgentState for LangGraph with memory summary for context / suggestions
        agent_state = create_initial_agent_state(
            session_id=session_id,
            query=request.message,
            customer_id=customer_id,
            customer_role=user.role if user else None,
            history=messages,
            metadata=metadata,
            memory_summary=current_mem_summary,
        )

        # Only merge customer memory into active search_criteria if user explicitly asks to resume
        norm_query = normalize_text(request.message)
        resume_signal = bool(re.search(
            r"\b(nhu cau cu|so thich da luu|tiep tuc tim|nhu lan truoc|nhu cu|tim lai|theo tieu chi cu|tiep tuc hanh trinh|tiep tuc tim kiem)\b",
            norm_query
        ))
        if resume_signal:
            agent_state["is_resume_search"] = True
            if not agent_state.get("search_criteria") and customer_memory:
                agent_state["search_criteria"] = {
                    key: value
                    for key, value in customer_memory.items()
                    if key in {
                        "region", "district", "province", "property_kind", "min_price", "max_price",
                        "min_bedrooms", "max_bedrooms", "exact_bedrooms", "min_bathrooms", "min_area", "area_or_ward", "ward",
                        "transaction_type", "orientation", "legal_status", "furniture_status", "min_floor", "max_floor",
                    }
                }

        if request.property_id:
            agent_state["current_property_id"] = str(request.property_id)
        if request.user_latitude is not None and request.user_longitude is not None:
            agent_state["user_location"] = {
                "latitude": request.user_latitude,
                "longitude": request.user_longitude,
            }
            agent_state["commute_landmark"] = "Vị trí của bạn"

        # Execute LangGraph Multi-Agent
        final_state = await run_agent(agent_state, on_stage=on_stage)

        response_msg = str(final_state.get("response") or "").strip()
        if not response_msg:
            response_msg = "Chào bạn! Mình có thể giúp bạn tìm nhà, xem chi tiết và đặt lịch xem nhà. Bạn cần hỗ trợ gì?"

        raw_properties = final_state.get("selected_properties") or []
        response_kind = final_state.get("response_kind", "DIRECT")
        intent = final_state.get("intent")
        # Strict relevancy check: only attach property cards when turn is genuinely about searching/viewing properties
        if response_kind in _PROPERTY_RELEVANT_KINDS or (intent in _PROPERTY_RELEVANT_INTENTS and response_kind not in ("DIRECT", "ASK_CRITERIA", "SEARCH_NO_RESULTS")):
            properties = raw_properties
        else:
            properties = []

        insights = final_state.get("insights") or {}
        ai_mode = final_state.get("ai_mode") or "llm_grounded"
        ai_model = final_state.get("ai_model")
        ai_latency_ms = int(final_state.get("ai_latency_ms") or 0)
        auth_required = bool(final_state.get("auth_required"))

        # Save metadata and update state
        stored_chat_state = {
            "criteria": final_state.get("search_criteria", {}),
            "soft_preferences": final_state.get("soft_preferences", []),
            "household_context": final_state.get("household_context", []),
            "commute_landmark": (
                None if final_state.get("commute_landmark") == "Vị trí của bạn"
                else final_state.get("commute_landmark")
            ),
            "max_commute_minutes": final_state.get("max_commute_minutes"),
            "max_commute_km": final_state.get("max_commute_km"),
            "travel_mode": final_state.get("travel_mode", "DRIVE"),
            "nearby_categories": final_state.get("nearby_categories", []),
            "monthly_income_vnd": final_state.get("monthly_income_vnd"),
            "own_capital_vnd": final_state.get("own_capital_vnd"),
            "property_refs": raw_properties if properties else (metadata.get("chat_state", {}).get("property_refs", []) if intent in _PROPERTY_RELEVANT_INTENTS else []),
            "search_result_refs": final_state.get("search_results") or metadata.get("chat_state", {}).get("search_result_refs", []),
            "selected_property_id": final_state.get("current_property_id"),
            "selected_property_index": final_state.get("selected_property_index"),
            "requested_date": final_state.get("requested_date"),
            "requested_hour": final_state.get("requested_hour"),
            "slots": final_state.get("selected_slots", []),
            "selected_slot_index": final_state.get("selected_slot_index"),
            "active_request_id": final_state.get("active_request_id"),
            "active_request_code": final_state.get("active_request_code"),
            "pending_action": final_state.get("pending_action"),
            "phase": final_state.get("phase", "IDLE"),
        }
        if settings.app_env != "production" and final_state.get("error"):
            stored_chat_state["debug_error"] = str(final_state["error"])
        metadata["chat_state"] = stored_chat_state
        metadata["insights"] = insights

        # Append messages
        messages.append({"role": "user", "content": request.message})
        messages.append({
            "role": "assistant",
            "content": response_msg,
            "properties": properties,
            "ai_mode": ai_mode,
            "ai_model": ai_model,
        })

        if customer_id:
            if intent == "SEARCH_PROPERTY":
                record_event(
                    db,
                    "property_search",
                    customer_user_id=customer_uuid,
                    session_id=session_id,
                    properties={"criteria": final_state.get("search_criteria") or {}},
                )
            if intent == "SEARCH_PROPERTY" and final_state.get("search_criteria"):
                await remember_search_criteria(db, customer_id, final_state.get("search_criteria"))
            await remember_feedback(db, customer_id, request.message)
            await remember_time_preferences(db, customer_id, request.message)
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
            suggested_actions=final_state.get("suggested_actions") or [],
            metadata=stored_chat_state,
            memory_summary=memory_summary(await get_customer_memory(db, customer_id)) if customer_id else "",
            auth_required=auth_required,
            ai_mode=ai_mode,
            ai_model=ai_model,
            ai_latency_ms=ai_latency_ms,
            ai_fallback_reason="provider_unavailable" if ai_mode == "fallback" else None,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Chat request failed for session %s", session_id)
        raise HTTPException(
            status_code=503,
            detail="Trợ lý đang gặp sự cố tạm thời. Vui lòng thử lại sau ít phút.",
        ) from exc


# Upper bound on waiting for a turn to finish after the client has gone. Two LLM
# calls at ~20s each plus persistence fits comfortably inside this.
_STREAM_DRAIN_TIMEOUT = 60

# What each graph node is actually doing, in the customer's words. Only nodes
# that take visible time are listed; anything unmapped is skipped rather than
# reported under a vague label.
_STAGE_LABELS = {
    "supervisor": "Đang đọc nhu cầu của bạn",
    "inventory": "Đang tìm trong kho nhà",
    "booking": "Đang kiểm tra khung giờ trống",
    "assignment": "Đang tìm nhân viên phụ trách",
    "hitl": "Đang chuyển cho nhân viên xác nhận",
    "respond": "Đang viết câu trả lời",
}


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    session_id: str = Depends(get_session_id),
    user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_session),
) -> StreamingResponse:
    """Same turn as POST /chat, with real progress reported while it runs.

    Each `stage` event fires when a graph node genuinely finishes. Nothing here is
    simulated: if the work is fast, the client simply sees fewer stages.
    """
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    async def run() -> ChatResponse:
        try:
            return await _execute_chat_turn(
                request, session_id, user, db, on_stage=queue.put_nowait
            )
        finally:
            queue.put_nowait(None)

    async def events() -> AsyncIterator[str]:
        task = asyncio.create_task(run())
        try:
            while True:
                node = await queue.get()
                if node is None:
                    break
                label = _STAGE_LABELS.get(node)
                if label:
                    payload = json.dumps({"stage": node, "label": label}, ensure_ascii=False)
                    yield f"event: stage\ndata: {payload}\n\n"

            result = await task
            body = result.model_dump(mode="json")
            yield f"event: result\ndata: {json.dumps(body, ensure_ascii=False)}\n\n"
        except HTTPException as exc:
            error = json.dumps({"detail": exc.detail, "status": exc.status_code}, ensure_ascii=False)
            yield f"event: error\ndata: {error}\n\n"
        except Exception:
            logger.exception("Chat stream failed for session %s", session_id)
            error = json.dumps(
                {"detail": "Trợ lý đang gặp sự cố tạm thời. Vui lòng thử lại sau ít phút.", "status": 503},
                ensure_ascii=False,
            )
            yield f"event: error\ndata: {error}\n\n"
        finally:
            # The turn is never cancelled: it holds the request-scoped DB session,
            # and cutting it off mid-write would persist half a turn. If the client
            # disconnected, wait here so FastAPI does not tear that session down
            # underneath the task. The shield keeps the timeout from cancelling it.
            if not task.done():
                try:
                    await asyncio.wait_for(asyncio.shield(task), timeout=_STREAM_DRAIN_TIMEOUT)
                except (TimeoutError, HTTPException):
                    logger.warning("Chat turn still running after client left: %s", session_id)
                except Exception:
                    logger.exception("Chat turn failed after client left: %s", session_id)

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",  # keep proxies from holding the stages back
            "Connection": "keep-alive",
        },
    )


@router.get("/status")
async def agent_status():
    """Report the production chat path currently serving requests."""
    from src.config import get_settings
    from src.services.geo_service import get_geo_service

    settings = get_settings()
    return {
        "status": "ready",
        "chat_engine": "langgraph-multi-agent-v2",
        "active_agents": ["supervisor", "inventory", "booking", "hitl", "respond"],
        "llm_configured": bool(settings.openrouter_api_key or settings.openai_api_key),
        "geo_configured": get_geo_service().configured,
        "booking_source": "booking-domain-service",
    }


@router.get("/status/geo")
async def geo_provider_status():
    """Run real Google Maps capability probes in non-production environments."""
    from src.config import get_settings
    from src.services.geo_service import get_geo_service

    if get_settings().app_env == "production":
        raise HTTPException(status_code=404, detail="Not found")
    return await get_geo_service().diagnose_capabilities()


@router.get("/session/{session_id}")
async def get_chat_session(
    session_id: str,
    user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get session data.

    Args:
        session_id: Session identifier

    Returns:
        Session data including messages
    """
    user_id_str = str(user.id) if user else None
    session_data = None
    if user_id_str:
        session_data = await get_persistent_session(db, session_id, user_id_str)
    if not session_data:
        memory = get_short_term_memory()
        session_data = await memory.get_session(session_id)
        if session_data:
            meta_customer_id = session_data.get("metadata", {}).get("customer_id")
            if meta_customer_id and user_id_str and str(meta_customer_id) != user_id_str:
                raise HTTPException(status_code=404, detail="Session not found")

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    metadata = session_data.get("metadata", {})
    if user_id_str:
        metadata["customer_id"] = user_id_str

    return {
        "session_id": session_id,
        "messages": session_data.get("messages", []),
        "metadata": metadata,
    }


@router.get("/sessions")
async def get_all_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get all chat sessions."""
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
