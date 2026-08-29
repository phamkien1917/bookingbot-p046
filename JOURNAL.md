# Weekly Journal — Team P-046 (Nera)

> Ghi lại mỗi tuần: học được gì, khó khăn gì, quyết định gì, kế hoạch tiếp.

---

## Week: 22/08/2026 - 29/08/2026

### Mục tiêu tuần này
- [x] Xử lý các issue mentor nêu ở buổi review trước
- [x] Đưa dữ liệu bản đồ thật vào luồng tư vấn (khoảng cách, thời gian đi làm)
- [x] Chạy đo traffic trên môi trường live và xuất báo cáo có số liệu thật
- [ ] Kéo độ trễ về ngưỡng release gate

### Đã hoàn thành
- Tích hợp Goong Maps: tính khoảng cách và thời gian đi làm từ bất động sản tới nơi khách làm việc, badge trên card, iframe chỉ đường trong khung chat.
- Sửa lỗi mất ngữ cảnh giữa các lượt và lỗi LLM lách guardrail khi khách hỏi ngoài phạm vi. Bộ đo cho thấy chặn được toàn bộ ca thử: hỏi về Tokyo, tháp Eiffel, prompt injection.
- Đóng 6 issue mentor nêu, thêm global exception handler, mã hoá token Google Calendar khi lưu, fallback in-memory cho luồng OAuth khi Redis chết.
- Bổ sung phần tính toán tài chính: khoản vay theo amortization, kiểm tra trần ngân sách, quick-reply sinh theo ngữ cảnh hội thoại.
- Áp bộ nhận diện Nera lên frontend: logo, favicon, token màu.
- Đo traffic Phase 2 trên API production: 15 kịch bản, 23 lượt, HTTP 200 đạt 100%, không có lỗi 500.
- Dọn repo: chuyển script gọi API thật ra `scripts/manual/`, thêm test cho `create_tour_request` và `cancel_customer_booking`, thêm đo thời gian từng node trong graph. Hiện 170 test chạy trong khoảng 5 giây, ruff sạch trên `src/`, `tests/`, `scripts/`.

### Khó khăn & Giải pháp
| Khó khăn | Giải pháp | Kết quả |
|----------|-----------|---------|
| `pytest` treo 120 giây mỗi lần chạy | Ba script gọi API thật nằm ở thư mục gốc với tiền tố `test_` nên bị pytest thu gom. Chuyển sang `scripts/manual/check_*.py` | Bộ test chạy còn khoảng 5 giây |
| Không biết 5,27s độ trễ đến từ đâu | `ai_latency_ms` chỉ đếm node supervisor. Bọc timing ở `build_agent_graph` để mọi node đều được đo, trả về trong `stage_timings` và gộp vào báo cáo traffic | Lần đo tới sẽ chỉ ra node nào tốn thời gian, thay vì chỉ có con số tổng |
| LLM tự bịa câu trả lời cho câu hỏi ngoài phạm vi | Siết prompt guardrail cho intent `OUT_OF_SCOPE` và chặn trước khi gọi LLM | 100% ca thử bị từ chối an toàn |
| Redis chết làm hỏng luồng đăng nhập Google | Thêm fallback in-memory cho bước trao đổi OAuth | Đăng nhập vẫn chạy khi Redis không sẵn sàng |

### Bài học
- Đo trước khi tối ưu. Nhóm định cắt bớt lời gọi LLM để giảm độ trễ, nhưng chưa có số liệu từng chặng nên không biết cắt chỗ nào. Việc đầu tiên phải là dựng phép đo.
- Test đặt đúng chỗ mới có giá trị. Ba file gọi API thật mang tên `test_` đã âm thầm biến bộ test thành thứ không ai muốn chạy.
- Con số trong báo cáo phải sinh ra từ phép đo, không gõ tay. Sau khi để script tự ghi verdict theo ngưỡng, báo cáo mới phản ánh đúng trạng thái hệ thống.

### Kế hoạch tuần sau
- [ ] Chạy lại bộ đo traffic để lấy thời gian từng node, xác định chặng chiếm nhiều thời gian nhất rồi mới tối ưu
- [ ] Đo lại trên https://www.nerahome.space sau khi backend đã warm, tách phần cold start của Render ra khỏi số liệu độ trễ
- [ ] Bổ sung test cho `redis_service` ở nhánh có Redis thật, không chỉ nhánh fallback
- [ ] Tổng duyệt kịch bản Demo Day trên môi trường live

---

<!-- Copy block trên cho tuần kế tiếp -->
