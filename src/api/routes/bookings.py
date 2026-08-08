from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.database import get_session
from src.schemas.booking import TourRequestCreate, TourRequestResponse
from src.services.booking_service import create_tour_request, get_my_tour_requests, execute_soft_hold
from src.api.routes.auth import get_current_user_id

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=TourRequestResponse)
async def create_booking(
    request_data: TourRequestCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_session)
):
    """Tạo yêu cầu đặt lịch xem nhà (Dành cho Khách hàng đã đăng nhập)."""
    try:
        booking = await create_tour_request(db, UUID(user_id), request_data)
        return booking
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my")
async def get_my_bookings(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_session)
):
    """Lấy danh sách các lịch xem nhà của tôi."""
    bookings = await get_my_tour_requests(db, UUID(user_id))
    return bookings


@router.post("/test-hold")
async def test_soft_hold(
    appointment_id: UUID,
    hold_minutes: int = 15,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_session)
):
    """
    API dùng để test tính năng Giữ chỗ (Row-level Lock).
    Mô phỏng Sale ấn duyệt lịch và kích hoạt Giữ chỗ (Soft Hold).
    """
    try:
        row = await execute_soft_hold(
            db,
            appointment_id=appointment_id,
            approved_by_user_id=UUID(user_id),
            hold_minutes=hold_minutes
        )
        return {"message": "Giữ chỗ thành công!", "hold_data": dict(row._mapping)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
