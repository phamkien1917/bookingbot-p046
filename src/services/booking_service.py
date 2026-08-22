import uuid
from datetime import date, datetime, time, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import (
    Appointment,
    AppointmentStatus,
    Conversation,
    CustomerProfile,
    DeliveryStatus,
    Message,
    MessageRole,
    Notification,
    NotificationChannel,
    Property,
    PropertySaleAssignment,
    PropertyStatus,
    RequestStatus,
    SaleProfile,
    SlotStatus,
    TourRequest,
    TourSlotOption,
    User,
    UserRole,
    UserStatus,
)
from src.exceptions import BookingConflictError, BookingNotFoundError, BookingPermissionError
from src.schemas.booking import BookingResponse, TourRequestCreate
from src.utils.time import utcnow

LOCAL_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
SLOT_HOURS = (9, 10, 14, 16)
REQUEST_HOLD_MINUTES = 15


def _enum_value(value):
    return value.value if hasattr(value, "value") else value


def serialize_booking(row: TourRequest) -> BookingResponse:
    prop = row.property
    appointment = row.appointment
    selected_slot = next(
        (slot for slot in row.slot_options if _enum_value(slot.status) == "SELECTED"),
        row.slot_options[0] if row.slot_options else None,
    )
    sale_profile = appointment.sale if appointment else (selected_slot.sale if selected_slot else None)
    sale_user = sale_profile.user if sale_profile else None
    media = []
    if prop and prop.media:
        media = [
            {"url": item.url, "is_cover": item.is_cover, "caption": item.caption}
            for item in prop.media
        ]

    data = {
        "id": row.id,
        "request_code": row.request_code,
        "status": _enum_value(row.status),
        "tour_mode": _enum_value(row.tour_mode),
        "preferred_start": row.preferred_start,
        "preferred_end": row.preferred_end,
        "party_size": row.party_size,
        "customer_note": row.customer_note,
        "created_at": row.created_at,
        "expires_at": row.expires_at,
        "property": {
            "id": prop.id,
            "title": prop.title,
            "address": ", ".join(filter(None, [prop.address_line, prop.ward, prop.district, prop.province])),
            "district": prop.district,
            "province": prop.province,
            "media": media,
        } if prop else None,
        "sale": {
            "id": sale_user.id,
            "full_name": sale_user.full_name,
            "phone": sale_user.phone,
            "email": sale_user.email,
            "job_title": sale_profile.job_title,
        } if sale_user else None,
        "appointment": {
            "id": appointment.id,
            "booking_code": appointment.booking_code,
            "status": _enum_value(appointment.status),
            "starts_at": appointment.starts_at,
            "ends_at": appointment.ends_at,
        } if appointment else None,
    }
    return BookingResponse.model_validate(data)


def _booking_load_options():
    return (
        selectinload(TourRequest.property).selectinload(Property.media),
        selectinload(TourRequest.appointment)
        .selectinload(Appointment.sale)
        .selectinload(SaleProfile.user),
        selectinload(TourRequest.slot_options)
        .selectinload(TourSlotOption.sale)
        .selectinload(SaleProfile.user),
    )


async def _get_booking(db: AsyncSession, booking_id: UUID) -> TourRequest | None:
    stmt = select(TourRequest).options(*_booking_load_options()).where(TourRequest.id == booking_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_available_slots(db: AsyncSession, property_id: UUID, target_date: date) -> dict:
    prop = await db.get(Property, property_id)
    if not prop or prop.status != PropertyStatus.AVAILABLE:
        raise BookingConflictError("Bất động sản không khả dụng")

    sales_result = await db.execute(
        select(SaleProfile)
        .join(User, User.id == SaleProfile.user_id)
        .join(PropertySaleAssignment, PropertySaleAssignment.sale_user_id == SaleProfile.user_id)
        .options(selectinload(SaleProfile.user))
        .where(
            SaleProfile.is_accepting_tours.is_(True),
            User.status == UserStatus.ACTIVE,
            PropertySaleAssignment.property_id == property_id
        )
        .order_by(SaleProfile.employee_code)
    )
    sales = sales_result.scalars().all()
    slots: list[dict] = []
    if not sales:
        return {"property_id": str(property_id), "date": target_date.isoformat(), "slots": slots}

    sale_ids = [sale.user_id for sale in sales]
    start_of_day = datetime.combine(target_date, time.min, tzinfo=LOCAL_TZ)
    end_of_day = datetime.combine(target_date, time.max, tzinfo=LOCAL_TZ)

    appointments = (await db.execute(
        select(Appointment.sale_user_id, Appointment.starts_at, Appointment.ends_at)
        .where(
            Appointment.sale_user_id.in_(sale_ids),
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
            Appointment.starts_at < end_of_day,
            Appointment.ends_at > start_of_day,
        )
    )).all()

    pending_options = (await db.execute(
        select(TourSlotOption.sale_user_id, TourSlotOption.starts_at, TourSlotOption.ends_at)
        .join(TourRequest, TourRequest.id == TourSlotOption.tour_request_id)
        .where(
            TourSlotOption.sale_user_id.in_(sale_ids),
            TourSlotOption.status == SlotStatus.SELECTED,
            TourRequest.status == RequestStatus.WAITING_APPROVAL,
            TourRequest.expires_at > func.now(),
            TourSlotOption.starts_at < end_of_day,
            TourSlotOption.ends_at > start_of_day,
        )
    )).all()

    now = datetime.now(LOCAL_TZ)
    for hour in SLOT_HOURS:
        start = datetime.combine(target_date, time(hour=hour), tzinfo=LOCAL_TZ)
        end = start + timedelta(hours=1)
        if start <= now + timedelta(hours=1):
            continue
        for sale in sales:
            conflict = any(
                uid == sale.user_id and a_start < end and a_end > start
                for uid, a_start, a_end in appointments
            )
            if conflict:
                continue
            pending_conflict = any(
                uid == sale.user_id and p_start < end and p_end > start
                for uid, p_start, p_end in pending_options
            )
            if not pending_conflict:
                slots.append({
                    "sale_user_id": str(sale.user_id),
                    "sale_name": sale.user.full_name,
                    "starts_at": start.isoformat(),
                    "ends_at": end.isoformat(),
                    "label": start.strftime("%H:%M"),
                })
                break
    return {"property_id": str(property_id), "date": target_date.isoformat(), "slots": slots}


async def create_tour_request(
    db: AsyncSession,
    customer_user_id: UUID,
    data: TourRequestCreate,
    conversation_id: UUID | None = None,
) -> TourRequest:
    prop = await db.get(Property, data.property_id)
    sale = await db.get(SaleProfile, data.sale_user_id)
    if not prop or prop.status != PropertyStatus.AVAILABLE:
        raise BookingConflictError("Bất động sản không khả dụng")
    if not sale or not sale.is_accepting_tours:
        raise BookingConflictError("Nhân viên tư vấn không còn khả dụng")
    if data.preferred_start <= utcnow().astimezone(data.preferred_start.tzinfo):
        raise BookingConflictError("Thời gian xem nhà phải ở tương lai")

    # Serialize competing requests for the exact Sale/time window. The conflict
    # checks and insert now happen inside the same PostgreSQL transaction.
    lock_key = f"tour:{data.sale_user_id}:{data.preferred_start.isoformat()}:{data.preferred_end.isoformat()}"
    await db.execute(text("SELECT pg_advisory_xact_lock(hashtext(:lock_key))"), {"lock_key": lock_key})

    conflict = await db.scalar(
        select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == data.sale_user_id,
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
            Appointment.starts_at < data.preferred_end,
            Appointment.ends_at > data.preferred_start,
        )
    )
    if conflict:
        raise BookingConflictError("Khung giờ vừa được người khác đặt, vui lòng chọn giờ khác")
    pending_conflict = await db.scalar(
        select(func.count(TourSlotOption.id))
        .join(TourRequest, TourRequest.id == TourSlotOption.tour_request_id)
        .where(
            TourSlotOption.sale_user_id == data.sale_user_id,
            TourSlotOption.status == SlotStatus.SELECTED,
            TourRequest.status == RequestStatus.WAITING_APPROVAL,
            TourRequest.expires_at > func.now(),
            TourSlotOption.starts_at < data.preferred_end,
            TourSlotOption.ends_at > data.preferred_start,
        )
    )
    if pending_conflict:
        raise BookingConflictError("Khung giờ đang được giữ cho một yêu cầu khác, vui lòng chọn giờ khác")

    expires_at = utcnow() + timedelta(minutes=REQUEST_HOLD_MINUTES)
    request = TourRequest(
        request_code=f"TR-{uuid.uuid4().hex[:12].upper()}",
        customer_user_id=customer_user_id,
        conversation_id=conversation_id,
        property_id=data.property_id,
        preferred_start=data.preferred_start,
        preferred_end=data.preferred_end,
        party_size=data.pax_count,
        customer_note=data.customer_note,
        status=RequestStatus.WAITING_APPROVAL,
        submitted_at=utcnow(),
        expires_at=expires_at,
    )
    db.add(request)
    await db.flush()
    db.add(TourSlotOption(
        tour_request_id=request.id,
        sale_user_id=data.sale_user_id,
        status=SlotStatus.SELECTED,
        starts_at=data.preferred_start,
        ends_at=data.preferred_end,
        valid_until=expires_at,
        selected_at=utcnow(),
        score=100,
        score_explanation={"source": "customer_selected"},
    ))
    notification_payload = {
        "request_code": request.request_code,
        "property_id": str(prop.id),
        "property_title": prop.title,
        "starts_at": data.preferred_start.isoformat(),
        "ends_at": data.preferred_end.isoformat(),
    }
    db.add(Notification(
        user_id=data.sale_user_id,
        channel=NotificationChannel.IN_APP,
        template_key="sale_reschedule_request" if data.is_reschedule else "sale_booking_request",
        payload=notification_payload,
        status=DeliveryStatus.PENDING,
    ))
    db.add(Notification(
        user_id=customer_user_id,
        channel=NotificationChannel.IN_APP,
        template_key="booking_request_received",
        payload=notification_payload,
        status=DeliveryStatus.PENDING,
    ))
    return await _get_booking(db, request.id)


async def get_my_tour_requests(db: AsyncSession, customer_user_id: UUID) -> list[dict]:
    result = await db.execute(
        select(TourRequest)
        .options(*_booking_load_options())
        .where(TourRequest.customer_user_id == customer_user_id)
        .order_by(TourRequest.created_at.desc())
    )
    return [serialize_booking(row) for row in result.scalars().all()]


async def get_customer_booking(db: AsyncSession, booking_id: UUID, customer_id: UUID) -> dict:
    row = await _get_booking(db, booking_id)
    if not row or row.customer_user_id != customer_id:
        raise BookingNotFoundError("Không tìm thấy lịch xem")
    if row.status == RequestStatus.WAITING_APPROVAL and row.expires_at:
        expires = row.expires_at
        now = utcnow().astimezone(expires.tzinfo)
        if expires <= now:
            row.status = RequestStatus.EXPIRED
            await db.commit()
    return serialize_booking(row)


async def cancel_customer_booking(db: AsyncSession, booking_id: UUID, customer_id: UUID, reason: str | None) -> dict:
    row = await _get_booking(db, booking_id)
    if not row or row.customer_user_id != customer_id:
        raise BookingNotFoundError("Không tìm thấy lịch xem")
    if row.status in (RequestStatus.CANCELLED, RequestStatus.EXPIRED, RequestStatus.REJECTED):
        return serialize_booking(row)
    # Notify the assigned Sale if any
    sale_user_id = None
    if row.appointment:
        sale_user_id = row.appointment.sale_user_id
    else:
        selected_slot = next((s for s in row.slot_options if s.status == SlotStatus.SELECTED), None)
        if selected_slot:
            sale_user_id = selected_slot.sale_user_id

    if sale_user_id:
        db.add(Notification(
            user_id=sale_user_id,
            channel=NotificationChannel.IN_APP,
            template_key="booking_cancelled_by_customer",
            payload={
                "request_code": row.request_code,
                "property_title": row.property.title if row.property else None,
                "reason": reason or "Khách hàng yêu cầu hủy",
            },
            status=DeliveryStatus.PENDING,
        ))

    row.status = RequestStatus.CANCELLED
    if row.appointment:
        row.appointment.status = AppointmentStatus.CANCELLED
        row.appointment.cancelled_at = utcnow()
        row.appointment.cancellation_reason = reason or "Khách hàng yêu cầu hủy"
    for slot in row.slot_options:
        slot.status = SlotStatus.WITHDRAWN
    await db.commit()
    return serialize_booking(row)


async def list_sale_requests(db: AsyncSession, sale_user_id: UUID) -> list[dict]:
    result = await db.execute(
        select(TourRequest)
        .join(TourSlotOption, TourSlotOption.tour_request_id == TourRequest.id)
        .options(
            *_booking_load_options(),
            selectinload(TourRequest.customer).selectinload(CustomerProfile.user),
        )
        .where(
            TourSlotOption.sale_user_id == sale_user_id,
            TourSlotOption.status == SlotStatus.SELECTED,
            TourRequest.status.in_([RequestStatus.WAITING_APPROVAL, RequestStatus.BOOKED]),
        )
        .order_by(TourRequest.preferred_start)
    )
    rows = result.scalars().unique().all()
    changed = False
    for row in rows:
        if row.status == RequestStatus.WAITING_APPROVAL and row.expires_at:
            expires_at = row.expires_at
            if expires_at <= utcnow().astimezone(expires_at.tzinfo):
                row.status = RequestStatus.EXPIRED
                changed = True
    if changed:
        await db.commit()
    rows = [row for row in rows if row.status in (RequestStatus.WAITING_APPROVAL, RequestStatus.BOOKED)]
    data = []
    for row in rows:
        item = serialize_booking(row).model_dump()
        customer = row.customer.user if row.customer and row.customer.user else None
        item["customer"] = {
            "id": str(customer.id),
            "full_name": customer.full_name,
            "phone": customer.phone,
            "email": customer.email,
        } if customer else None
        data.append(item)
    return data


async def accept_sale_request(db: AsyncSession, booking_id: UUID, sale_user_id: UUID) -> dict:
    row = await _get_booking(db, booking_id)
    if not row or row.status != RequestStatus.WAITING_APPROVAL:
        raise BookingConflictError("Yêu cầu không còn chờ xử lý")
    selected = next((s for s in row.slot_options if s.sale_user_id == sale_user_id and s.status == SlotStatus.SELECTED), None)
    if not selected:
        raise BookingPermissionError("Yêu cầu không được phân cho bạn")
    if row.expires_at and row.expires_at <= utcnow().astimezone(row.expires_at.tzinfo):
        row.status = RequestStatus.EXPIRED
        await db.commit()
        raise BookingConflictError("Yêu cầu đã hết hạn")
    conflict = await db.scalar(
        select(func.count(Appointment.id)).where(
            Appointment.sale_user_id == sale_user_id,
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
            Appointment.starts_at < selected.ends_at,
            Appointment.ends_at > selected.starts_at,
        )
    )
    if conflict:
        raise BookingConflictError("Bạn đã có lịch khác trong khung giờ này")
    appointment = Appointment(
        approval_request_id=(await db.execute(text("""
            INSERT INTO approval_requests (
                tour_request_id, slot_option_id, requested_reviewer_user_id,
                status, expires_at, decided_by_user_id, decided_at, decision_note,
                approved_sale_user_id, approved_starts_at, approved_ends_at
            ) VALUES (
                :tour_request_id, :slot_option_id, :sale_user_id,
                'APPROVED', :expires_at, :sale_user_id, now(), 'Sale accepted',
                :sale_user_id, :starts_at, :ends_at
            ) RETURNING id
        """), {
            "tour_request_id": row.id,
            "slot_option_id": selected.id,
            "sale_user_id": sale_user_id,
            "expires_at": row.expires_at or utcnow() + timedelta(minutes=15),
            "starts_at": selected.starts_at,
            "ends_at": selected.ends_at,
        })).scalar_one(),
        booking_code=f"BK{uuid.uuid4().hex[:8].upper()}",
        tour_request_id=row.id,
        customer_user_id=row.customer_user_id,
        property_id=row.property_id,
        sale_user_id=sale_user_id,
        status=AppointmentStatus.CONFIRMED,
        starts_at=selected.starts_at,
        ends_at=selected.ends_at,
        party_size=row.party_size,
        customer_note=row.customer_note,
        meeting_address=row.property.address_line if row.property else None,
        confirmation_sent_at=utcnow(),
    )
    db.add(appointment)
    await db.flush()
    row.status = RequestStatus.BOOKED
    db.add(Notification(
        user_id=row.customer_user_id,
        appointment_id=appointment.id,
        channel=NotificationChannel.IN_APP,
        template_key="booking_confirmed",
        payload={
            "booking_code": appointment.booking_code,
            "property_title": row.property.title if row.property else None,
            "starts_at": appointment.starts_at.isoformat(),
            "ends_at": appointment.ends_at.isoformat(),
        },
        status=DeliveryStatus.PENDING,
    ))

    # Proactively inject confirmed booking message into Customer Chat
    target_conv_id = row.conversation_id
    if not target_conv_id:
        target_conv = await db.scalar(
            select(Conversation)
            .where(Conversation.customer_user_id == row.customer_user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(1)
        )
        if target_conv:
            target_conv_id = target_conv.id

    if target_conv_id:
        local_start = appointment.starts_at.astimezone(LOCAL_TZ)
        local_end = appointment.ends_at.astimezone(LOCAL_TZ) if appointment.ends_at else local_start + timedelta(hours=1)
        duration_mins = int((local_end - local_start).total_seconds() / 60)
        prop_title = row.property.title if row.property else "Bất động sản"
        prop_addr = row.property.address_line if row.property else "Địa chỉ BĐS"
        prop_id_str = str(row.property_id)
        sale_user = await db.get(User, sale_user_id)
        sale_name = sale_user.full_name if sale_user else "Chuyên viên tư vấn"

        chat_msg = (
            f"🎉 **Lịch xem nhà của bạn ĐÃ ĐƯỢC XÁC NHẬN!**\n\n"
            f"📋 **Mã booking chính thức:** `{appointment.booking_code}` (Yêu cầu: `{row.request_code}`)\n\n"
            f"🏠 **Căn hộ đã chọn:**\n"
            f"   - **Tên căn:** {prop_title}\n"
            f"   - **Địa chỉ:** {prop_addr}\n"
            f"   - **ID:** `{prop_id_str}`\n\n"
            f"📅 **Lịch xem nhà:**\n"
            f"   - **Ngày:** {local_start.strftime('%d/%m/%Y')}\n"
            f"   - **Giờ:** {local_start.strftime('%H:%M')} – {local_end.strftime('%H:%M')}\n"
            f"   - **Thời lượng:** {duration_mins} phút\n\n"
            f"👤 **Sale phụ trách:** {sale_name}\n"
            f"📍 **Địa điểm gặp:** {appointment.meeting_address or prop_addr}\n"
            f"🔄 **Trạng thái:** `CONFIRMED` (Đã duyệt)\n\n"
            f"💡 **Lưu ý:**\n"
            f"   - Quý khách vui lòng mang theo CMND/CCCD\n"
            f"   - Đến đúng giờ hẹn để trải nghiệm xem nhà tốt nhất\n"
            f"   - Liên hệ Sale hoặc nhắn trực tiếp cho Nera nếu cần đổi ngày/hủy lịch\n\n"
            f"Bạn nhớ đến đúng giờ nhé! 😊"
        )
        db.add(Message(
            conversation_id=target_conv_id,
            role=MessageRole.ASSISTANT,
            content_redacted=chat_msg,
            structured_payload={
                "notification_type": "APPOINTMENT_CONFIRMED",
                "booking_code": appointment.booking_code,
                "request_code": row.request_code,
            },
        ))
        try:
            from src.services.memory import get_short_term_memory
            memory = get_short_term_memory()
            await memory.append_message(
                str(target_conv_id),
                role="assistant",
                content=chat_msg,
            )
        except Exception:
            pass
    reminder_specs = [
        (row.customer_user_id, timedelta(hours=24), "tour_reminder_24h"),
        (sale_user_id, timedelta(hours=2), "sale_departure_reminder"),
        (row.customer_user_id, timedelta(minutes=30), "tour_reminder_30m"),
    ]
    for recipient_id, before, template_key in reminder_specs:
        scheduled_at = appointment.starts_at - before
        if scheduled_at > utcnow().astimezone(scheduled_at.tzinfo):
            db.add(Notification(
                user_id=recipient_id,
                appointment_id=appointment.id,
                channel=NotificationChannel.IN_APP,
                template_key=template_key,
                payload={
                    "booking_code": appointment.booking_code,
                    "property_title": row.property.title if row.property else None,
                    "starts_at": appointment.starts_at.isoformat(),
                    "meeting_address": appointment.meeting_address,
                },
                scheduled_at=scheduled_at,
                status=DeliveryStatus.PENDING,
            ))
    await db.commit()
    return serialize_booking(await _get_booking(db, row.id))


async def reject_sale_request(db: AsyncSession, booking_id: UUID, sale_user_id: UUID, reason: str | None) -> dict:
    row = await _get_booking(db, booking_id)
    if not row or row.status != RequestStatus.WAITING_APPROVAL:
        raise BookingConflictError("Yêu cầu không còn chờ xử lý")
    selected = next((s for s in row.slot_options if s.sale_user_id == sale_user_id and s.status == SlotStatus.SELECTED), None)
    if not selected:
        raise BookingPermissionError("Yêu cầu không được phân cho bạn")
    selected.status = SlotStatus.WITHDRAWN
    row.extracted_requirements = {**(row.extracted_requirements or {}), "rejection_reason": reason or "Sale từ chối"}
    reassigned = await _reassign_waiting_request(db, row, trigger="sale_rejected")
    if not reassigned:
        row.status = RequestStatus.REJECTED
        await _notify_customer_and_operators(
            db,
            row,
            "booking_needs_new_time",
            "Không còn Sale phù hợp cho khung giờ đã chọn",
        )
    await db.commit()
    return serialize_booking(await _get_booking(db, row.id))


async def _notify_customer_and_operators(
    db: AsyncSession,
    row: TourRequest,
    template_key: str,
    message: str,
) -> None:
    payload = {
        "request_code": row.request_code,
        "property_title": row.property.title if row.property else None,
        "starts_at": row.preferred_start.isoformat() if row.preferred_start else None,
        "message": message,
    }
    db.add(Notification(
        user_id=row.customer_user_id,
        channel=NotificationChannel.IN_APP,
        template_key=template_key,
        payload=payload,
        status=DeliveryStatus.PENDING,
    ))
    operators = (await db.execute(
        select(User.id).where(
            User.role.in_([UserRole.ADMIN, UserRole.COORDINATOR]),
            User.status == UserStatus.ACTIVE,
        )
    )).scalars().all()
    for user_id in operators:
        db.add(Notification(
            user_id=user_id,
            channel=NotificationChannel.IN_APP,
            template_key="booking_requires_attention",
            payload=payload,
            status=DeliveryStatus.PENDING,
        ))


async def _reassign_waiting_request(db: AsyncSession, row: TourRequest, trigger: str) -> bool:
    """Assign the same slot to the least-busy eligible Sale not tried before."""
    if not row.preferred_start or not row.preferred_end:
        return False
    tried_sale_ids = {slot.sale_user_id for slot in row.slot_options}
    candidates = (await db.execute(
        select(SaleProfile)
        .join(User, User.id == SaleProfile.user_id)
        .where(
            SaleProfile.is_accepting_tours.is_(True),
            User.status == UserStatus.ACTIVE,
            SaleProfile.user_id.not_in(tried_sale_ids),
        )
    )).scalars().all()
    sale_ids = [sale.user_id for sale in candidates]
    if not sale_ids:
        return False

    busy_sale_ids = set((await db.execute(
        select(Appointment.sale_user_id).where(
            Appointment.sale_user_id.in_(sale_ids),
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
            Appointment.starts_at < row.preferred_end,
            Appointment.ends_at > row.preferred_start,
        )
    )).scalars().all())

    busy_sale_ids.update((await db.execute(
        select(TourSlotOption.sale_user_id)
        .join(TourRequest, TourRequest.id == TourSlotOption.tour_request_id)
        .where(
            TourSlotOption.sale_user_id.in_(sale_ids),
            TourSlotOption.status == SlotStatus.SELECTED,
            TourRequest.status == RequestStatus.WAITING_APPROVAL,
            TourRequest.expires_at > func.now(),
            TourSlotOption.starts_at < row.preferred_end,
            TourSlotOption.ends_at > row.preferred_start,
        )
    )).scalars().all())

    eligible_sales = [sale for sale in candidates if sale.user_id not in busy_sale_ids]
    if not eligible_sales:
        return False

    eligible_sale_ids = [sale.user_id for sale in eligible_sales]
    start_of_day = datetime.combine(row.preferred_start.date(), time.min, tzinfo=row.preferred_start.tzinfo or LOCAL_TZ)
    end_of_day = start_of_day + timedelta(days=1)

    workloads = (await db.execute(
        select(Appointment.sale_user_id, func.count(Appointment.id))
        .where(
            Appointment.sale_user_id.in_(eligible_sale_ids),
            Appointment.starts_at >= start_of_day,
            Appointment.starts_at < end_of_day,
        )
        .group_by(Appointment.sale_user_id)
    )).all()
    workload_map = {uid: count for uid, count in workloads}

    available = [(workload_map.get(sale.user_id, 0), sale) for sale in eligible_sales]
    if not available:
        return False
    _, sale = min(available, key=lambda item: item[0])
    expires_at = utcnow() + timedelta(minutes=REQUEST_HOLD_MINUTES)
    row.status = RequestStatus.WAITING_APPROVAL
    row.expires_at = expires_at
    db.add(TourSlotOption(
        tour_request_id=row.id,
        sale_user_id=sale.user_id,
        status=SlotStatus.SELECTED,
        starts_at=row.preferred_start,
        ends_at=row.preferred_end,
        valid_until=expires_at,
        selected_at=utcnow(),
        score=90,
        score_explanation={"source": "automatic_reassignment", "trigger": trigger},
    ))
    payload = {
        "request_code": row.request_code,
        "property_title": row.property.title if row.property else None,
        "starts_at": row.preferred_start.isoformat(),
        "trigger": trigger,
    }
    db.add(Notification(
        user_id=sale.user_id,
        channel=NotificationChannel.IN_APP,
        template_key="sale_booking_request",
        payload=payload,
        status=DeliveryStatus.PENDING,
    ))
    db.add(Notification(
        user_id=row.customer_user_id,
        channel=NotificationChannel.IN_APP,
        template_key="booking_sale_reassigned",
        payload=payload,
        status=DeliveryStatus.PENDING,
    ))
    return True


async def reassign_expired_requests(db: AsyncSession) -> tuple[int, int]:
    """Reassign unanswered requests; escalate only after all Sales were tried."""
    now = utcnow()
    rows = (await db.execute(
        select(TourRequest)
        .options(*_booking_load_options())
        .where(
            TourRequest.status == RequestStatus.WAITING_APPROVAL,
            TourRequest.expires_at <= now,
        )
        .with_for_update(skip_locked=True)
    )).scalars().unique().all()
    reassigned = expired = 0
    for row in rows:
        for slot in row.slot_options:
            if slot.status == SlotStatus.SELECTED:
                slot.status = SlotStatus.EXPIRED
        if await _reassign_waiting_request(db, row, trigger="sale_timeout"):
            reassigned += 1
        else:
            row.status = RequestStatus.EXPIRED
            await _notify_customer_and_operators(
                db,
                row,
                "booking_request_expired",
                "Tất cả Sale phù hợp đều bận; cần chọn khung giờ mới",
            )
            expired += 1
    return reassigned, expired


async def list_all_bookings(db: AsyncSession, limit: int = 50) -> list[dict]:
    result = await db.execute(
        select(TourRequest)
        .options(
            *_booking_load_options(),
            selectinload(TourRequest.customer).selectinload(CustomerProfile.user),
        )
        .order_by(TourRequest.created_at.desc())
        .limit(limit)
    )
    data = []
    for row in result.scalars().unique().all():
        item = serialize_booking(row).model_dump()
        customer = row.customer.user if row.customer and row.customer.user else None
        item["customer"] = {
            "id": str(customer.id),
            "full_name": customer.full_name,
            "phone": customer.phone,
            "email": customer.email,
        } if customer else None
        data.append(item)
    return data


async def reschedule_customer_booking(
    db: AsyncSession,
    booking_id: UUID,
    customer_id: UUID,
    sale_user_id: UUID,
    new_preferred_start: datetime,
    new_preferred_end: datetime,
) -> dict:
    """Reschedule a booking by cancelling the old one and creating a new tour request."""
    from src.schemas.booking import TourRequestCreate

    old = await _get_booking(db, booking_id)
    if not old or old.customer_user_id != customer_id:
        raise BookingNotFoundError("Không tìm thấy lịch xem")
    if old.status not in (RequestStatus.BOOKED, RequestStatus.WAITING_APPROVAL):
        raise BookingConflictError("Chỉ có thể dời lịch đã xác nhận hoặc đang chờ")

    async with db.begin_nested():
        # Cancel the old booking
        old.status = RequestStatus.CANCELLED
        if old.appointment:
            old.appointment.status = AppointmentStatus.RESCHEDULED
            old.appointment.cancelled_at = utcnow()
            old.appointment.cancellation_reason = "Khách hàng yêu cầu dời lịch"
        for slot in old.slot_options:
            slot.status = SlotStatus.WITHDRAWN

        # Create a new tour request with the new times
        new_request = TourRequestCreate(
            property_id=old.property_id,
            sale_user_id=sale_user_id,
            preferred_start=new_preferred_start,
            preferred_end=new_preferred_end,
            pax_count=old.party_size,
            customer_note=f"Dời lịch từ {old.request_code}",
            is_reschedule=True,
        )
        new_row = await create_tour_request(db, customer_id, new_request)
        return serialize_booking(new_row)

