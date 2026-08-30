# Gate 2 — Kịch bản quay video demo (3 phút)

> Dựa trên 5 test case đã chạy thật ngày 15/08/2026 (`eval/results/gate2_eval_evidence.md`). Toàn bộ câu hỏi/kỳ vọng dưới đây đã verify chạy đúng — không có gì trong kịch bản này chưa được test trước.

## Chuẩn bị trước khi quay (không tính vào 3 phút)

1. Mở 2 cửa sổ cạnh nhau: **(A)** terminal đang chạy `uvicorn` (để lộ log), **(B)** trình duyệt/Swagger UI (`http://127.0.0.1:8000/docs`) hoặc frontend thật (`http://localhost:3000`) để gõ câu hỏi.
2. Xoá/thu gọn log cũ trong terminal A cho sạch (`clear`), để khi quay chỉ thấy log mới sinh ra.
3. Đảm bảo `.env` có `OPENROUTER_API_KEY` hợp lệ, backend đã restart với key đó.
4. Test thử 1 lần trước khi quay thật (free model có lúc chậm 30–80s do rate limit) để tránh khoảng chết dài trên video.

## Kịch bản theo timeline

### 0:00 – 0:20 — Mở đầu
**Nói:** "Đây là demo agent bất động sản của team, dùng LangGraph multi-agent thật, chạy với LLM thật qua OpenRouter — không phải mock. Em sẽ chứng minh bằng log server song song với câu trả lời trên UI."

**Màn hình:** Cắt nhanh qua 2 cửa sổ A và B để người xem biết cấu trúc video.

### 0:20 – 1:00 — Case 1: Tìm kiếm bất động sản (chứng minh LLM thật + không bịa dữ liệu)
**Gõ ở cửa sổ B:** `Tôi muốn tìm căn hộ 2 phòng ngủ ở quận 7, giá dưới 4 tỷ`

**Trong lúc chờ phản hồi, trỏ chuột vào cửa sổ A**, chỉ vào các dòng log xuất hiện:
```
LLM initialized with model: nvidia/nemotron-3-ultra-550b-a55b:free
HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
```
**Nói:** "Đây — log server cho thấy agent vừa gọi thật tới OpenRouter, model Nemotron, và nhận về 200 OK. Đây không phải câu trả lời dựng sẵn."

**Khi response về, đọc to:** "Rất tiếc, hiện tại không có bất động sản nào phù hợp với tiêu chí của bạn..."

**Nói:** "Agent trích xuất đúng: quận 7, dưới 4 tỷ, 2 phòng ngủ — nhưng dữ liệu crawl thật của tụi em chưa có căn khớp, nên nó nói thật là không có, không bịa ra một căn giả."

### 1:00 – 1:40 — Case 2: Đặt lịch xem nhà (chứng minh xử lý thiếu thông tin)
**Gõ:** `Tôi muốn đặt lịch xem nhà vào cuối tuần này`

**Nói trong lúc chờ:** "Case này test khả năng agent phát hiện thiếu thông tin."

**Khi response về, đọc to:** "Bạn muốn đặt lịch xem căn nào? Vui lòng chọn một bất động sản trước."

**Nói:** "Agent không tự bịa ra một booking rỗng — nó hỏi lại đúng cái còn thiếu trước khi hành động."

### 1:40 – 2:15 — Case 3: Câu hỏi ngoài phạm vi (chứng minh guardrail chống hallucination)
**Gõ:** `Mua nhà cần chuẩn bị giấy tờ gì`

**Khi response về, đọc to (rút gọn):** "...Câu hỏi của bạn tôi không trả lời được. Bạn vui lòng hỏi trực tiếp Sale..."

**Nói:** "Đây là điểm em muốn nhấn mạnh: agent được thiết kế để **từ chối trả lời** câu hỏi pháp lý ngoài phạm vi thay vì bịa thông tin sai — tụi em ưu tiên an toàn hơn là trả lời cho có."

### 2:15 – 2:45 — Case 4 + 5 (chạy nhanh, không cần đọc hết)
**Gõ nhanh 2 câu liên tiếp**, chỉ đọc lướt response:
- `Lịch xem nhà của tôi đang ở trạng thái nào rồi` → hỏi lại mã booking/SĐT
- `Chào bạn` → chào đúng vai, liệt kê đúng năng lực thật

**Nói:** "Cả 5 case tụi em test — tìm nhà, đặt lịch, câu hỏi ngoài phạm vi, check status, và chào hỏi — đều chạy qua LLM thật, có log xác nhận, không có case nào dùng câu trả lời cứng."

### 2:45 – 3:00 — Kết
**Nói:** "Backend là FastAPI + LangGraph multi-agent 6 node, PostgreSQL 24 bảng với dữ liệu crawl thật, toàn bộ đã dựng qua Docker và test end-to-end. Chi tiết kiến trúc và log đầy đủ tụi em để trong `ARCHITECTURE.md` và `eval/results/gate2_eval_evidence.md` trong repo."

**Màn hình:** Cắt nhanh qua `ARCHITECTURE.md` hoặc sơ đồ mermaid render trên GitHub trong 2–3 giây cuối rồi kết thúc.

## Ghi chú quan trọng khi quay

- **Đừng cắt bỏ đoạn chờ LLM phản hồi** (10–80s tuỳ model free) — nếu quá dài, dùng speed-up 2x-4x đoạn chờ thay vì cắt hẳn, để giữ tính "video chưa dựng giả". Yêu cầu Gate 2 không đòi hỏi video liền mạch không cắt, nhưng không nên tạo cảm giác phản hồi tức thì nếu thực tế không phải vậy.
- Nếu 1 case bị timeout/lỗi khi quay thật (free model đôi khi rate-limit), **cứ để lỗi xuất hiện trên video và nói rõ**: "đây là giới hạn của model free tier, agent có cơ chế tự chuyển model khác" — trung thực còn tốt hơn cắt dựng.
- Không cần quay cả 5 case y hệt thứ tự trên nếu thời gian không cho phép — ưu tiên giữ Case 1 (chứng minh LLM thật) và Case 3 (chứng minh không hallucinate), đây là 2 case thuyết phục nhất.
