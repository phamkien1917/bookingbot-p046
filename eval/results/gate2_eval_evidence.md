# Gate 2 — Eval Evidence

> 5 test case chạy tay qua endpoint thật `POST /api/v1/chat`, LLM thật (không mock), thực hiện 15/08/2026.

## Cấu hình khi test

- **Backend:** `develop` branch, chạy local qua `uvicorn src.main:app`, PostgreSQL + Redis qua Docker Compose.
- **LLM Provider:** OpenRouter (`https://openrouter.ai/api/v1`), model `nvidia/nemotron-3-ultra-550b-a55b:free` — xác nhận qua log server, toàn bộ request LLM trong phiên test đều trả `HTTP/1.1 200 OK`, không có lần nào rơi vào nhánh fallback rule-based (`All LLM attempts failed` — không xuất hiện trong log của phiên test này).
- **Endpoint:** `POST http://127.0.0.1:8000/api/v1/chat`, body `{"message": "..."}`, header `X-Session-Id` riêng cho mỗi case.

## Kết quả

### Case 1 — Tìm kiếm bất động sản (SEARCH_PROPERTY)
- **Input:** `Tôi muốn tìm căn hộ 2 phòng ngủ ở quận 7, giá dưới 4 tỷ`
- **Output:** `Rất tiếc, hiện tại không có bất động sản nào phù hợp với tiêu chí của bạn. Bạn có muốn thay đổi điều kiện tìm kiếm không?`
- **Structured extraction:** `{"max_price": 4000000000, "min_bedrooms": 2, "district": "Quận 7", "property_kind": "APARTMENT"}`
- **Đánh giá:** Trích xuất tiêu chí đúng 100% từ câu tự nhiên. Agent truy vấn PostgreSQL thật (`SELECT ... FROM properties WHERE district ILIKE 'Quận 7' AND ...`), thật sự không có bản ghi khớp trong dữ liệu crawl hiện có → phản hồi trung thực, không bịa property. **Pass** (đúng hành vi mong đợi, kể cả khi 0 kết quả).

### Case 2 — Đặt lịch xem nhà (BOOK_APPOINTMENT)
- **Input:** `Tôi muốn đặt lịch xem nhà vào cuối tuần này`
- **Output:** `Bạn muốn đặt lịch xem căn nào? Vui lòng chọn một bất động sản trước.`
- **Đánh giá:** Agent nhận đúng ý định đặt lịch nhưng phát hiện thiếu `property_id` (chưa chọn căn) → hỏi lại đúng field còn thiếu thay vì tạo booking rỗng. **Pass.**

### Case 3 — Câu hỏi ngoài phạm vi (GENERAL_QA)
- **Input:** `Mua nhà cần chuẩn bị giấy tờ gì`
- **Output:** `Tôi là BookingBot - TRỢ LÝ ĐẶT LỊCH XEM NHÀ & GIỮ CĂN TỰ ĐỘNG 😊. Câu hỏi của bạn tôi không trả lời được. Bạn vui lòng hỏi trực tiếp Sale khi đi xem nhà nhé. Bạn có muốn tôi giữ căn này và đặt lịch xem nhà không?`
- **Đánh giá:** Đúng theo thiết kế `Intent.GENERAL_QA` ("câu hỏi tổng quát — KHÔNG search DB") — agent từ chối trả lời thay vì bịa thông tin pháp lý, điều hướng sang Sale. **Pass về mặt an toàn/không hallucinate**, nhưng trải nghiệm hơi cứng (luôn chèn câu mời giữ căn dù ngữ cảnh không liên quan) — ghi nhận làm action item.

### Case 4 — Kiểm tra trạng thái booking (CHECK_STATUS)
- **Input:** `Lịch xem nhà của tôi đang ở trạng thái nào rồi`
- **Output:** `Để kiểm tra trạng thái booking, vui lòng cung cấp: Mã booking (VD: BK12345678) hoặc Số điện thoại đã đăng ký. Bạn có thể cung cấp thông tin này không?`
- **Đánh giá:** Đúng hành vi — không tự nhận diện được user nếu chưa có định danh, hỏi lại thông tin cần thiết thay vì đoán. **Pass.**

### Case 5 — Chào hỏi (GREETING)
- **Input:** `Chào bạn`
- **Output:** `Xin chào! 👋 Tôi là BookingBot, trợ lý AI của công ty bất động sản. Tôi có thể giúp bạn: 🔍 Tìm kiếm bất động sản phù hợp · 📅 Đặt lịch xem nhà · 📋 Kiểm tra trạng thái booking · ❓ Trả lời các câu hỏi về bất động sản. Bạn cần tôi hỗ trợ gì hôm nay?`
- **Đánh giá:** Chào đúng vai, liệt kê đúng năng lực thật của hệ thống (không hứa quá khả năng). **Pass.**

## Tổng kết

- **5/5 test case chạy được end-to-end với LLM thật** (OpenRouter, model free `nvidia/nemotron-3-ultra-550b-a55b`), có bằng chứng log server xác nhận (`200 OK`, tên model, không fallback).
- Không phát hiện trường hợp bịa dữ liệu bất động sản/giá/trạng thái không có nguồn.
- Điểm cần cải thiện (không chặn Gate 2, ghi để làm sau): Case 3 luôn chèn câu mời "giữ căn" kể cả khi không liên quan tới property cụ thể — nên tách logic GENERAL_QA khỏi luồng gợi ý giữ căn.
- **Lưu ý quan trọng cho việc báo cáo:** trước khi tìm ra cấu hình đúng, hệ thống có một nhánh fallback rule-based khiến response vẫn trả về hợp lý ngay cả khi LLM thất bại hoàn toàn (xác minh bằng cách cố tình test với key OpenAI hết credit và key sai domain — cả hai đều fail 100% nhưng response vẫn "trông như đúng"). Khi demo/báo cáo, nên trỏ trực tiếp vào server log (model name + `200 OK` từ đúng domain LLM provider) làm bằng chứng, không chỉ dựa vào response text.
