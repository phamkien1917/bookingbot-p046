# HỒ SƠ TỔNG HỢP TOÀN DIỆN DỰ ÁN NERA (P-046)
**Dành cho: Vũ Thế Lực (PM & AI Product Lead) — Đội 046LTD**  
**Sản phẩm:** Nera — Trợ lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O  
**Chương trình:** AI20K Build Phase Cohort 3  
**Bản chạy thực tế (Live URL):** [https://www.nerahome.space/](https://www.nerahome.space/)  
**Mã nguồn (Repository):** [github.com/AI20K-Build-Phase-Cohort-3/P-046](https://github.com/AI20K-Build-Phase-Cohort-3/P-046)

---

# MỤC LỤC
1. [TỔNG QUAN BÀI TOÁN & GIẢI PHÁP SẢN PHẨM](#1-tổng-quan-bài-toán--giải-pháp-sản-phẩm)
2. [KIẾN TRÚC KỸ THUẬT & CƠ CHẾ VẬN HÀNH](#2-kiến-trúc-kỹ-thuật--cơ-chế-vận-hành)
3. [BÁO CÁO PHÂN CÔNG & ĐÓNG GÓP THỰC TẾ (LỰC & KIÊN)](#3-báo-cáo-phân-công--đóng-góp-thực-tế-lực--kiên)
4. [KẾT QUẢ ĐO LƯỜNG & KIỂM THỬ THỰC NGHIỆM](#4-kết-quả-đo-lường--kiểm-thử-thực-nghiệm)
5. [ĐỐI CHIẾU XỬ LÝ 6 PHẢN HỒI CỦA MENTOR](#5-đối-chiếu-xử-lý-6-phản-hồi-của-mentor)
6. [KỊCH BẢN THUYẾT TRÌNH BẢO VỆ 5 PHÚT (DEMO DAY PITCH)](#6-kịch-bản-thuyết-trình-bảo-vệ-5-phút-demo-day-pitch)
7. [BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN (DEFENSE Q&A)](#7-bộ-câu-hỏi-vấn-đáp-phản-biện-defense-qa)
8. [KẾ HOẠCH HÀNH ĐỘNG TIẾP THEO (NEXT STEPS)](#8-kế-hoạch-hành-động-tiếp-theo-next-steps)

---

# 1. TỔNG QUAN BÀI TOÁN & GIẢI PHÁP SẢN PHẨM

### 📍 1.1. Thực trạng & Nỗi đau ngành BĐS O2O (Online-to-Offline)
Trong quy trình môi giới bất động sản truyền thống, việc hẹn khách đi xem nhà mẫu hoặc căn thực tế gặp nhiều bất cập:
- **Người tìm nhà:** Bị phân mảnh thông tin giữa hàng ngàn tin đăng rời rạc; bộ lọc tìm kiếm cứng nhắc, không lưu lại ngữ cảnh; mỗi lần quay lại tìm kiếm phải nhập lại toàn bộ tiêu chí.
- **Doanh nghiệp & Đội ngũ Sale:** Điều phối lịch rảnh thủ công qua tin nhắn Zalo/Chat, dẫn đến tình trạng **trùng lịch (double-booking)** giữa các Sale, bỏ lỡ khách hàng tiềm năng và tốn nhiều thời gian sàng lọc sơ bộ.

### 🎯 1.2. Giải pháp Nera
Nera là hệ thống trợ lý AI đàm thoại giúp:
1. **Tìm kiếm BĐS bằng ngôn ngữ tự nhiên:** Hiểu các nhu cầu mềm ("căn 2PN gần bệnh viện Bạch Mai dưới 3 tỷ, tiện đi làm").
2. **Duy trì bộ nhớ ngữ cảnh đa lượt (Multi-turn Memory):** Tự động kế thừa các tiêu chí đã chọn mà khách không cần nhắc lại.
3. **Đặt lịch thông minh & Giữ chỗ tạm thời (Soft-hold 15 phút):** Tự động đối soát khung giờ trống của Sale trong cơ sở dữ liệu và khóa tạm slot để tránh trùng lịch.
4. **Phê duyệt con người (Human-in-the-loop - HITL):** Bắt buộc nhân viên Sale đăng nhập hệ thống duyệt lịch trước khi tạo lịch hẹn chính thức.

---

# 2. KIẾN TRÚC KỸ THUẬT & CƠ CHẾ VẬN HÀNH

```
[ Frontend: Next.js 14 / Vercel ]
        │ (REST API / SSE Streaming / HttpOnly Cookie)
        ▼
[ Backend: FastAPI / Render ] ── [ Auth & RBAC: 4 Roles (Customer, Sale, Coord, Admin) ]
        │
        ▼
[ Multi-Agent Orchestration: LangGraph ]
  ├── Supervisor Node (Điều phối & Phân loại Intent)
  ├── Inventory Agent (Truy vấn dữ liệu & Lọc ràng buộc cứng)
  ├── Booking Agent (Xác thực slot lịch & Tạo đề xuất)
  └── Respond Node (Sinh câu trả lời tự nhiên có Grounding)
        │
        ├── LLM Service (GPT-4o-mini / OpenRouter)
        ├── External APIs: Goong Maps & Google Routes (Đo khoảng cách & Tuyến đường)
        ├── Affordability Engine (Tính toán khả năng tài chính & Khoản vay)
        └── Memory Layer: Mem0 OSS (Redis Cache + PostgreSQL Persistence)
```

### 🔒 2.1. Phân quyền chặt chẽ (RBAC) 4 vai trò
- **Khách hàng (`CUSTOMER`):** Tìm kiếm nhà, trò chuyện AI, xem chi tiết BĐS, đặt lịch hẹn và quản lý lịch cá nhân (`/my-bookings`).
- **Chuyên viên Sale (`SALE`):** Nhận thông báo, xem danh sách yêu cầu đặt lịch, duyệt/từ chối lịch hẹn, xem lịch trình trong ngày (`/sale`).
- **Điều phối viên (`COORDINATOR`):** Phân bổ lại lịch hẹn khi Sale bận hoặc xử lý hàng đợi HITL.
- **Quản trị viên (`ADMIN`):** Quản lý người dùng, khóa/mở tài khoản, theo dõi số liệu KPI và phễu chuyển đổi (`/admin`).

### 🛡️ 2.2. Tính kiên cường của hệ thống (System Resilience)
- **In-memory Fallback:** Khi dịch vụ Redis gặp sự cố, hệ thống tự động chuyển sang lưu trữ tạm thời trên bộ nhớ RAM của tiến trình backend, không làm sập ứng dụng.
- **Rule-based Fallback:** Khi API mô hình ngôn ngữ (OpenAI/OpenRouter) bị gián đoạn, hệ thống kích hoạt luật cứng và hiển thị minh bạch nhãn `ai_mode: fallback` trên giao diện người dùng.

---

# 3. BÁO CÁO PHÂN CÔNG & ĐÓNG GÓP THỰC TẾ (LỰC & KIÊN)

### 👤 3.1. Vũ Thế Lực — PM / AI Product & Data Quality Lead
- **Định hình bài toán & Nghiệp vụ sản phẩm:** Xây dựng User Journey cho 4 nhóm người dùng, thiết kế cơ chế giữ căn 15 phút (`PropertyHold`) và luồng phê duyệt con người (HITL).
- **Thiết kế UX Explainability (`feat(chat): confirm what Nera understood`):** Đưa ra quyết định sản phẩm: Trước khi trả kết quả danh sách nhà, AI bắt buộc phải tóm tắt lại những gì đã hiểu để người dùng kiểm chứng, tạo dựng niềm tin (User Trust).
- **Thiết lập chốt chặn Trung thực (`fix(search): recognise rental vocabulary`):** Xây dựng rào chắn ngăn AI bịa đặt: Khi dữ liệu hệ thống chỉ có tin Bán mà khách hỏi Thuê, AI thẳng thắn thừa nhận hệ thống chưa có dữ liệu thuê thay vì tự sinh tin giả.
- **Làm sạch & Bảo vệ dữ liệu (`fix(inventory): strip broker contact pitch`):** Xây dựng bộ lọc loại bỏ số điện thoại rác và lời chào môi giới ngoài từ dữ liệu crawl để bảo vệ uy tín nền tảng.
- **Kiểm soát chất lượng & Ổn định nền tảng:** Xử lý lỗi console UTF-8 trên Windows, sửa lỗi crash `Path` khi khởi động auto-seed, chuẩn hóa tài liệu kiến trúc.

### 👤 3.2. Phạm Trung Kiên — Tech Lead / AI Core & Fullstack
- **Kiến trúc Multi-Agent LangGraph:** Thiết kế StateGraph điều phối các Agent chuyên trách (Supervisor, Inventory, Booking, RespondNode).
- **Tích hợp Bản đồ & Định tuyến:** Tích hợp Goong Maps API đo khoảng cách và nhúng Iframe bản đồ chỉ đường trực tiếp vào PropertyCard.
- **Engine Tài chính (`affordability.py`):** Xây dựng thuật toán tính toán dòng tiền trả góp vay mua nhà theo lãi suất và thời hạn vay.
- **Bảo mật & UI/UX:** Xây dựng chốt chặn Demo Password Guard, Mật khẩu ngẫu nhiên OAuth, đồng bộ Brand Identity và thiết kế giao diện Next.js.

---

# 4. KẾT QUẢ ĐO LƯỜNG & KIỂM THỬ THỰC NGHIỆM

### 📊 4.1. Kết quả Batch Evaluation (52 kịch bản / 117 lượt tương tác)
- **Tổng số lượt hỏi thử nghiệm:** 117 lượt.
- **Số lượt lỗi hệ thống (HTTP 500 / Crash):** **0 lượt (0%)**.
- **Độ trễ trung bình (Average Latency):** **~2.1 giây / câu trả lời**.
- **Nhận diện ngoài phạm vi (Fallback Accuracy):** Nhận diện 100% các câu hỏi nằm ngoài phạm vi BĐS hoặc ngoài khu vực (Tokyo, tháp Eiffel, Amazon) và kích hoạt phản hồi từ chối hợp lệ.

### 🧪 4.2. Bộ kiểm thử tự động (Test Suite)
- **Test phân quyền 403 (`tests/test_role_authorization.py`):** Xác nhận 100% trường hợp Customer truy cập trái phép API Sale/Admin đều bị trả về `403 Forbidden`.
- **Test bảo mật OAuth (`tests/test_google_oauth_password.py`):** Xác nhận tài khoản Google OAuth có mật khẩu ngẫu nhiên an toàn, chặn hoàn toàn hình thức đoán mật khẩu `gauth_<email>`.
- **Test Demo Password Guard (`tests/test_demo_password_guard.py`):** Xác nhận mật khẩu demo bị vô hiệu hóa hoàn toàn trên môi trường `production` và `staging`.
- **Test hành vi Mem0 (`tests/test_mem0_service.py`):** Kiểm tra hành vi đẩy dữ liệu Redis và thiết lập TTL hết hạn.

---

# 5. ĐỐI CHIẾU XỬ LÝ 6 PHẢN HỒI CỦA MENTOR

| Issue | Vấn đề Mentor chỉ ra | Hiện trạng giải quyết | Minh chứng trong Code |
| :--- | :--- | :---: | :--- |
| **Issue 1** | Schema cũ mâu thuẫn, MOCKUI chết, đường dẫn hardcode Windows | 🟢 **ĐÃ XONG 90%** | Đã xóa `database/mvp/`, xóa `README_boilerplate.md`, không còn `MOCKUI/`, `README.md` đã chuyển sang đường dẫn tương đối. |
| **Issue 2** | Thiếu test service lớn, không có test từ chối quyền 403, test mem0 lấy lệ | 🟢 **ĐÃ XONG 85%** | Đã viết `test_role_authorization.py` (test 403), viết lại `test_mem0_service.py` thành test hành vi thực tế, thêm `test_booking_service.py`. |
| **Issue 3** | Token Calendar plaintext, rò `str(e)` ra client, `/docs` mở ở production | 🟢 **ĐÃ XONG 80%** | `src/main.py` đã tắt Swagger Docs ở production; `auth.py` và `sale.py` đã dùng `logger.exception()` giấu lỗi SQL. *(Còn phần mã hóa at-rest cho calendar token sẽ xử lý ở Phase tới).* |
| **Issue 4** | Lỗi ruff thiếu import `Path` trong `src/main.py` làm crash auto-seed | 🟢 **ĐÃ XONG 100%** | `src/main.py:7` đã import `from pathlib import Path`, khởi động auto-seed trơn tru. |
| **Issue 5** | `verify_password` nhận mật khẩu demo ở mọi môi trường | 🟢 **ĐÃ XONG 100%** | `auth_service.py:26` đã chặn `if settings.app_env != "development": return False` và có test kiểm thử đa môi trường. |
| **Issue 6** | Tài khoản Google OAuth có mật khẩu đoán được `gauth_{email}` | 🟢 **ĐÃ XONG 100%** | `google_oauth.py:167` đổi sang sinh ngẫu nhiên bằng `secrets.token_urlsafe(32)` và có test hồi quy xác minh. |

---

# 6. KỊCH BẢN THUYẾT TRÌNH BẢO VỆ 5 PHÚT (DEMO DAY PITCH)

### ⏱️ PHÚT 1: Mở đầu & Nêu bài toán thực tế (Vũ Thế Lực trình bày)
> *"Kính thưa Hội đồng và các Mentor, em là **Vũ Thế Lực** – đại diện nhóm P-046 mang đến sản phẩm **Nera – Trợ lý AI Bất động sản và Đặt lịch xem nhà O2O**.*  
>  
> *Trong thị trường BĐS hiện nay, việc dẫn khách đi xem nhà mẫu đang gặp 3 nỗi đau lớn:*  
> 1. *Khách hàng bị 'ngợp' giữa hàng ngàn tin đăng rời rạc và mất tiêu chí mỗi lần tìm lại.*  
> 2. *Điều phối lịch xem nhà thủ công qua tin nhắn dẫn tới tình trạng **trùng lịch (double-booking)** giữa các Sale.*  
> 3. *Đa số Chatbot trên thị trường chỉ trả lời chung chung hoặc bị ảo giác (hallucination).*  
>  
> *Nera ra đời để giải quyết triệt để bài toán này bằng mô hình **Multi-Agent kết hợp Grounding dữ liệu thật và cơ chế Human-in-the-loop**."*

---

### ⏱️ PHÚT 2 - 3: Giải pháp kiến trúc & Demo trực tiếp (Phạm Trung Kiên trình bày / demo)
> *"Hệ thống của chúng em đang chạy thực tế tại địa chỉ `nerahome.space` với kiến trúc 3 lớp:*  
> 1. *Giao diện Next.js App Router mượt mà.*  
> 2. *Hệ thống Multi-Agent trên LangGraph phân tách rõ vai trò: **Supervisor** giữ ngữ cảnh, **Inventory Agent** lọc nhà theo ràng buộc cứng, và **Booking Agent** quản lý lịch trống.*  
> 3. *Cơ sở dữ liệu PostgreSQL chứa hơn 1.000 tin crawl thật và Redis quản lý bộ nhớ Mem0.*  
>  
> *(Thực hiện Demo trực tiếp):*  
> - *Khách chat: 'Tìm căn 2PN ở Cầu Giấy dưới 3 tỷ, đi xe đến ĐH Quốc Gia dưới 10 phút'.*  
> - *AI tóm tắt lại tiêu chí -> Gọi Goong Maps đo khoảng cách thật -> Trả về thẻ nhà có thật trong DB kèm bản đồ Iframe.*  
> - *Khách chọn đặt lịch xem lúc 9:00 sáng -> Hệ thống tạo bản ghi **giữ chỗ 15 phút (PropertyHold)**.*  
> - *Chuyển sang màn hình `/sale` của nhân viên: Sale nhận thông báo, bấm **Duyệt** -> Lịch hẹn chính thức được xác nhận."*

---

### ⏱️ PHÚT 4 - 5: Tính kỷ luật sản phẩm, Đánh giá & Tương lai (Vũ Thế Lực kết luận)
> *"Điểm cốt lõi làm nên sự khác biệt của Nera từ góc nhìn **AI Product** chính là **Sự trung thực và Tính kiên cường của hệ thống** (Resilience):*  
> - *AI không bao giờ tự ý chốt lịch ảo: Con người (Sale) luôn là người phê duyệt cuối cùng (HITL).*  
> - *Hệ thống có cơ chế Fallback minh bạch: Nếu Redis sập, tự động chuyển sang In-memory; nếu LLM gặp sự cố, hệ thống chuyển sang Fallback theo luật và thông báo rõ cho người dùng.*  
> - *Nhóm đã vượt qua bộ 117 câu hỏi kiểm thử kịch bản với độ trễ trung bình ~2.1s và 0 lỗi hệ thống.*  
>  
> *Về kế hoạch phát triển tiếp theo, nhóm sẽ nâng cấp mã hóa Token lịch at-rest và tích hợp engine tính toán tài chính chuyên sâu.*  
> *Xin cảm ơn Hội đồng và rất mong nhận được những câu hỏi góp ý từ các Mentor!"*

---

# 7. BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN (DEFENSE Q&A)

#### ❓ Câu 1: *"Tại sao không để AI tự động chốt lịch luôn cho khách mà phải bắt Sale duyệt (HITL) cho mất công?"*
> **Trả lời (Góc nhìn PM):**  
> *"Dạ thưa Mentor, trong BĐS O2O, việc đi xem nhà phát sinh chi phí thực tế (thời gian di chuyển của Sale, mở cửa căn hộ, xe đưa đón). Nếu để AI tự chốt, chỉ cần khách spam hoặc AI hiểu nhầm sẽ gây lãng phí nguồn lực rất lớn. Giữ chỗ 15 phút và để Sale duyệt là điểm cân bằng hoàn hảo: vừa giải phóng 80% thời gian tư vấn ban đầu cho Sale, vừa giữ trách nhiệm pháp lý và kiểm soát thực tế thuộc về con người."*

#### ❓ Câu 2: *"Làm sao bạn đảm bảo AI không bịa ra giá nhà hoặc địa chỉ ảo (Hallucination)?"*
> **Trả lời (Góc nhìn AI Product):**  
> *"Dạ, nhóm áp dụng kiến trúc **SQL Grounding**. LLM không có quyền tự sinh dữ liệu BĐS. LLM chỉ đóng vai trò trích xuất tiêu chí (Entity Extraction) để Backend query trực tiếp vào PostgreSQL. Mọi câu trả lời đều gắn nhãn `llm_grounded` lấy từ DB thực tế. Nếu không có nhà thỏa mãn hoặc thiếu dữ liệu, hệ thống bắt buộc AI thông báo không tìm thấy thay vì suy đoán."*

#### ❓ Câu 3: *"Nếu API của OpenAI bị timeout hoặc Redis bị sập thì sản phẩm của bạn có chết không?"*
> **Trả lời (Góc nhìn Kỹ thuật & Resilience):**  
> *"Dạ không. Nhóm đã thiết kế sẵn **2 tầng Fallback**:*  
> 1. *Với Redis: Hệ thống có cơ chế In-memory fallback tự động chuyển sang lưu tạm trong RAM của tiến trình.*  
> 2. *Với LLM: Hệ thống bắt exception và kích hoạt Rule-based Fallback, đồng thời UI hiển thị rõ nhãn 'Fallback theo luật' để người dùng không bị gián đoạn trải nghiệm."*

#### ❓ Câu 4: *"Sự khác biệt lớn nhất giữa việc tìm kiếm bằng Nera so với gõ bộ lọc trên Batdongsan.com.vn là gì?"*
> **Trả lời (Góc nhìn UX & AI Value):**  
> *"Bộ lọc truyền thống chỉ hiểu các tiêu chí cứng và bắt người dùng nhập lại từ đầu. Nera hiểu được các **nhu cầu mềm kết hợp ngữ cảnh đa lượt** (ví dụ: 'tìm căn vừa tiền cho vợ chồng mới cưới, gần viện Bạch Mai để tiện đi làm'). Khách có thể đổi tiêu chí từng bước mà không cần chọn lại từ đầu nhờ lớp Memory đa tầng của hệ thống."*

---

# 8. KẾ HOẠCH HÀNH ĐỘNG TIẾP THEO (NEXT STEPS)

- **P0 — Bắt buộc xử lý ngay:**
  - Bổ sung mã hóa đối xứng AES/Fernet cho `calendar_refresh_token` trong `SaleProfile`.
- **P1 — Hoàn thiện chất lượng:**
  - Geocode và chuẩn hóa lại tọa độ Lat/Long cho toàn bộ tin crawl để tăng độ phủ tìm kiếm bản đồ.
  - Mở rộng bộ kiểm thử tự động cho `redis_service.py` và các tình huống giữ chỗ 15 phút.
- **P2 — Mở rộng tính năng:**
  - Hỗ trợ khung giờ xem nhà linh hoạt theo lịch làm việc thực tế của từng nhân viên Sale.
  - Tích hợp công cụ tính toán khả năng chi trả tài chính chuyên dụng.
