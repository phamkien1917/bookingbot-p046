from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.services.hitl_service import create_hitl_case, resolve_hitl_case


@pytest.mark.asyncio
async def test_hitl_case_is_durable_and_resolvable() -> None:
    customer_id = uuid4()
    coordinator_id = uuid4()
    db = MagicMock()
    db.flush = AsyncMock()
    reviewer_result = MagicMock()
    reviewer_result.scalars.return_value.all.return_value = [coordinator_id]
    db.execute = AsyncMock(return_value=reviewer_result)

    case = await create_hitl_case(
        db,
        reason="NO_SALE_AVAILABLE",
        context={"property_id": str(uuid4())},
        session_id=str(uuid4()),
        customer_user_id=customer_id,
    )
    db.get = AsyncMock(return_value=case)
    resolved = await resolve_hitl_case(
        db,
        case.id,
        coordinator_id,
        action="OVERRIDE",
        message="Đã phân sale thủ công",
    )

    assert resolved.status == "RESOLVED"
    assert resolved.resolved_by_user_id == coordinator_id
    assert resolved.decision["action"] == "OVERRIDE"
    assert resolved.decision["message"] == "Đã phân sale thủ công"
