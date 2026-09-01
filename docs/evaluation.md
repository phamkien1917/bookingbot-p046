# Evaluation Evidence — Nera AI Real Estate Platform (P-046)

> **Deliverable #10 — Ban Tổ Chức AI20K Build Phase (Cohort 3)**  
> **Dự án:** Nera — Trợ lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O  
> **Đội ngũ:** Vũ Thế Lực (PM & AI Product Lead) · Phạm Trung Kiên (Tech Lead)  
> **Môi trường đo lường:** Python 3.13 (`.venv`) · `pytest 9.1.1` · `pytest-cov 7.1.0` · FastAPI / LangGraph  
> **Bản chạy thực tế:** [https://www.nerahome.space/](https://www.nerahome.space/)  

---

## 1. Bảng Tổng hợp Kết quả Kiểm thử (Test Results)

Hệ thống kiểm thử tự động của Nera gồm **720 test cases** chạy tự động qua `pytest`:

```
====================== 720 passed, 2 warnings in 10.71s =======================
```

| Nhóm kiểm thử | File đại diện | Số lượng | Kết quả | Trọng tâm kiểm tra |
|:---|:---|:---:|:---:|:---|
| **Golden Scenarios & Acceptance** | `test_golden_set.py` | **222** | 🟢 100% PASS | Trích xuất tiêu chí single-turn, tính toàn vẹn 150 acceptance cases |
| **Search & Normalization** | `test_search_criteria_service.py`, `test_crawl_pipeline.py` | **65** | 🟢 100% PASS | Bóc tách khoảng giá, quận huyện, số phòng, chuẩn hóa 27 tỉnh thành |
| **Financial Affordability** | `test_affordability.py`, `test_supervisor_finance_extract.py` | **15** | 🟢 100% PASS | Công thức tính lãi suất vay trả góp ngân hàng, nhận diện thu nhập |
| **Booking & Concurrency** | `test_booking_service.py`, `test_property_hold_concurrency.py` | **15** | 🟢 100% PASS | Khóa giữ chỗ 15 phút (`PropertyHold`), chống double-booking đồng thời |
| **Security & Phân quyền** | `test_role_authorization.py`, `test_demo_password_guard.py` | **11** | 🟢 100% PASS | Chặn 401/403 trên endpoint Sale/Admin, bảo vệ mật khẩu Demo |
| **Resilience & Fallback** | `test_redis_service.py`, `test_geo_tool_failure.py` | **15** | 🟢 100% PASS | InMemoryFallback khi Redis sập, thừa nhận khi Goong Maps lỗi |
| **Agent Behavior & HITL** | `test_hitl_no_false_confirmation.py`, `test_rental_honesty.py` | **10** | 🟢 100% PASS | Không nói "đã xác nhận" khi Sale chưa duyệt, trung thực kho thuê |
| **Observability & Token Tracker**| `test_token_usage.py`, `test_stage_timings.py` | **11** | 🟢 100% PASS | Trích xuất token usage từ API provider, đo mili-giây từng node |
| **Các Unit & Flow khác** | `test_geo_service.py`, `test_route_optimizer.py`, ... | **356** | 🟢 100% PASS | Haversine distance, time utilities, JWT encryption, Pydantic validation |
| **TỔNG CỘNG** | **43 file kiểm thử chuyên biệt** | **720** | 🟢 **100% PASS** | **Thời gian thực thi: 10.71 giây** |

---

## 2. Đo lường Code Coverage (pytest-cov)

Chạy đo lường toàn diện qua `pytest tests/ --cov=src --cov-report=term-missing`:

| Nhóm module | Số dòng lệnh (Stmts) | Độ bao phủ (Coverage) | Đánh giá |
|:---|:---:|:---:|:---|
| **Cấu hình & Dữ liệu Models (`src/config.py`, `models.py`)** | 487 | **100%** | Tuyệt đối |
| **Schemas API & DTOs (`src/schemas/*`)** | 197 | **95%** | Rất cao |
| **Tối ưu Lộ trình (`src/services/route_optimizer.py`)** | 85 | **91%** | Rất cao |
| **Trích xuất Tiêu chí Tìm kiếm (`src/services/search_criteria_service.py`)** | 233 | **89%** | Rất cao |
| **Quản lý Trạng thái Hội thoại (`src/services/chat_state_service.py`)** | 95 | **86%** | Rất cao |
| **Tính toán Tài chính Vay mua (`src/services/affordability.py`)** | 143 | **78%** | Tốt |
| **Quy trình Duyệt HITL (`src/services/hitl_service.py`)** | 45 | **78%** | Tốt |
| **Đo lường Token & Chi phí (`src/services/token_usage.py`)** | 88 | **72%** | Tốt |
| **Xác thực & Kết nối DB (`src/services/auth_service.py`, `connection.py`)** | 196 | **67%** | Đạt chuẩn |
| **Router Chat & Gateway (`src/api/routes/__init__.py`, `chat.py`)** | 259 | **65%** | Đạt chuẩn |
| **Toàn bộ Codebase (`src/`)** | **7.657** | **48%** | *(Core services đạt 72-100%, các nhánh query mở rộng đang tiếp tục bổ sung test)* |

---

## 3. Bảng Chỉ số Chất lượng Grounding & RAG

Thay vì RAG tài liệu văn bản thuần túy, Nera là hệ thống **SQL & Geo Grounded RAG** (truy vấn dữ liệu cấu trúc thực tế kết hợp dịch vụ bản đồ):

| Chỉ số chất lượng | Định nghĩa & Tiêu chuẩn kiểm tra | Kết quả đo được | Benchmark | Trạng thái |
|:---|:---|:---:|:---:|:---:|
| **SQL Faithfulness (Độ trung thực)** | 100% thông tin BĐS (giá, số phòng, diện tích, vị trí) lấy từ CSDL 3.796 căn thật, không để LLM tự bịa. | **100%** (`ai_mode=llm_grounded`) | > 95% | 🟢 **PASS** |
| **Out-of-Scope Guardrail Rejection** | Chặn các câu hỏi không liên quan (thời tiết, Tokyo, Tháp Eiffel, prompt injection) trước khi gọi LLM. | **100%** (10/10 ca thử bị từ chối an toàn) | 100% | 🟢 **PASS** |
| **Commute Grounding (Goong Maps)** | Tính toán khoảng cách & thời gian di chuyển bằng Goong Distance Matrix API, có badge và iframe minh chứng. | **100%** các ca lọc khoảng cách | > 90% | 🟢 **PASS** |
| **Context Retention (Trí nhớ ngữ cảnh)** | Kế thừa tiêu chí cũ (quận, loại nhà, ngân sách) khi người dùng đổi diện tích hoặc số phòng ở lượt kế tiếp. | **100%** (82/82 ca golden criteria pass) | > 85% | 🟢 **PASS** |
| **Concurrency Safety** | Không xảy ra tình trạng 2 khách đặt trùng cùng 1 khung giờ xem nhà của 1 căn. | **0% Double-booking** (PostgreSQL Lock) | 0% | 🟢 **PASS** |

---

## 4. Hiệu năng & Tốc độ Phản hồi (Performance Metrics)

Đo lường trực tiếp trên môi trường Live Production ([https://www.nerahome.space/](https://www.nerahome.space/)):

| Endpoint / Hành động | Thời gian phản hồi trung bình | P95 | Tỷ lệ thành công (HTTP 200) | Ghi chú |
|:---|:---:|:---:|:---:|:---|
| **Khóa giữ chỗ xem nhà (`PropertyHold`)** | **0.33s** | **0.45s** | 100% | Giao dịch DB tức thì |
| **Chat Tìm nhà (Khi máy nóng)** | **4.08s** | **5.20s** | 100% | 1 LLM call + Goong Maps |
| **Fast-path Chào hỏi (GREETING)** | **0.04s** | **0.08s** | 100% | Regex thuần, 0 LLM call |
| **Chat Tìm nhà (Tổng thể cả Cold-start)** | **5.80s** | **9.52s** | 100% (23/23) | Gồm cả độ trễ đánh thức Render free tier |
| **Health check (`/health`)** | **12ms** | **25ms** | 100% | Kiểm tra kết nối DB & Redis |

---

## 5. Đo lường Token Runtime & Chi phí Kinh tế (Cost/Job)

Hệ thống được tích hợp `src/services/token_usage.py` để trích xuất trực tiếp lượng token tiêu thụ từ phản hồi của mô hình:

```
[Token Usage Instrumentation]
Input Tokens: 4,294 | Output Tokens: 210 | Cached Input Tokens: 4,096 | LLM Calls: 1
```

- **Tận dụng Prompt Caching:** Hơn 85% context hệ thống được nạp từ cache (4.096 tokens), giúp giảm 50% chi phí gọi LLM.
- **Chi phí mỗi lượt chat:** **~13.9 VNĐ/lượt**.
- **Chi phí một cuộc hội thoại hoàn chỉnh (7 lượt):** **~97 VNĐ**.
- **Chi phí hoàn tất một lịch xem nhà được duyệt (Cost/Job):**

| Hạng mục chi phí | Chi phí (VNĐ) | Giải thích |
|:---|---:|:---|
| **API LLM & Goong Maps** | 1.200 | 5 cuộc hội thoại × 240đ (`gpt-4o-mini` có prompt cache) |
| **Phút duyệt của Sale (HITL)** | **2.150** | 1.5 phút × mức lương Sale 15tr/tháng (~86k/giờ) |
| **Hạ tầng Server & Database** | 1.500 | Phân bổ 1.5tr/tháng cho 1.000 lịch hẹn |
| **Dự phòng Retry** | 240 | +20% API dự phòng hội thoại dài |
| **TỔNG COST/JOB** | **~5.000 VNĐ** | **Tỷ lệ Gross Margin đạt 70% ở mức giá 300.000đ/seat/tháng** |

---

## 6. Minh chứng Kiểm thử 3 Failure Modes Nghiêm trọng (SEV-0)

### SEV-0 #1: Goong Maps gặp sự cố không được tự bịa khoảng cách
- **File kiểm thử:** `tests/test_geo_tool_failure.py`
- **Kịch bản:** Mock `GeoService` ném ngoại lệ `TimeoutError` và `HTTPError`.
- **Kết quả:** Nera trả về phản hồi thừa nhận chưa xác minh được khoảng cách, không chứa bất kỳ con số km hay phút ước lượng giả mạo nào.

### SEV-0 #2: Chống xác nhận ảo khi Sale chưa duyệt (HITL)
- **File kiểm thử:** `tests/test_hitl_no_false_confirmation.py`
- **Kịch bản:** Khách hỏi tình trạng lịch khi bản ghi `ApprovalRequest` đang ở trạng thái `PENDING`.
- **Kết quả:** Câu trả lời khẳng định rõ "yêu cầu đang chờ Sale duyệt" và tuyệt đối **không chứa chuỗi "đã xác nhận"**.

### SEV-0 #3: Chống Double-Booking khi tranh chấp cùng slot
- **File kiểm thử:** `tests/test_property_hold_concurrency.py`
- **Kịch bản:** Sử dụng `asyncio.gather()` bắn 2 request đồng thời đặt cùng 1 khung giờ của 1 BĐS.
- **Kết quả:** Cơ chế `pg_advisory_xact_lock` cho phép đúng 1 request tạo thành công `PropertyHold`, request còn lại nhận thông báo slot đã được giữ chỗ.

---

## 7. Khảo sát Người dùng & Môi giới Thực tế

- **Quy mô khảo sát:** n=20 nhà môi giới / quản lý sàn (CenLand, Đất Xanh Miền Bắc, OneHousing, tự do) và n=30 người tìm nhà tại Hà Nội.
- **Kết quả chính:**
  - **85% (17/20 môi giới)** sẵn sàng trả phí sử dụng nền tảng; mức giá trung vị sẵn sàng chi trả đúng **300.000 VNĐ/seat/tháng**.
  - **85% môi giới** từng gặp sự cố trùng lịch ít nhất 1 lần/quý, với mức thiệt hại tự khai báo từ 2.000.000đ đến 8.000.000đ mỗi lần.
  - Khách tìm nhà đánh giá cao nhất tính năng **nhớ ngữ cảnh không phải nhập lại** (4.6/5.0) và **tính thời gian đi làm thực tế qua bản đồ** (4.8/5.0).
