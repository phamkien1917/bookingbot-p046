# BÁO CÁO MINH CHỨNG TOÀN DIỆN ĐÓNG GÓP CỦA TECH LEAD & AI CORE (PHẠM TRUNG KIÊN)
**Dự án:** Nera — AI Real Estate & O2O Booking Platform (P-046 / 046LTD)  
**Nhân sự đảm nhiệm:** **Phạm Trung Kiên**  
**Vai trò:** **Tech Lead & AI Core Engineer**  
**Bản chạy thực tế (Live URL):** [https://www.nerahome.space/](https://www.nerahome.space/)  
**Mã nguồn Repository:** [AI20K-Build-Phase-Cohort-3/P-046](https://github.com/AI20K-Build-Phase-Cohort-3/P-046)  

---

## 📌 TỔNG QUAN PHẠM VI TRÁCH NHIỆM

Trong dự án Nera, **Phạm Trung Kiên** đảm nhiệm vai trò **Tech Lead & AI Core Engineer**, là kiến trúc sư kỹ thuật trưởng chịu trách nhiệm thiết kế hệ thống, lập trình lõi AI Multi-Agent, tích hợp bản đồ địa lý Goong Maps, phát triển toàn bộ API Backend FastAPI, thiết kế CSDL PostgreSQL 18 bảng, xây dựng lớp bộ nhớ đệm kiên cường (Redis InMemoryFallback) và toàn bộ ứng dụng Frontend Next.js 14 App Router.

```
                             PHẠM TRUNG KIÊN (TECH LEAD & AI CORE)
                                              │
    ┌─────────────────┬───────────────────────┼───────────────────────┬─────────────────┐
    ▼                 ▼                       ▼                       ▼                 ▼
[AI MULTI-AGENT]   [MAPS & GEO ROUTING]    [BACKEND & DATABASE]    [RESILIENCE & DB]  [FRONTEND NEXT.JS]
• LangGraph State  • Goong Maps Distance   • FastAPI Async REST    • PostgreSQL 18 Bảng• 25 App Routes
• Multi-turn NLG   • Proximity SQL Query   • RBAC 4 Roles (JWT)    • Advisory Lock     • Typewriter Stream
• Amortization Loan• Iframe Chỉ đường Live • Sale Assignment Engine• Redis Fallback RAM• Sale/Admin Map
• Compare Engine   • Batch Distance Matrix • Auto-Seed Accounts    • Rate Limiting     • Framer Motion UI
```

---

## 🧠 KHỐI 1: LÕI AI MULTI-AGENT & QUẢN TRỊ TRẠNG THÁI (AI CORE & LANGGRAPH)

Trực tiếp thiết kế và lập trình lõi điều phối Multi-Agent trên LangGraph, giải quyết các bài toán suy luận phức tạp trong hội thoại bất động sản:

1. **Kiến trúc LangGraph Multi-Agent Engine:**
   - Xây dựng StateGraph phân tách trách nhiệm rõ ràng: `Supervisor` ➔ `InventoryAgent` / `BookingAgent` / `AssignmentAgent` / `HITLAgent` ➔ `RespondNode`.
   - Thiết kế cấu trúc `AgentState` duy trì trạng thái tìm kiếm, lịch sử tin nhắn, thông tin giữ chỗ và bộ nhớ khách hàng qua nhiều lượt.
2. **Cơ chế Suy luận & So sánh Đa lượt (Intelligent Multi-Turn & Comparison Engine):**
   - Lập trình tính năng so sánh đa căn hộ: Trích xuất các thuộc tính đối sánh (giá, diện tích, vị trí, tiện ích, số phòng), xuất bảng Markdown trực quan trong khung chat.
   - Tính năng đánh giá sâu từng căn (Property Detail Analysis / Deep Review): Cho phép khách hỏi chi tiết về một BĐS cụ thể đang xem.
   - Nhận diện và xử lý linh hoạt số lượng căn yêu cầu (Dynamic Quantity Parsing) và phân bổ xen kẽ các tỉnh thành (Region Province Interleaving).
3. **Động cơ Tính toán Tài chính & Trả góp (Loan Amortization Engine):**
   - Viết module tính toán hạn mức vay mua nhà, lịch trả góp gốc và lãi hàng tháng theo niên kim cố định hoặc dư nợ giảm dần trong `src/services/affordability.py`.
   - Kiểm tra trần ngân sách thực tế và sinh các câu gợi ý phản hồi ngữ cảnh (Contextual Dynamic Quick Replies).
4. **Tích hợp Trí nhớ Người dùng (Customer Memory & Resume Flow):**
   - Tích hợp `CustomerMemoryService` lưu trữ sở thích dài hạn (quận ưa thích, số phòng, khoảng giá) và tự động nhận diện ý định tiếp tục hành trình cũ (`RESUME_SEARCH_INTENT`).
5. **Ổn định & Chống lỗi Hội thoại (Agent Hardening):**
   - Xử lý triệt để lỗi Hydration Mismatch và giật lag giao diện bằng hiệu ứng Typewriter tuần tự.
   - Chặn gửi trùng lặp tin nhắn (Double submit prevention) khi đang tải và thêm nút Dừng chat trực tiếp (Stop streaming).

---

## 🗺️ KHỐI 2: TÍCH HỢP BẢN ĐỒ ĐỊA LÝ & TỐI ƯU LỘ TRÌNH (GEO & MAPS ENGINE)

Xây dựng hệ thống định vị địa lý thông minh giúp người tìm nhà tính toán khoảng cách thực tế tới nơi làm việc:

1. **Tích hợp Goong Maps Distance Matrix & Geocoding API:**
   - Xây dựng `src/services/geo_service.py` chuyển đổi địa chỉ thành tọa độ (Geocoding) và tính toán chính xác khoảng cách (km) và thời gian di chuyển (phút) bằng xe máy/ô tô.
   - Hiển thị badge thời gian di chuyển trực tiếp trên thẻ BĐS và nhúng iframe bản đồ lộ trình Goong Maps tương tác ngay trong khung chat.
2. **Tối ưu Hiệu năng Truy vấn Không gian (Spatial Optimization):**
   - Tối ưu hóa truy vấn SQL theo độ gần (Proximity SQL query) tới các địa danh/trường học/công ty trọng điểm.
   - Gom lô (Batch) các yêu cầu tính khoảng cách tới Goong Distance Matrix API để giảm thiểu thời gian chờ và tiết kiệm hạn mức API.
3. **Bản đồ Lộ trình Chuyên viên Sale (Sale Route Map):**
   - Xây dựng trang `/sale/route-map` hiển thị toàn bộ các điểm hẹn xem nhà trong ngày của Sale trên nền bản đồ số CartoDB Voyager Tiles.

---

## ⚙️ KHỐI 3: KIẾN TRÚC BACKEND & CƠ SỞ DỮ LIỆU (BACKEND & DATABASE)

Trực tiếp thiết kế toàn bộ hệ thống API bất đồng bộ và cơ sở dữ liệu quan hệ cho nền tảng O2O:

1. **Kiến trúc FastAPI Backend (Async I/O):**
   - Xây dựng hệ thống RESTful API chuẩn OpenAPI với 25+ endpoints: Authentication, Chat, Properties, Bookings, Sale, Admin, Favorites, Memory.
   - Hỗ trợ truyền phát dữ liệu thời gian thực qua Server-Sent Events (SSE) cho phản hồi AI streaming.
2. **Hệ Quản trị CSDL PostgreSQL 18 Bảng:**
   - Thiết kế mô hình CSDL quan hệ chuẩn hóa cao: `users`, `properties`, `property_media`, `appointments`, `property_holds`, `sale_profiles`, `customer_profiles`, `conversations`, `messages`, `customer_preferences`, `daily_route_plans`, ...
   - Thiết lập các ràng buộc toàn vẹn dữ liệu, chỉ mục (Indexes) và migrations tương thích Neon / Supabase / Render PostgreSQL.
3. **Xác thực & Phân quyền Đa vai trò (RBAC):**
   - Quản lý phiên an toàn qua JWT lưu trữ trong HttpOnly Cookie.
   - Phân quyền chặt chẽ 4 vai trò (`CUSTOMER`, `SALE`, `COORDINATOR`, `ADMIN`) qua dependency `require_roles`.
   - Tích hợp luồng đăng nhập Google Sign-in OAuth và quên mật khẩu.
4. **Động cơ Phân bổ Sale & Khởi tạo Dữ liệu (Assignment & Seeding Engine):**
   - Xây dựng cơ chế tự động gán Sale phụ trách theo khu vực BĐS, giới hạn quyền tiếp nhận lịch hẹn cho đúng nhân sự.
   - Cơ chế Auto-seed tự động khởi tạo dữ liệu mẫu và danh sách 20 tài khoản Sale khu vực khi hệ thống khởi chạy lần đầu.

---

## 🛡️ KHỐI 4: TÍNH KIÊN CƯỜNG HẠ TẦNG & BỘ NHỚ ĐỆM (RESILIENCE & LOCKS)

Thiết kế các giải pháp bảo vệ hệ thống trước sự cố hạ tầng và tải đồng thời cao:

1. **Lớp Dự phòng Bộ nhớ Đệm (InMemoryFallback Engine):**
   - Thiết kế kiến trúc chuyển đổi trạng thái thông minh trong `src/services/redis_service.py`: Khi kết nối Redis gặp sự cố, hệ thống **tự động chuyển sang sử dụng bộ nhớ RAM (In-Memory Fallback)** mà không làm crash server hay gián đoạn phiên chat của người dùng.
2. **Chống Trùng lịch bằng Advisory Locks:**
   - Kết hợp PostgreSQL `pg_advisory_xact_lock` và bảng `PropertyHold` giữ căn 15 phút, loại bỏ 100% tình trạng 2 khách hàng đặt trùng cùng một slot xem nhà của Sale.
3. **Giới hạn Tần suất (Rate Limiting):**
   - Triển khai thuật toán Sliding Window Rate Limiter (120 req/phút) bảo vệ API khỏi nguy cơ bị spam hoặc tấn công từ chối dịch vụ.

---

## 🎨 KHỐI 5: KỸ THUẬT GIAO DIỆN & TRẢI NGHIỆM NGƯỜI DÙNG (FRONTEND & UX)

Xây dựng toàn bộ ứng dụng Frontend hiện đại, tối ưu trải nghiệm đàm thoại và phân hệ vận hành O2O:

1. **Next.js 14 App Router & 25 Routes Biên dịch:**
   - Xây dựng đầy đủ các phân hệ chức năng: Trang chủ AIHome (`/`), Giao diện Chatbot (`/chat`), Khám phá BĐS (`/properties`, `/properties/[id]`), Đặt lịch (`/booking/schedule`, `/booking/hold`), Bảng điều khiển Sale (`/sale`, `/sale/route-map`), Quản trị Admin (`/admin`), Quản lý lịch cá nhân (`/my-bookings`, `/saved`, `/memory`, `/profile`).
2. **Thiết kế Trải nghiệm Cao cấp (Premium Design System):**
   - Sử dụng Tailwind CSS, Framer Motion, Lucide Icons, Glassmorphism, Sonner Toast thông báo, và hiệu ứng Skeleton Shimmer khi tải dữ liệu.
   - Thẻ BĐS tương tác cao (PropertyCard): Có thể mở rộng xem ảnh, xem tiện ích, gắn badge khoảng cách và kích hoạt trợ lý AI nổi (Floating AI Assistant).
3. **Tối ưu Triển khai & Cross-Domain:**
   - Cấu hình Next.js Standalone Output tối ưu hóa cho Vercel.
   - Xử lý CORS và chia sẻ cookie xác thực an toàn giữa Vercel Frontend (`nerahome.space`) và Render Backend API.

---

## 📑 BẢNG ÁNH XẠ CÁC COMMIT CHÍNH CỦA PHẠM TRUNG KIÊN (GIT EVIDENCE)

| Mã Commit | Loại hình | Mô tả chi tiết phần việc kỹ thuật đã thực hiện |
|:---|:---:|:---|
| `7e90cea` | **Fix/Geo** | Tối ưu hóa truy vấn SQL theo độ gần landmark và batch Goong DistanceMatrix |
| `8e1431d` | **Style/Chat**| Tinh chỉnh giao diện bản đồ tương tác trong khung chat |
| `0a09aa2` | **Fix/Sale** | Giới hạn phân bổ lại lịch hẹn cho đúng Sale phụ trách BĐS |
| `55146ce` | **Feat/Data** | Bổ sung trường xác thực `last_verified_at` và cập nhật kho BĐS |
| `a0f037c` | **Fix/Agent** | Định tuyến và hoàn thiện prompt phân tích chuyên sâu chi tiết BĐS |
| `2c40c1b` | **DevOps** | Xây dựng Render Blueprint (`render.yaml`) và tích hợp CI Deploy Hook |
| `89441c8` | **Feat/UI** | Nâng cấp UI/UX với Framer Motion, Sonner Toast, Skeleton Shimmer, Glassmorphism |
| `a72667a` | **Fix/Geo** | Ngăn chặn cảnh báo gây hiểu lầm khi lọc khoảng cách thành công |
| `bbe93e1` | **Feat/Geo** | Tích hợp khoảng cách Goong Maps, badge thẻ BĐS và iframe chỉ đường |
| `47b9fe1` | **Fix/Agent** | Nâng cấp regex giới hạn địa lý và siết prompt guardrail cho `OUT_OF_SCOPE` |
| `f39406b` | **Fix/AI** | Khắc phục lỗi mất ngữ cảnh AI và chặn hoàn toàn bypass ngoài phạm vi |
| `f722c92` | **Fix/Core** | Giải quyết triệt để 6 issue trọng tâm sau buổi review của Mentor |
| `e67f615` | **Fix/OAuth** | Xây dựng InMemoryFallback cho trao đổi OAuth khi Redis gặp sự cố |
| `9317537` | **Feat/AI** | Nâng cấp NLG, tính toán khoản vay Amortization và quick-replies động |
| `71ad7c6` | **Fix/Chat** | Sửa hydration mismatch và tối ưu hiệu ứng Typewriter tuần tự |
| `7de16b6` | **Feat/Brand**| Tích hợp official Nera logo, symbol, favicon và brand tokens |
| `23e7651` | **Feat/Chat** | Làm kiên cố hóa luồng Agent, session persistence và typewriter streaming |
| `8afb51c` | **Fix/Search**| Hỗ trợ lọc chính xác số phòng ngủ khi người dùng yêu cầu cụ thể |
| `8e2448e` | **Fix/DB** | Runtime migration dọn dẹp dữ liệu đất không hợp lệ trên production |
| `3b01801` | **Fix/Data** | Chuẩn hóa tên tiêu đề BĐS bằng Unicode word boundaries nghiêm ngặt |
| `7a2df85` | **Feat/Data** | Tự động chuẩn hóa và làm đẹp tiêu đề BĐS, giải mã các từ viết tắt |
| `3f1beb7` | **Feat/Search**| Nâng cấp bộ lọc địa lý toàn quốc và bổ sung nút Dừng chat |
| `efed944` | **Feat/UI** | Bóc tách số lượng động, xen kẽ tỉnh thành và thẻ BĐS mở rộng |
| `5df02b6` | **Fix/UI** | Tinh chỉnh nút toggle sidebar linh hoạt trong giao diện chat |
| `69da27e` | **Feat/UI** | Bổ sung nút hamburger toggle cho thanh lịch sử chat thu gọn |
| `59983dd` | **Fix/DB** | Đảm bảo tạo hồ sơ khách hàng khi đăng nhập Google và lưu hội thoại |
| `fe72faf` | **Fix/Auth** | Cầu nối phiên Google OAuth với Cookie frontend và Header Authorization |
| `80f94c6` | **Feat/Auth** | Xây dựng luồng Quên mật khẩu và hỗ trợ Google Sign-in OAuth |
| `4f8e483` | **Fix/Sale** | Sửa render bản đồ lộ trình Sale với CartoDB Voyager tiles |
| `89e1b22` | **Feat/AI** | Bật trợ lý AI nổi (Floating AI Assistant) đánh giá BĐS đang xem |
| `7e95ed1` | **Feat/Auth** | Tự động migrate và seed 20 tài khoản Sale XHome khu vực |
| `866b90e` | **Fix/Map** | Loại bỏ dữ liệu ảo, hiển thị bản đồ Leaflet tiles với CartoDB |
| `bd623de` | **Fix/Deploy**| Ổn định hóa luồng deploy production và luồng đặt lịch O2O |
| `759e050` | **Fix/Booking**| Cho phép người mua xem trước các slot tour khả dụng mà không cần login |
| `19f3379` | **Fix/Auth** | Bật cross-domain credentials, jwt localStorage persistence và CORS |
| `f39964c` | **Feat/DB** | Tự động seed BĐS và tài khoản ban đầu nếu DB rỗng khi khởi động |
| `68c24e5` | **Feat/Agent**| Hoàn thiện so sánh thông minh đa lượt và xác thực login production |
| `84d4c9d` | **Feat/UI** | Render bảng Markdown so sánh phong phú và styled table đẹp mắt |
| `c399efc` | **Feat/Agent**| Khôi phục hệ thống Multi-Agent hoàn chỉnh với khả năng suy luận sâu |

---

## 🏆 TỔNG KẾT

Với khối lượng đóng góp đồ sộ và chất lượng kỹ thuật vượt trội trên toàn bộ các mảng **Lõi AI Multi-Agent**, **Tích hợp Bản đồ Goong Maps**, **FastAPI Backend & CSDL PostgreSQL 18 bảng**, **Tính kiên cường InMemoryFallback**, và **25 Routes Frontend Next.js 14**, vai trò **Tech Lead & AI Core** của **Phạm Trung Kiên** là trụ cột kỹ thuật vững chắc đưa dự án Nera đạt đỉnh cao về hiệu năng, độ tin cậy và sự sẵn sàng cho Demo Day AI20K!
