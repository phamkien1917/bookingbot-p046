# Phạm Trung Kiên — Tech Lead & AI Core Engineer

**Dự án:** Nera — Trợ lý AI bất động sản & đặt lịch xem nhà O2O (P-046 / 046LTD)  
**Bản chạy thật:** <https://www.nerahome.space/>  
**Mã nguồn:** [AI20K-Build-Phase-Cohort-3/P-046](https://github.com/AI20K-Build-Phase-Cohort-3/P-046)  
**Đóng góp trong git:** Kiến trúc sư trưởng toàn bộ mã nguồn Backend FastAPI, Lõi AI Multi-Agent, CSDL PostgreSQL 18 bảng và Frontend Next.js 14 App Router.

---

## Vai trò trong một câu

Trong khi PM định hình bài toán và đo lường độ chính xác, phần việc của tôi là **biến toàn bộ kiến trúc O2O thành một hệ thống phần mềm chạy thật, chịu tải song song, bảo toàn ngữ cảnh đa lượt và không sập khi dịch vụ bên thứ ba gặp sự cố.**

| Hạng mục | Trước khi giải quyết | Giải pháp & Kết quả thực tế | Kiểm chứng |
|:---|:---|:---|:---|
| **Lõi AI Multi-Agent** | Prompt đơn lẻ, mất ngữ cảnh khi so sánh | **LangGraph StateGraph 5 nodes** + So sánh đa căn hộ | `src/agents/graph.py` |
| **Tính toán Khoảng cách** | Ước lượng km thủ công hoặc gọi API rời rạc | **Goong Maps Distance Matrix Batch + Spatial SQL** | `src/services/geo_service.py` |
| **Rủi ro Hạ tầng** | Redis sập làm crash cả server | **Lớp đệm In-Memory Fallback tự động chuyển mạch** | `src/services/redis_service.py` |
| **Giao diện & Vận hành** | Prototype HTML tĩnh | **25 Routes Next.js 14 + Sale & Admin Dashboard** | `frontend/src/app/` |

---

## 1. Lõi AI Multi-Agent & Quản trị Trạng thái (LangGraph)

Tôi thiết kế đồ thị trạng thái đàm thoại trên LangGraph, chia nhỏ trách nhiệm cho từng Agent chuyên biệt thay vì dồn vào một prompt khổng lồ:

- **`Supervisor`:** Phân loại ý định người dùng (GREETING, SEARCH, COMPARE, DETAIL, BOOKING, AFFORDABILITY, OUT_OF_SCOPE).
- **`InventoryAgent`:** Sinh câu truy vấn SQL Grounding có điều kiện, đối chiếu dữ liệu thật từ kho 3.796 căn.
- **`BookingAgent`:** Đàm phán khung giờ rảnh của Sale, kích hoạt khóa giữ chỗ 15 phút (`PropertyHold`).
- **`AssignmentAgent`:** Tìm kiếm và điều phối đúng Sale phụ trách khu vực bất động sản.
- **`RespondNode`:** Tổng hợp phản hồi, định dạng danh sách thẻ BĐS và truyền phát SSE (Server-Sent Events) về client.

**Giải quyết bài toán So sánh Đa lượt (Multi-turn Comparison):**  
Xây dựng cơ chế trích xuất ma trận thuộc tính (giá, diện tích, vị trí, tiện ích, số phòng ngủ) giữa 2 hay nhiều căn hộ khách yêu cầu so sánh, tự động định dạng thành bảng so sánh Markdown trực quan kèm nhận định ưu/nhược điểm từng căn.

📄 [`src/agents/graph.py`](../src/agents/graph.py) ·
[`src/agents/nodes/supervisor.py`](../src/agents/nodes/supervisor.py) ·
[`src/agents/nodes/inventory_agent.py`](../src/agents/nodes/inventory_agent.py)

---

## 2. Tích hợp Bản đồ Địa lý & Spatial Optimization (Goong Maps)

Để người tìm nhà biết chính xác khoảng cách từ căn hộ đến nơi làm việc hoặc trường học:

1. **Chuyển đổi địa chỉ & Tính ma trận cự ly:**  
   Tích hợp Goong Geocoding và Goong Distance Matrix API để tính toán chính xác số kilomet và số phút di chuyển bằng xe máy/ô tô theo mạng lưới giao thông thực tế tại Việt Nam.
2. **Kỹ thuật Gom lô (Batch Request) & Lọc không gian (Spatial SQL):**  
   Thay vì gọi API Goong cho từng căn hộ (gây chậm và tốn quota), hệ thống lọc sơ bộ theo bán kính tọa độ trong PostgreSQL trước, sau đó **gom toàn bộ tọa độ đích vào một lượt gọi Batch Distance Matrix duy nhất**.
3. **Bản đồ trực quan trong hội thoại & Sale Route Map:**  
   Nhúng iframe bản đồ lộ trình tương tác trực tiếp ngay dưới thẻ căn hộ trong khung chat, và xây dựng bản đồ số `/sale/route-map` hiển thị tất cả các điểm hẹn xem nhà trong ngày của nhân viên Sale trên nền CartoDB Voyager tiles.

📄 [`src/services/geo_service.py`](../src/services/geo_service.py) ·
[`frontend/src/app/sale/route-map/page.tsx`](../frontend/src/app/sale/route-map/page.tsx)

---

## 3. CSDL PostgreSQL 18 Bảng & Cơ chế Khóa Chống Trùng Lịch

Thiết kế cơ sở dữ liệu quan hệ hoàn chỉnh phục vụ luồng nghiệp vụ O2O từ online sang offline:

```
[users] ──┬── [customer_profiles] ──── [conversations] ──── [messages]
          │
          └── [sale_profiles] ──────── [appointments] ──┬─ [properties] ── [property_media]
                                                        │
                                                        └─ [property_holds] (15-min Lock)
```

- **Xác thực & Phân quyền (RBAC 4 vai trò):** Quản lý phiên làm việc qua JWT lưu trong HttpOnly Cookie (`CUSTOMER`, `SALE`, `COORDINATOR`, `ADMIN`). Tích hợp Google Sign-in OAuth.
- **Cơ chế Khóa Chống Trùng lịch 100%:** Sử dụng PostgreSQL `pg_advisory_xact_lock` kết hợp bản ghi `PropertyHold` thời hạn 15 phút. Khi một khách hàng bấm giữ chỗ căn hộ tại một khung giờ, toàn bộ các request song song khác đều bị chặn lại và thông báo slot đang được giữ.

📄 [`src/database/models.py`](../src/database/models.py) ·
[`src/services/property_hold_service.py`](../src/services/property_hold_service.py) ·
[`src/services/auth_service.py`](../src/services/auth_service.py)

---

## 4. Hạ tầng Kiên cường: Lớp Dự phòng In-Memory Fallback

Một trong những rủi ro lớn nhất của hệ thống đàm thoại AI là dịch vụ bộ nhớ đệm (Redis) gặp sự cố mạng hoặc quá tải:

- **Tự động chuyển mạch In-Memory RAM:** Tôi thiết kế lớp `InMemoryFallback` trong `src/services/redis_service.py`. Khi kết nối Redis bị ngắt, hệ thống **tự động fallback về lưu trữ trong bộ nhớ RAM của tiến trình mà không văng exception hay gián đoạn phiên hội thoại của người dùng**.
- **Sliding Window Rate Limiter:** Thiết lập bộ giới hạn 120 request/phút bảo vệ API backend trước các đợt spam request.

📄 [`src/services/redis_service.py`](../src/services/redis_service.py) ·
[`tests/test_oauth_redis_fallback.py`](../tests/test_oauth_redis_fallback.py)

---

## 5. Ứng dụng Frontend Next.js 14 App Router (25 Routes)

Xây dựng toàn bộ giao diện người dùng trên nền tảng Next.js 14 App Router với hiệu năng cao và thiết kế hiện đại:

- **25 Routes chức năng hoàn chỉnh:**
  - Khách hàng: Trang chủ (`/`), Chatbot AI (`/chat`), Khám phá BĐS (`/properties`, `/properties/[id]`), Đặt lịch (`/booking/schedule`, `/booking/hold`), Lịch hẹn cá nhân (`/my-bookings`), Yêu thích (`/saved`), Trí nhớ AI (`/memory`).
  - Vận hành: Bảng điều khiển Sale (`/sale`), Bản đồ lộ trình (`/sale/route-map`), Quản trị Admin (`/admin`).
- **Trải nghiệm đàm thoại mượt mà:** Hiệu ứng Typewriter tuần tự đồng bộ với việc xuất hiện của các thẻ BĐS, loại bỏ hoàn toàn hiện tượng nhấp nháy giao diện (Hydration Mismatch).
- **Hệ thống Design System:** Sử dụng Tailwind CSS, Framer Motion, Lucide Icons, Glassmorphism, Sonner Toast thông báo và Skeleton Shimmer loading.

📄 [`frontend/src/app/`](../frontend/src/app/) ·
[`frontend/src/components/chat/`](../frontend/src/components/chat/)

---

## 6. DevOps & Tự động Hóa Triển khai

- **Render Blueprint (`render.yaml`):** Cấu hình tự động khởi chạy FastAPI Backend và cơ sở dữ liệu PostgreSQL trên Render.
- **Vercel Edge Deployment:** Tối ưu hóa frontend Next.js chạy tại Edge Network Hồng Kông (HKG) cho tốc độ tải trang cực nhanh tại Việt Nam.
- **Auto-Seed Data:** Tự động khởi tạo dữ liệu mẫu và 20 tài khoản Sale XHome khu vực khi database khởi động lần đầu, giúp việc review và chấm bài của Ban Giám Khảo diễn ra trơn tru mà không cần thiết lập thủ công.

📄 [`render.yaml`](../render.yaml) ·
[`Dockerfile`](../Dockerfile) ·
[`docker-compose.yml`](../docker-compose.yml)

---

## Nguyên tắc kỹ thuật

**Code chạy được là điều kiện cần, độ tin cậy và khả năng tự phục hồi là điều kiện đủ.** Mọi tầng từ API, Agent, Database đến Frontend đều phải có cơ chế xử lý lỗi tường minh, không bao giờ để lộ lỗi hệ thống ra giao diện khách hàng.
