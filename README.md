# Booking Bot AI

Hệ thống tìm bất động sản và đặt lịch xem nhà gồm FastAPI/LangGraph, Next.js, PostgreSQL và Redis (có fallback bộ nhớ khi Redis không chạy). Hệ thống có bốn vai trò: Khách hàng, Sale, Điều phối và Admin.

## Chạy nhanh trên Windows

Yêu cầu: Python 3.11+, Node.js 20+, PostgreSQL. Chạy các lệnh sau tại `C:\buildAI\P-046`.

```powershell
Copy-Item .env.example .env
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Cập nhật `DATABASE_URL`, `JWT_SECRET_KEY` và API key AI trong `.env`. Khởi tạo database mới bằng bốn file SQL theo đúng thứ tự:

```powershell
psql -U visitops -d visitops -f database/001_schema.sql
psql -U visitops -d visitops -f database/002_seed.sql
psql -U visitops -d visitops -f database/004_crawled_data.sql
psql -U visitops -d visitops -f database/005_batdongsan_data.sql
psql -U visitops -d visitops -f database/006_saved_properties.sql
psql -U visitops -d visitops -f database/007_customer_memory.sql
```

Terminal 1 — backend:

```powershell
cd C:\buildAI\P-046
.\venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — frontend:

```powershell
cd C:\buildAI\P-046\frontend
npm.cmd install
npm.cmd run dev
```

Mở `http://localhost:3005` (script development của frontend dùng cổng 3005). API docs ở `http://localhost:8000/docs`.

Nếu muốn chạy toàn bộ hệ thống demo bằng Docker (PostgreSQL, Redis, backend và frontend):

```powershell
docker compose up --build
```

Sau đó mở `http://localhost:3000`; không cần chạy frontend riêng. Với database Docker cũ đã có volume, chạy thêm migration 006 và 007 bằng `psql` vì thư mục init chỉ chạy khi tạo volume lần đầu.

## Tài khoản demo

Các tài khoản dùng hash dành riêng cho demo chấp nhận mật khẩu `Demo@123` và
mật khẩu cũ `123456`. Tài khoản đăng ký thật vẫn xác thực bằng mật khẩu bcrypt
riêng; không dùng hash demo cho người dùng thật hoặc hệ thống production.

| Vai trò | Email | Giao diện |
|---|---|---|
| Khách hàng | `customer.demo@example.com` | `/`, `/chat`, `/my-bookings` |
| Sale | `kien.sale@example.com` | `/sale` |
| Admin | `admin.demo@example.com` | `/admin` |

Tài khoản seed dùng mật khẩu demo chỉ được chấp nhận khi `APP_ENV=development`. Tài khoản khách đăng ký mới luôn được lưu bằng bcrypt. Trước khi deploy production, đặt `APP_ENV=production`, dùng `JWT_SECRET_KEY` ngẫu nhiên dài và thay hash demo trong dữ liệu seed.

## Luồng nghiệp vụ

1. Khách đăng nhập hoặc đăng ký, tìm căn trên danh sách hay chatbot.
2. Khách chọn ngày và khung giờ thực còn trống, hệ thống giữ yêu cầu trong 15 phút.
3. Sale đăng nhập `/sale` để nhận hoặc từ chối yêu cầu.
4. Khi Sale nhận, hệ thống tạo appointment và khách thấy trang xác nhận/mã booking.
5. Admin theo dõi booking, người dùng, đồng thời khóa/mở tài khoản tại `/admin`.

Phiên đăng nhập dùng cookie HttpOnly. API Sale/Admin và lịch sử chatbot đều kiểm tra vai trò và chủ sở hữu ở backend.

Chat production dùng `POST /api/v1/chat`, chạy graph trong `src/agents/**` và lưu trạng thái hội thoại qua nhiều lượt. LLM trích xuất intent bằng Structured Outputs; bộ parser quyết định các ràng buộc cứng trước khi truy vấn PostgreSQL. Backend vẫn độc quyền phân quyền và booking; xem [kiến trúc chat](docs/chat-architecture.md).

Tìm kiếm theo quãng đường/thời gian và tiện ích lân cận cần bật Geocoding API, Routes API và Places API (New), sau đó đặt `GOOGLE_MAPS_API_KEY`. Nếu chưa cấu hình hoặc tọa độ không vượt qua kiểm tra chất lượng, chatbot sẽ nói rõ chưa xác minh thay vì ước lượng. Reset mật khẩu production cần cấu hình SMTP; token khôi phục hết hạn sau 15 phút và tự vô hiệu sau khi dùng.

Mỗi response công khai `ai_mode`: `llm_grounded`, `llm_direct`, `llm_intent` hoặc `fallback`. Nếu provider lỗi, UI hiện rõ “Fallback theo luật” thay vì giả làm phản hồi AI. Cấu hình model bằng `OPENAI_MODEL_NAME` hoặc `MODEL_NAME` khi dùng OpenRouter.

## Kiểm tra chất lượng

```powershell
cd C:\buildAI\P-046
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe -m pytest tests -q

cd frontend
npm.cmd run lint
npm.cmd run build
```

Smoke test chat (không tạo booking):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_smoke.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_ai.ps1
```

Kiểm thử booking thật dùng một tài khoản customer dùng cho test; script luôn hủy booking đã tạo khi hoàn tất:

```powershell
$env:BOOKINGBOT_TEST_EMAIL="customer.demo@example.com"
$env:BOOKINGBOT_TEST_PASSWORD="Demo@123"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_booking.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_sale_approval.ps1
```

Ma trận kiểm thử thủ công và tự động hóa tiếp theo nằm tại `eval/chat_scenarios.json`.

Bộ acceptance/stress test mở rộng gồm 150 kịch bản có runner HTTP độc lập:

```powershell
python scripts/run_chat_agent_eval.py --limit 10
python scripts/run_chat_agent_eval.py --report eval/results/chat_agent_acceptance_report.json
```

Xem hướng dẫn nhóm test, booking side effects và ngưỡng release tại `eval/CHAT_AGENT_TEST_GUIDE.md`.

Các biến frontend tùy chọn:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Advanced booking completion

- Sale approval creates a real `PropertyHold` from the confirmed appointment.
- Missing Sale cases enter a durable PostgreSQL HITL queue for Coordinator.
- Conflicts and running-late events create alternatives without changing the original booking until the customer confirms.
- Viewing slots are ranked with each customer's `preferred_time_slots` memory.
- Confirmation/reminder jobs support in-app, email, SMS provider and Zalo OA channels with retry.
- Daily routes expose Google Routes traffic evidence, time-window feasibility and an explicit fallback provider.
- Admin analytics exposes conversion funnel, reminder delivery success and no-show rate.

Run the live KPI contract check with a disposable Admin account:

```powershell
$env:BOOKINGBOT_ADMIN_EMAIL="admin.demo@example.com"
$env:BOOKINGBOT_ADMIN_PASSWORD="<demo-password>"
python scripts/run_booking_kpi_eval.py
```
 
