# Development Journal — Team P-046 (Nera)

> **Deliverable #8 — Ban Tổ Chức AI20K Build Phase (Cohort 3)**  
> **Dự án:** Nera — AI Real Estate & O2O Booking Platform  
> **Nhóm phát triển:** Vũ Thế Lực (PM & AI Product Lead) · Phạm Trung Kiên (Tech Lead & AI Core Engineer)  

---

## 📅 Tuần 4: 29/08/2026 – 01/09/2026 (Phase 1 Evaluation & Hardening)

### Mục tiêu tuần này
- [x] Thiết lập hệ thống đo lường token runtime và chi phí thực tế cho mỗi lượt chat
- [x] Đóng kín 3 lỗi nghiêm trọng (SEV-0): Lỗi tool bản đồ, Chống xác nhận giả HITL, Khóa đồng thời chống Double-booking
- [x] Tích hợp bộ 222 kịch bản Golden Scenarios vào pytest CI gate
- [x] Đo lường và lập báo cáo chi phí monetization một trang (Monetization One-Pager)
- [x] Chuẩn hóa toàn bộ 10 Deliverables theo chuẩn yêu cầu BTC AI20K

### Đã hoàn thành
1. **Đo lường Token & Cost Runtime:** Xây dựng `src/services/token_usage.py` trích xuất chính xác token vào/ra và prompt caching từ API provider. Xác định chi phí thực tế: ~13.9 VNĐ/lượt chat, Cost/Job ~5.000 VNĐ cho mỗi lịch hẹn được duyệt.
2. **Kiểm thử Failure Modes (SEV-0):**
   - Viết `test_geo_tool_failure.py`: Khi Goong Maps lỗi, hệ thống không bịa khoảng cách.
   - Viết `test_hitl_no_false_confirmation.py`: Chặn triệt để câu "đã xác nhận" khi Sale chưa duyệt `APPROVED`.
   - Viết `test_property_hold_concurrency.py`: Kiểm chứng cơ chế `pg_advisory_xact_lock` với 2 coroutine đồng thời qua `asyncio.gather()`.
3. **Mở rộng Test Suite:** Nâng tổng số test cases tự động lên **720 tests PASSED 100%** trong 10.71s.
4. **Chiến lược Monetization:** Hoàn thành `docs/research/MONETIZATION_ONE_PAGER.md` với mô hình 300.000đ/seat/tháng dựa trên khảo sát n=20 môi giới CenLand/Đất Xanh/OneHousing.

### Khó khăn & Giải pháp
| Khó khăn | Giải pháp kỹ thuật | Kết quả |
|:---|:---|:---|
| Không đo được chi phí runtime, chỉ có số liệu tính tay | Viết `src/services/token_usage.py` đọc usage từ response của LLM provider và trả về trong state | Đo được chính xác token và chi phí từng lượt: 4.096 token cache, ~13.9 VNĐ/lượt |
| 222 kịch bản test trước đây chỉ chạy qua script HTTP, không tự động trên CI | Viết `tests/test_golden_set.py` chạy replay 82 ca trích xuất criteria và assert integrity trực tiếp trong pytest | Toàn bộ 222 kịch bản được bảo vệ tự động mỗi lần chạy CI |
| Nguy cơ Sale và Khách bị chồng lịch khi bấm cùng lúc | Sử dụng `pg_advisory_xact_lock` trên PostgreSQL kèm bản ghi `PropertyHold` 15 phút | 100% không bị double-booking trong môi trường chịu tải |

### Bài học kinh nghiệm
- **Đo lường trước khi tối ưu:** Nhìn vào số liệu token thực tế mới thấy chi phí nhân sự duyệt lịch (HITL ~2.150 VNĐ) cao gấp đôi chi phí LLM (~1.200 VNĐ). Do đó, điểm mấu chốt để giảm Cost/Job là tối ưu thao tác duyệt 1 chạm của Sale trên mobile.
- **Kỷ luật kiểm thử tự động:** Biến các kịch bản JSON thành test có thể chạy trong CI giúp loại bỏ hoàn toàn tình trạng "code chạy được trên máy cá nhân nhưng gãy trên server".

---

## 📅 Tuần 3: 22/08/2026 – 28/08/2026 (Goong Maps & Guardrails)

### Mục tiêu tuần này
- [x] Xử lý các issue mentor nêu ở buổi review
- [x] Đưa dữ liệu bản đồ thật vào luồng tư vấn (khoảng cách, thời gian đi làm)
- [x] Chạy đo traffic trên môi trường live và xuất báo cáo có số liệu thật
- [x] Tích hợp Langfuse Observability để soi độ trễ từng chặng

### Đã hoàn thành
- Tích hợp Goong Maps: tính khoảng cách và thời gian đi làm từ bất động sản tới nơi khách làm việc, badge trên card, iframe chỉ đường trong khung chat.
- Sửa lỗi mất ngữ cảnh giữa các lượt và lỗi LLM lách guardrail khi khách hỏi ngoài phạm vi. Bộ đo cho thấy chặn được 100% ca thử: hỏi về Tokyo, tháp Eiffel, prompt injection.
- Đóng 6 issue mentor nêu, thêm global exception handler, mã hoá token Google Calendar khi lưu, fallback in-memory cho luồng OAuth khi Redis chết.
- Bổ sung tính toán tài chính: khoản vay theo amortization, kiểm tra trần ngân sách, quick-reply sinh theo ngữ cảnh hội thoại.
- Áp bộ nhận diện Nera lên frontend: logo, favicon, token màu.
- Đo traffic trên API production: 15 kịch bản, 23 lượt, HTTP 200 đạt 100%, không có lỗi 500.

### Khó khăn & Giải pháp
| Khó khăn | Giải pháp | Kết quả |
|:---|:---|:---|
| `pytest` treo 120 giây mỗi lần chạy | Ba script gọi API thật nằm ở thư mục gốc với tiền tố `test_` bị pytest thu gom. Chuyển sang `scripts/manual/check_*.py` | Bộ test chạy còn ~5 giây |
| Không biết 5.27s độ trễ đến từ đâu | Bọc timing `_timed()` ở `build_agent_graph` để mọi node đều được đo, trả về trong `stage_timings` và tích hợp Langfuse | Tách rõ thời gian từng node và vòng gọi bản đồ Goong |
| LLM tự bịa câu trả lời cho câu hỏi ngoài phạm vi | Siết prompt guardrail cho intent `OUT_OF_SCOPE` và chặn trước khi gọi LLM | 100% ca thử bị từ chối an toàn |
| Redis chết làm hỏng luồng đăng nhập Google | Thêm fallback in-memory cho bước trao đổi OAuth | Đăng nhập vẫn chạy khi Redis không sẵn sàng |

### Bài học kinh nghiệm
- Test đặt đúng chỗ mới có giá trị. Test unit cần chạy nhanh và không phụ thuộc mạng; test gọi API bên ngoài phải tách riêng để không làm nghẽn luồng phát triển.
- Con số trong báo cáo phải sinh ra từ phép đo, không gõ tay. Sau khi để script tự ghi verdict theo ngưỡng, báo cáo mới phản ánh đúng trạng thái hệ thống.

---

## 📅 Tuần 2: 15/08/2026 – 21/08/2026 (LangGraph Multi-Agent Core)

### Mục tiêu tuần này
- [x] Chuyển đổi từ monolithic chatbot sang kiến trúc LangGraph Multi-Agent
- [x] Xây dựng CSDL 18 bảng trên PostgreSQL và nạp dữ liệu BĐS thật
- [x] Thiết kế luồng phân quyền 4 vai trò (Customer, Sale, Coordinator, Admin)

### Đã hoàn thành
- Xây dựng LangGraph StateGraph với 4 node chính: Supervisor, Inventory Agent, Booking Agent, Respond Node.
- Xây dựng hệ thống CSDL PostgreSQL hoàn chỉnh với 18 bảng quan hệ và nạp dữ liệu crawled BĐS thật tại Hà Nội.
- Triển khai xác thực JWT qua HttpOnly Cookie và phân quyền RBAC chặt chẽ ở tầng API FastAPI.

---

## 📅 Tuần 1: 08/08/2026 – 14/08/2026 (Khởi động dự án & Phỏng vấn thị trường)

### Mục tiêu tuần này
- [x] Xác định bài toán cốt lõi và chân dung khách hàng mục tiêu
- [x] Khảo sát thực địa 20 môi giới và 30 người tìm nhà tại Hà Nội
- [x] Khởi tạo kiến trúc dự án Next.js 14 + FastAPI + Docker Compose

### Đã hoàn thành
- Phát hiện nỗi đau đứt gãy kép (Dual Friction Funnel): Khách nản vì phải nhập lại form và chờ đợi Sale; Sale quá tải vì 80% thời gian trả lời câu hỏi lặp lại và dễ bị trùng lịch.
- Định vị sản phẩm Nera: Trợ lý AI BĐS hội thoại tự nhiên kết hợp đặt lịch O2O khép kín.
