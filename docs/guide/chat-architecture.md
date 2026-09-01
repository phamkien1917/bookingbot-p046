# Kiến trúc chat production

```text
Next.js /chat
    |
    v
POST /api/v1/chat -- rate limit, session ownership, auth context
    |
    v
LangGraph supervisor
    |-- deterministic criteria reconciliation
    |-- structured LLM intent/context
    |
    +-- inventory agent -- PostgreSQL hard filters -- Geo Service
    +-- booking agent ---- booking_service (authorization + locking)
    +-- respond node ----- grounded/direct/fallback response
    |
    v
Redis short-term state + PostgreSQL authenticated conversation
```

## Ranh giới tin cậy

- LLM chỉ phân loại và diễn đạt; SQL, quyền truy cập, giá, UUID và side effect do backend kiểm soát.
- `search_result_refs` giữ pool kết quả gốc; `property_refs` chỉ là các card ở lượt hiện tại. Vì vậy chọn một căn không phá tham chiếu “căn 1/căn 2” ở lượt sau.
- Giá, loại giao dịch, vị trí, loại nhà, phòng, diện tích, hướng, tầng, pháp lý và nội thất là hard filter. Tiêu chí mâu thuẫn tạo câu hỏi xác nhận, không được tự sửa.
- Tin thuê và tin bán không bao giờ trộn. Kho không có tin thuê phải trả về không kết quả.
- Route Matrix cung cấp quãng đường/thời gian theo `DRIVE`, `WALK`, `BICYCLE`, `TRANSIT` hoặc `TWO_WHEELER`. Places Nearby cung cấp bằng chứng tiện ích; khoảng cách POI đang hiển thị rõ là đường chim bay.
- Thiếu API key, provider lỗi hoặc tọa độ sai tỉnh sẽ tạo cảnh báo “chưa xác minh”, không sinh số giả.
- Booking luôn dùng customer đã xác thực, slot thực và transaction/lock trong `booking_service`.
- Cookie đăng nhập là HttpOnly. Google OAuth không đưa JWT lên URL. Reset password dùng token 15 phút gắn với password hash hiện tại.

## State bền vững

Mỗi lượt lưu criteria, soft preferences, household context, commute landmark, giới hạn km/phút, travel mode, nearby categories, pool kết quả, căn đang chọn, lịch/slot và pending action. Redis phục vụ cache; cuộc trò chuyện đã đăng nhập được ghi PostgreSQL và kiểm tra owner khi khôi phục.

## Provenance phản hồi

API trả `ai_mode`, `ai_model`, `ai_latency_ms`, `suggested_actions` và `ai_fallback_reason`. Frontend ưu tiên `suggested_actions` từ backend; không suy luận workflow từ câu chữ nếu server đã cung cấp action.
