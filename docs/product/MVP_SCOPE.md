# MVP Scope — AI Home Search Companion

## Nguyên tắc phạm vi

- AI phải nằm ở trung tâm trải nghiệm.
- Người tìm thuê nhà là người dùng chính.
- Ưu tiên một hành trình hai phiên chạy được và chứng minh memory, personalization, explainability và retention.
- Không mở rộng phạm vi chỉ vì tính năng đã xuất hiện trong PRD, Project Brief hoặc mockup cũ.

## MUST HAVE

### AI Conversation

- Nhận yêu cầu tìm nhà bằng ngôn ngữ tự nhiên.
- Trích xuất thông tin đã có trong hội thoại.
- Hiển thị AI đang hiểu gì về người dùng.
- Hỏi làm rõ trường còn thiếu theo ngữ cảnh.
- Phát hiện tiêu chí mâu thuẫn và hỏi người dùng ưu tiên điều gì.

### Profile và AI Memory

- Lưu và hiển thị nhu cầu hiện tại, must-have, ưu tiên và tiêu chí linh hoạt.
- Cho phép người dùng xác nhận, sửa hoặc xóa memory.
- Ghi nhớ thay đổi tiêu chí qua các phiên.
- Không hỏi lại thông tin đã biết nếu chưa có dấu hiệu thay đổi.

### Recommendation và Explainability

- Đề xuất tối đa 3 căn sau khi có đủ điều kiện tối thiểu.
- Giải thích lý do phù hợp, điểm chưa phù hợp, trade-off và dữ liệu còn thiếu.
- Chỉ hiển thị dữ kiện căn hộ có nguồn; không tạo dữ kiện giả.

### Feedback, Shortlist và Compare

- Hỗ trợ LIKE, DISLIKE, SAVE và REJECT.
- Ghi nhận lý do feedback.
- Cho phép tạo shortlist.
- So sánh các căn trong shortlist theo hồ sơ cá nhân.
- Có AI summary về khác biệt và trade-off.

### Journey History và Resume

- Hiển thị căn đã xem, đã lưu, đã loại và lý do.
- Tóm tắt phiên trước khi người dùng quay lại.
- Tiếp tục từ điểm đã dừng bằng hồ sơ, lịch sử và feedback đã có.
- Đề xuất mới phải phản ánh điều AI học được từ feedback trước đó.

## SHOULD HAVE

Các nội dung này hỗ trợ MVP nhưng không được chặn happy path cốt lõi:

- profile progress trong màn hình hội thoại;
- quick actions cho các hành động thường dùng;
- property card hiển thị ngay trong hội thoại;
- lịch sử thay đổi tiêu chí trong Profile/Memory;
- nhãn nguồn và thời điểm xác minh của dữ kiện căn hộ;
- trạng thái rõ ràng khi dữ liệu thiếu hoặc chưa thể đề xuất;
- nút “Tôi muốn xem căn này” chỉ để ghi nhận yêu cầu ở trạng thái Pending.

## FUTURE SCOPE

Chỉ xem xét khi MVP đã được kiểm chứng và có quyết định phạm vi mới:

- stakeholder workflow dành cho sale;
- quy trình xử lý yêu cầu xem nhà sau trạng thái Pending;
- booking và xác nhận lịch hoàn chỉnh;
- đồng bộ Google Calendar;
- CRM integration;
- thông báo SMS, Zalo hoặc Push;
- dashboard vận hành và báo cáo nâng cao;
- native mobile app;
- AI pricing, AI analytics, tư vấn đầu tư, pháp lý hoặc tín dụng.

## DEPRECATED / OLD DIRECTION

Không dùng các nội dung sau để định nghĩa hoặc ưu tiên MVP hiện tại:

- định vị sản phẩm là “trợ lý đặt lịch xem nhà và giữ căn”;
- lấy sale hoặc admin làm người dùng trung tâm;
- lấy số lượng booking, tỷ lệ nhận lịch hoặc hiệu suất sale làm outcome chính;
- soft hold, countdown giữ căn và tự động xác nhận booking;
- tự động phân công sale hoặc tối ưu lộ trình TSP;
- Sale Dashboard hoặc Admin Booking Dashboard phức tạp;
- Multi-Agent, Microservices hoặc Event-Driven Architecture như giá trị sản phẩm;
- xây một portal bất động sản nhiều chức năng rồi gắn chatbot vào.

Các tài liệu và mockup chứa hướng cũ được giữ nguyên làm bằng chứng lịch sử; không bị xóa hoặc tự động chuyển thành backlog.
