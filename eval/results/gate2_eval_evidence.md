# Gate 2 — Eval Evidence

> 5 test case chạy tay qua endpoint thật `POST /api/v1/chat`, LLM thật (không mock), thực hiện 15/08/2026.

## Cấu hình khi test

Backend là branch `develop`, chạy local qua `uvicorn src.main:app`, PostgreSQL + Redis lên qua Docker Compose. LLM dùng OpenRouter (`https://openrouter.ai/api/v1`), model `nvidia/nemotron-3-ultra-550b-a55b:free`. Toàn bộ request LLM trong phiên test đều trả `HTTP/1.1 200 OK` từ đúng domain OpenRouter — kiểm tra kỹ vì hệ thống có một nhánh fallback rule-based khá khéo, có thể trả lời hợp lý ngay cả khi LLM chết hoàn toàn, nên chỉ tin response text thôi là chưa đủ bằng chứng.

Gọi endpoint bằng `curl -X POST http://127.0.0.1:8000/api/v1/chat -d '{"message": "..."}'`, mỗi case dùng một `X-Session-Id` riêng để không lẫn ngữ cảnh.

## Kết quả

**Case 1 — tìm nhà (SEARCH_PROPERTY).** Hỏi *"Tôi muốn tìm căn hộ 2 phòng ngủ ở quận 7, giá dưới 4 tỷ"*, agent trả về *"Rất tiếc, hiện tại không có bất động sản nào phù hợp với tiêu chí của bạn. Bạn có muốn thay đổi điều kiện tìm kiếm không?"*, kèm phần trích xuất tiêu chí `{"max_price": 4000000000, "min_bedrooms": 2, "district": "Quận 7", "property_kind": "APARTMENT"}` — đúng cả 4 field. Truy vấn PostgreSQL chạy thật (`SELECT ... WHERE district ILIKE 'Quận 7' AND ...`) và quả thật không có bản ghi khớp trong dữ liệu crawl hiện có, nên câu trả lời "không có kết quả" là trung thực chứ không phải agent lười tìm. Đạt.

**Case 2 — đặt lịch xem nhà (BOOK_APPOINTMENT).** Hỏi *"Tôi muốn đặt lịch xem nhà vào cuối tuần này"* — chưa nói rõ căn nào — agent hỏi ngược lại *"Bạn muốn đặt lịch xem căn nào? Vui lòng chọn một bất động sản trước."* thay vì tự tạo một booking rỗng cho có. Đây đúng là hành vi mong muốn khi thiếu field bắt buộc.

**Case 3 — câu hỏi ngoài phạm vi (GENERAL_QA).** Hỏi *"Mua nhà cần chuẩn bị giấy tờ gì"* — một câu hỏi pháp lý mà hệ thống không có dữ liệu nguồn để trả lời chắc chắn. Agent từ chối và điều hướng: *"Câu hỏi của bạn tôi không trả lời được. Bạn vui lòng hỏi trực tiếp Sale khi đi xem nhà nhé."* Đây là case quan trọng nhất trong 5 case, vì nó chứng minh agent thà từ chối còn hơn bịa thông tin pháp lý sai. Điểm trừ nhỏ: phần đuôi câu trả lời tự động chèn thêm lời mời "giữ căn và đặt lịch xem nhà" dù ngữ cảnh chẳng liên quan gì đến một căn cụ thể — không sai nhưng hơi cứng, đáng sửa sau Gate 2.

**Case 4 — kiểm tra trạng thái booking (CHECK_STATUS).** Hỏi *"Lịch xem nhà của tôi đang ở trạng thái nào rồi"*, agent không đoán mò mà hỏi lại mã booking hoặc số điện thoại đã đăng ký — hợp lý vì session chưa gắn với danh tính cụ thể nào.

**Case 5 — chào hỏi (GREETING).** Hỏi đơn giản *"Chào bạn"*, agent chào lại đúng vai và liệt kê đúng 4 năng lực nó thực sự có (tìm nhà, đặt lịch, kiểm tra booking, trả lời câu hỏi BĐS) — không hứa hẹn tính năng không tồn tại.

## Tổng kết

5/5 case chạy end-to-end với LLM thật, có log xác nhận model + status code, không có case nào rơi vào fallback. Không phát hiện trường hợp nào bịa property, giá, hay trạng thái không có nguồn.

Một điều đáng ghi lại cho ai đọc báo cáo này sau: trước khi tìm ra cấu hình key đúng, hệ thống đã được thử với 2 key hỏng (OpenAI hết credit, và một proxy lạ trả 403), và trong cả hai trường hợp response trên API vẫn "trông như đúng" nhờ fallback rule-based. Nếu chỉ nhìn response text mà không mở log server, rất dễ nhầm rằng LLM đang hoạt động trong khi thực ra nó đã chết hoàn toàn. Khi demo hoặc audit lại hệ thống này, luôn đối chiếu với log (tên model + status code từ đúng domain provider), đừng chỉ tin vào câu trả lời hiển thị.
