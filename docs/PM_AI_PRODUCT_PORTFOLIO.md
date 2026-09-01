# BÁO CÁO MINH CHỨNG TOÀN DIỆN ĐÓNG GÓP CỦA PM & AI PRODUCT LEAD (VŨ THẾ LỰC)
**Dự án:** Nera — AI Real Estate & O2O Booking Platform (P-046 / 046LTD)  
**Nhân sự đảm nhiệm:** **Vũ Thế Lực**  
**Vai trò:** **Product Manager & AI Product Lead**  
**Bản chạy thực tế (Live URL):** [https://www.nerahome.space/](https://www.nerahome.space/)  
**Mã nguồn Repository:** [AI20K-Build-Phase-Cohort-3/P-046](https://github.com/AI20K-Build-Phase-Cohort-3/P-046)  

---

## 📌 TỔNG QUAN PHẠM VI CÔNG VIỆC ĐẢM NHIỆM

Trong dự án Nera, **Vũ Thế Lực** đảm nhiệm vai trò kép **Product Manager & AI Product Lead**, trực tiếp tham gia từ nghiên cứu thị trường, xây dựng bài toán kinh doanh, thiết kế và lập trình các cấu phần AI/Backend cốt lõi, thu thập và chuẩn hóa dữ liệu, đến xây dựng bộ kiểm thử chất lượng AI (Eval Suite) và chuẩn bị hồ sơ thuyết trình Demo Day.

```
                              VŨ THẾ LỰC (PM & AI PRODUCT LEAD)
                                              │
    ┌─────────────────┬───────────────────────┼───────────────────────┬─────────────────┐
    ▼                 ▼                       ▼                       ▼                 ▼
[DATA & PIPELINE] [AI & BACKEND CODE]    [EVAL & TESTING]     [PRODUCT & RESEARCH] [DEMO DAY & GTM]
• 3.796 BĐS thật  • Token Tracker        • 720 tests pass     • Field Survey n=20  • Pitch Deck PDF
• Normalization   • Stage Timings        • 3 tests SEV-0      • Product Brief/PRD  • 5-min Script
• Freshness Stamp • Finance Extraction   • 222 Golden Cases   • Monetization 300k  • Video Demo
• Noise Cleaners  • Guardrails & Safety  • Eval Audit Master  • Cost/Job 5.000đ    • 10 Deliverables
```

---

## 🛠️ KHỐI 1: KỸ THUẬT DỮ LIỆU & CRAWL PIPELINE (DATA ENGINEERING)

Trực tiếp thu thập, kiểm duyệt và chuẩn hóa kho dữ liệu thực tế hơn **3.700 căn hộ trên 27 tỉnh thành** (thay vì 167 căn chỉ ở Hà Nội của đề bài ban đầu), phục vụ việc truy vấn SQL Grounding chính xác cho Agent:

1. **Thu thập dữ liệu BĐS thực tế:**
   - Xây dựng pipeline trích xuất dữ liệu từ các sàn BĐS uy tín: [`database/crawler_batdongsan.py`](file:///d:/AITHUCCHIEN/P-046/database/crawler_batdongsan.py), xuất bản file CSDL [`004_crawled_data.sql`](file:///d:/AITHUCCHIEN/P-046/004_crawled_data.sql) (3.796 bản ghi thật).
   - Thiết lập script phân tích chất lượng dữ liệu: [`scripts/audit_crawled_data.py`](file:///d:/AITHUCCHIEN/P-046/scripts/audit_crawled_data.py).
2. **Bộ chuẩn hóa và làm sạch dữ liệu BĐS (Data Normalization & Cleaning):**
   - **Chuẩn hóa địa lý 27 tỉnh thành:** [`010_province_normalization.sql`](file:///d:/AITHUCCHIEN/P-046/010_province_normalization.sql) và `src/services/search_criteria_service.py`.
   - **Xác thực độ tươi mới tin đăng:** Xây dựng [`src/utils/freshness.py`](file:///d:/AITHUCCHIEN/P-046/src/utils/freshness.py) đóng dấu `last_verified_at` và loại bỏ tin hết hạn.
   - **Bộ lọc nhiễu tiêu đề & mô tả:** Xây dựng [`src/utils/property_text.py`](file:///d:/AITHUCCHIEN/P-046/src/utils/property_text.py) để:
     - Lọc bỏ các đoạn chào mời của môi giới ("Liên hệ ngay e Lan...", "Chính chủ gửi bán...").
     - Ẩn số điện thoại nguồn để bảo vệ quyền riêng tư và tránh khách liên hệ tắt ngoài hệ thống.
     - Chuẩn hóa viết hoa tiêu đề BĐS, giữ nguyên các từ viết tắt chuyên ngành (BĐS, Căn hộ, CC, TT).
     - Sanity Band: Thiết lập ngưỡng trần/sàn loại bỏ giá ảo (ví dụ căn hộ 2 tỷ nhưng tin đăng ghi 2 triệu để câu view).
3. **Kiểm thử tự động cho Data Pipeline:**
   - Viết [`tests/test_crawl_pipeline.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_crawl_pipeline.py) gồm **40 test cases** kiểm tra toàn bộ pipeline làm sạch dữ liệu.

---

## 💻 KHỐI 2: LẬP TRÌNH AI MULTI-AGENT & BACKEND SERVICES (ENGINEERING)

Trực tiếp viết mã nguồn cho các module AI Agent, đo lường hệ thống, logic tài chính và bảo mật hạ tầng:

1. **Hệ thống Đo lường Token & Chi phí Runtime (Token & Cost Instrumentation):**
   - Viết trọn vẹn module [`src/services/token_usage.py`](file:///d:/AITHUCCHIEN/P-046/src/services/token_usage.py) bóc tách chính xác `input_tokens`, `output_tokens`, `cached_input_tokens`, `llm_calls` từ API response của OpenAI/OpenRouter.
   - Mở rộng schema [`src/models/schemas.py`](file:///d:/AITHUCCHIEN/P-046/src/models/schemas.py) để gắn số liệu token trực tiếp vào từng response trả về cho client.
2. **Hệ thống Đo lường Thời gian từng Node (Stage Timings):**
   - Viết decorator `_timed()` trong [`src/agents/graph.py`](file:///d:/AITHUCCHIEN/P-046/src/agents/graph.py) đo chính xác mili-giây thực thi của từng node (`supervisor`, `inventory`, `booking`, `respond`), trả về trong trường `stage_timings`.
   - Viết bộ test kiểm chứng độ chính xác: [`tests/test_stage_timings.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_stage_timings.py).
3. **Tích hợp Giám sát Chuyên sâu Langfuse Tracing:**
   - Xây dựng helper `_trace_callbacks()` có cache trong [`src/agents/graph.py`](file:///d:/AITHUCCHIEN/P-046/src/agents/graph.py).
   - Gắn `langfuse_session_id` và `langfuse_user_id` gom toàn bộ phiên hội thoại vào cây span lồng nhau.
   - Tách riêng thời gian gọi bên thứ ba (Goong Maps) khỏi thời gian gọi LLM.
   - Soạn thảo tài liệu hướng dẫn demo đo độ trễ: [`docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md`](file:///d:/AITHUCCHIEN/P-046/docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md).
4. **Bóc tách Ý định Tài chính & Tư vấn Vay mua (Financial Extraction):**
   - Viết hàm `_extract_finance()` và regex tài chính trong [`src/agents/nodes/supervisor.py`](file:///d:/AITHUCCHIEN/P-046/src/agents/nodes/supervisor.py) để phân biệt rõ giữa "thu nhập 40 triệu/tháng" và "ngân sách mua nhà 40 tỷ".
   - Viết bộ test hồi quy: [`tests/test_supervisor_finance_extract.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_supervisor_finance_extract.py).
5. **Guardrails & An toàn Agent (AI Safety & Discipline):**
   - Thiết kế cơ chế từ chối an toàn khi người dùng hỏi ngoài phạm vi (Tokyo, Tháp Eiffel, Prompt injection), không tốn token gọi LLM ngoài lề.
   - Nhận diện thuật ngữ Cho Thuê và xử lý trung thực kho hàng rỗng: [`tests/test_rental_honesty.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_rental_honesty.py).
   - Cơ chế Fallback 2 tầng: Fallback sang Rule-based khi LLM lỗi ([`tests/test_llm_structured_fallback.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_llm_structured_fallback.py)), và tự động chuyển model provider ([`tests/test_llm_model_selection.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_llm_model_selection.py)).
6. **Bảo mật & Hạ tầng:**
   - Bổ sung **Global Exception Handler** trong [`src/main.py`](file:///d:/AITHUCCHIEN/P-046/src/main.py) ngăn chặn rò rỉ lỗi SQL stack trace ra bên ngoài.
   - Thiết lập chốt chặn **Demo Password Guard** trong [`src/services/auth_service.py`](file:///d:/AITHUCCHIEN/P-046/src/services/auth_service.py) chặn mật khẩu demo khi `APP_ENV != development`.
   - Sửa lỗi crash UTF-8 console stream logging trên hệ điều hành Windows.

---

## 🧪 KHỐI 3: KIỂM THỬ TỰ ĐỘNG & BỘ ĐÁNH GIÁ CHẤT LƯỢNG AI (AI EVALUATION)

Xây dựng bộ kiểm thử chất lượng AI toàn diện, đưa số lượng test tự động lên **720 tests PASSED 100%**:

1. **Bộ 3 Kiểm thử Đóng kín Failure Modes Nghiêm trọng (SEV-0 Tests):**
   - [`tests/test_geo_tool_failure.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_geo_tool_failure.py): Mô phỏng Goong Maps timeout/lỗi ➔ Agent thừa nhận chưa xác minh khoảng cách, tuyệt đối không tự bịa km.
   - [`tests/test_hitl_no_false_confirmation.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_hitl_no_false_confirmation.py): Khi Sale chưa duyệt (`status != APPROVED`), câu trả lời tuyệt đối không chứa từ "đã xác nhận".
   - [`tests/test_property_hold_concurrency.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_property_hold_concurrency.py): Mô phỏng 2 coroutine tranh cùng slot xem nhà qua `asyncio.gather()` ➔ Cơ chế PostgreSQL Advisory Lock bảo vệ 100% không bị double-booking.
2. **Tích hợp 222 Kịch bản Golden Set vào Pytest CI Gate:**
   - Viết [`tests/test_golden_set.py`](file:///d:/AITHUCCHIEN/P-046/tests/test_golden_set.py): Tự động hóa việc kiểm tra tính toàn vẹn của 222 kịch bản JSON (`chat_agent_acceptance.json`, `chat_scenarios.json`, `chat_agent_multiturn_extended.json`) và replay 82 ca bóc tách tiêu chí mà không tốn chi phí gọi LLM.
3. **Báo cáo Đánh giá AI Toàn diện (Evaluation Evidence Deliverable #10):**
   - [`docs/evaluation/NERA_EVALUATION_AUDIT.md`](file:///d:/AITHUCCHIEN/P-046/docs/evaluation/NERA_EVALUATION_AUDIT.md): Báo cáo audit chuyên sâu chỉ ra các điểm lệch giữa giả định và thực tế code, phân loại test pyramid và trajectory 6 nodes.
   - [`docs/evaluation.md`](file:///d:/AITHUCCHIEN/P-046/docs/evaluation.md): Báo cáo tổng hợp số liệu đo lường 720 tests, độ bao phủ coverage, bảng chất lượng SQL Grounding, độ trễ P95 và chi phí runtime.

---

## 📈 KHỐI 4: NGHIÊN CỨU THỊ TRƯỜNG, ĐỊNH VỊ SẢN PHẨM & MONETIZATION

Xây dựng toàn bộ nền tảng định vị sản phẩm và chiến lược kinh doanh thực chiến:

1. **Khảo sát thực địa & Nghiên cứu người dùng (Field Research):**
   - [`docs/research/FIELD_RESEARCH_SYNTHESIS.md`](file:///d:/AITHUCCHIEN/P-046/docs/research/FIELD_RESEARCH_SYNTHESIS.md): Chủ trì khảo sát thực tế n=20 môi giới/quản lý sàn (CenLand, Đất Xanh Miền Bắc, OneHousing) và n=30 người tìm nhà tại Hà Nội.
   - [`docs/research/FIELD_SURVEY.md`](file:///d:/AITHUCCHIEN/P-046/docs/research/FIELD_SURVEY.md), [`INTERVIEW_GUIDE.md`](file:///d:/AITHUCCHIEN/P-046/docs/research/INTERVIEW_GUIDE.md): Soạn thảo bảng câu hỏi và khung phỏng vấn chuẩn hóa.
   - Phát hiện bài toán **Nỗi đau đứt gãy kép (Dual Friction Funnel)**: Khách nản vì phải nhập lại form và chờ đợi Sale; Sale mất 80% thời gian trả lời tin nhắn lặp lại và chịu rủi ro trùng lịch 15-20%.
2. **Chiến lược Định giá & Kinh tế Đơn vị (Monetization One-Pager — Day 28):**
   - [`docs/research/MONETIZATION_ONE_PAGER.md`](file:///d:/AITHUCCHIEN/P-046/docs/research/MONETIZATION_ONE_PAGER.md):
     - Xác định Value Metric: **Seat** (300.000đ/tài khoản/tháng) dựa trên sự đồng thuận của 85% môi giới được phỏng vấn.
     - Tính toán chi phí đơn vị **Cost/Job ~5.000 VNĐ** cho mỗi lịch hẹn được duyệt (LLM 1.200đ + Phút duyệt của Sale 2.150đ + Infra 1.500đ).
     - Tỷ lệ Gross Margin đạt **70%**.
     - Neo giá vào thiệt hại thực tế: *"Trả 300k/tháng để không mất 8 triệu một lần vì trùng lịch"*.
     - Kế hoạch GTM 90 ngày (90-Day Plan): 2 sàn pilot tháng đầu ➔ Xuất bản Pilot Report ➔ 3 sàn trả tiền (~60 seats).
   - [`docs/research/COST_MODEL.md`](file:///d:/AITHUCCHIEN/P-046/docs/research/COST_MODEL.md): Xây dựng mô hình tính toán chi phí token và hạ tầng.
3. **Định nghĩa Sản phẩm (PRD & Scope):**
   - [`docs/product/PRODUCT_BRIEF.md`](file:///d:/AITHUCCHIEN/P-046/docs/product/PRODUCT_BRIEF.md): Định vị Nera là *AI Home Search Companion*.
   - [`docs/product/MVP_SCOPE.md`](file:///d:/AITHUCCHIEN/P-046/docs/product/MVP_SCOPE.md), [`USER_JOURNEY.md`](file:///d:/AITHUCCHIEN/P-046/docs/product/USER_JOURNEY.md): Xác định phạm vi tính năng MVP và luồng trải nghiệm người dùng.

---

## 🎤 KHỐI 5: THUYẾT TRÌNH DEMO DAY, SLIDE DECK & HỒ SƠ 10 DELIVERABLES

Chuẩn bị toàn bộ hồ sơ trình bày và tài liệu bàn giao theo quy chuẩn Ban Tổ Chức:

1. **Bộ Slide Thuyết trình & Kịch bản Nói Demo Day:**
   - [`docs/pitch-deck.pdf`](file:///d:/AITHUCCHIEN/P-046/docs/pitch-deck.pdf) & [`presentation/pitch_deck.pdf`](file:///d:/AITHUCCHIEN/P-046/presentation/pitch_deck.pdf): Xuất bản file PDF slide thuyết trình chuẩn 10 slide.
   - [`docs/SLIDE_THUYET_TRINH_NERA_DEMO_DAY.md`](file:///d:/AITHUCCHIEN/P-046/docs/SLIDE_THUYET_TRINH_NERA_DEMO_DAY.md): Kịch bản thuyết minh chi tiết phân bổ từng giây cho Vũ Thế Lực (PM) và Phạm Trung Kiên (Tech Lead) trong 5 phút thuyết trình + 3 phút Q&A.
2. **Kịch bản Video Demo (Deliverable #6):**
   - [`docs/video-demo.md`](file:///d:/AITHUCCHIEN/P-046/docs/video-demo.md): Kịch bản quay video 4 phút 45 giây thể hiện trọn vẹn luồng khách tìm nhà, lọc Goong Maps, giữ chỗ 15 phút, Sale duyệt HITL và Langfuse tracing.
3. **Bộ Nhận diện Thương hiệu & Tài sản Hình ảnh (Brand Assets):**
   - Thiết kế OpenGraph banner và thumbnail Demo Day: [`frontend/public/og/nera-og.png`](file:///d:/AITHUCCHIEN/P-046/frontend/public/og/nera-og.png), `docs/demo/assets/`.
4. **Nhật ký Phát triển & Báo cáo Công việc (Deliverables #8 & #9):**
   - [`docs/journal.md`](file:///d:/AITHUCCHIEN/P-046/docs/journal.md): Nhật ký 4 tuần phát triển ghi lại mục tiêu, kết quả, khó khăn, giải pháp và bài học kinh nghiệm.
   - [`docs/worklog.md`](file:///d:/AITHUCCHIEN/P-046/docs/worklog.md): Bảng lịch sử commit và công việc chi tiết theo từng ngày từ 24/08 đến 01/09/2026.
5. **Chuẩn hóa README Chuẩn Vàng (Deliverable #2):**
   - Cập nhật [`README.md`](file:///d:/AITHUCCHIEN/P-046/README.md) đầy đủ ảnh minh họa, bảng 10 deliverables, cây thư mục, bảng API và tài khoản demo.

---

## 📑 BẢNG ÁNH XẠ CÁC COMMIT CHÍNH CỦA VŨ THẾ LỰC (GIT EVIDENCE)

| Mã Commit | Loại hình | Mô tả chi tiết phần việc đã thực hiện |
|:---|:---:|:---|
| `7dd3c79` | **Docs** | Chuẩn hóa toàn bộ cấu trúc 10 Deliverables theo chuẩn BTC |
| `c640ea3` | **Docs** | Xuất bản file PDF slide thuyết trình `docs/pitch-deck.pdf` (Deliverable #7) |
| `0644230` | **Fix** | Đồng bộ thumbnail Demo Day và OpenGraph card banner |
| `a93eff8` | **Docs/Research** | Hoàn thành tài liệu Monetization One-Pager (Day 28) |
| `dbeff92` | **Feat/Eval** | Xây dựng `token_usage.py`, viết 3 tests SEV-0 và tích hợp 222 Golden Scenarios |
| `c9dbe24` | **Feat/SEO** | Bổ sung thẻ OpenGraph và Twitter card metadata |
| `26d3335` | **Style** | Sửa biến linter ruff trên nhánh develop |
| `faf2b61` | **Feat/UI** | Hiển thị tiến trình từng bước của Agent thay vì ghi đè 1 dòng |
| `09a6054` | **Fix/Booking** | Chặn lỗi tự động đặt lịch vào năm sau khi khách gõ ngày trong quá khứ |
| `a910dff` | **Fix/Booking** | Giải phóng slot phase, bảo vệ không đặt giờ khách không yêu cầu |
| `aaa3c7b` | **Feat/Data** | Thu thập và chuẩn hóa dữ liệu 3.662 căn hộ toàn quốc, đóng dấu độ tươi mới |
| `3f75947` | **Feat/Data** | Xác thực độ tươi mới tin đăng và tối ưu hiển thị kết quả bản đồ |
| `3cabf63` | **Docs/Research** | Xây dựng mô hình chi phí Cost Model và tài liệu nghiên cứu thị trường |
| `f9d363f` | **Docs** | Soạn thảo kịch bản thuyết trình Demo Day và tài liệu nguồn NotebookLM |
| `69334c5` | **Docs/Research** | Xây dựng khung khảo sát thực địa, công cụ phỏng vấn và tổng hợp kết quả n=20 |
| `c2be737` | **Fix/AI** | Siết chặt regex tài chính trong Supervisor Agent, tránh nhận nhầm chữ "tìm kiếm" |
| `20a7a39` | **Docs** | Soạn thảo kịch bản demo đo độ trễ bằng Langfuse và cập nhật worklog |
| `5ff7bfc` | **Fix/AI** | Sửa lỗi Supervisor đọc nhầm thu nhập hàng tháng thành giá mua BĐS |
| `bdcae50` | **Feat/Observability**| Hoàn thiện tích hợp Langfuse Tracing chạy thật, gom session và user tracking |
| `57d4c3a` | **Fix/HITL** | Xử lý điều hướng trong HITL Node khi tiếp tục phiên làm việc cũ |
| `ddc591c` | **Fix/LLM** | Thiết lập cơ chế Model Fallback cho các lời gọi Structured Outputs |
| `b3c6472` | **Fix/Chat** | Lưu giữ danh sách căn đã chọn (Shortlist) và hồ sơ HITL qua nhiều lượt |
| `1ccf9a3` | **Feat/AI** | Xây dựng `_timed()` đo thời gian từng node trong LangGraph Graph |
| `06acfd8` | **Test** | Viết bộ kiểm thử cho các luồng tạo và hủy lịch hẹn |
| `6d9c03d` | **Fix/Geo** | Chuẩn hóa trích xuất lộ trình và nhãn dịch vụ Goong Maps |
| `8e04698` | **Docs/Security** | Thêm Global Exception Handler giấu lỗi CSDL, đồng bộ số liệu kiến trúc |
| `5b2eedd` | **Fix/Search** | Nhận diện thuật ngữ Cho Thuê và xử lý kho rỗng trung thực |
| `eed68b9` | **Fix/Data** | Lọc sạch lời chào môi giới và số điện thoại khỏi mô tả tin đăng BĐS |
| `203adad` | **Feat/Chat** | Thêm bước xác nhận những gì Nera đã hiểu trước khi trả về kết quả |
| `e07eeff` | **Feat/Chat** | Trả lời câu hỏi tài chính bằng công thức toán thật và thanh tiến trình |
| `5dcb6c3` | **Docs/Security** | Thiết lập chốt chặn bảo vệ mật khẩu Demo khi chạy Production |
| `1a997d3` | **Docs/Brand** | Thiết kế bộ nhận diện thương hiệu Nera Brand Kit, logo, icons |
| `4fed927` | **Fix/Data** | Lọc sạch các từ khóa quảng cáo marketing khỏi tiêu đề BĐS |

---

## 🏆 TỔNG KẾT

Tất cả các phần việc của **Vũ Thế Lực** ở cả 5 mảng (**Data Engineering**, **AI Multi-Agent & Backend Code**, **AI Evaluation & Testing**, **Market Discovery & Monetization**, và **Demo Pitching**) đều đã được ghi nhận đầy đủ, minh bạch trong repository và sẵn sàng 100% để Ban Tổ Chức AI20K kiểm tra và chấm điểm!
