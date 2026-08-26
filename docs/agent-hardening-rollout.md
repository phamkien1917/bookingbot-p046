# Kế hoạch hoàn thiện agent và triển khai

Không thể liệt kê hữu hạn “toàn bộ câu người dùng có thể hỏi”. Mục tiêu có thể kiểm chứng là bao phủ theo taxonomy, sinh biến thể tự động, đo lỗi trên log thật và bắt buộc agent từ chối suy đoán khi thiếu bằng chứng.

## Taxonomy bắt buộc

1. Tìm kiếm: mua/thuê, vị trí, vùng, loại BĐS, giá, phòng, diện tích, tầng, hướng, pháp lý, nội thất, số lượng.
2. Địa lý: cách địa danh bao nhiêu km/phút; đi bộ, ô tô, xe máy, xe đạp, công cộng; gần trường, bệnh viện, đại học, siêu thị, công viên.
3. Tham chiếu nhiều lượt: căn này/căn đó, số thứ tự, chọn rồi so sánh, đổi một tiêu chí, tìm thêm nhưng loại kết quả cũ.
4. Booking: guest → login → tiếp tục, chọn ngày/slot, trùng lịch, hết slot, kiểm tra, hủy, dời lịch, sale nhận/từ chối/reassign.
5. Tư vấn: quy trình, pháp lý, tài chính. Dữ liệu thời gian thực như lãi suất phải có nguồn/ngày hoặc trả lời chưa thể xác minh.
6. An toàn: prompt injection, UUID giả, session người khác, spam/rate limit, PII, XSS trong listing, provider/Redis/DB lỗi.

## Gate chất lượng

- Hard-filter precision: 100% trên transaction, budget, location, kind, legal, orientation, floor.
- Booking side-effect accuracy: 100%; không tạo/hủy/dời ngoài intent đã xác nhận.
- Multi-turn reference accuracy: >= 98% trên eval cố định.
- Geo evidence coverage: 100% kết quả có số km/phút phải có provider; 0 số được suy đoán.
- Hallucinated inventory facts: 0 trong eval và sampled production logs.
- P95 chat không Geo <= 4 giây; Geo <= 7 giây; error rate < 1%.

## Triển khai

1. CI: Ruff, pytest, frontend lint/build, migration safety test và eval deterministic là required checks.
2. Staging: clone schema, dùng dữ liệu đã ẩn danh; chạy toàn bộ `eval/chat_scenarios.json`, booking smoke và kiểm tra tọa độ theo tỉnh.
3. Cấu hình: secret JWT riêng >= 32 ký tự, SMTP, Google Maps APIs với key hạn chế theo API/IP, budget alert và quota.
4. Shadow 24 giờ: luồng mới chạy song song không trả cho user; so intent, criteria, property IDs và latency với production.
5. Canary: 5% → 25% → 50% → 100%, mỗi nấc tối thiểu 2 giờ. Tự rollback khi error > 2%, hard-filter violation > 0 hoặc P95 tăng > 30%.
6. Sau phát hành: lưu feedback có taxonomy, triage hằng ngày tuần đầu; mỗi lỗi production phải thành test hồi quy trước khi đóng.

## Việc còn phải làm trước 100% traffic

- Làm sạch/geocode lại dữ liệu hiện có; tọa độ sai tỉnh sẽ bị Geo Service loại nên có thể giảm coverage.
- Bổ sung nguồn tin cho thuê; code đã ngăn trộn sale/rent nhưng database hiện gần như chỉ có tin bán.
- Chuyển HITL case khỏi bộ nhớ process sang bảng PostgreSQL + admin queue. Assignment thực tế hiện do booking domain service xử lý; agent thử nghiệm cũ không nên được nối vào production vì sẽ phân công trùng.
- Thêm telemetry theo `intent`, `response_kind`, provider, latency, empty-result reason và filter violations; không ghi raw PII.
