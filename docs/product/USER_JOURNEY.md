# User Journey — Hai phiên tìm nhà

## Persona và bối cảnh mẫu

Người dùng đang tìm thuê nhà cho gia đình ba người, ngân sách khoảng 18 triệu đồng/tháng, làm việc tại Cầu Giấy và dự kiến chuyển trong 1–3 tháng.

## Session 1 — Lần đầu tìm nhà

### Mục tiêu phiên

Giúp người dùng diễn đạt nhu cầu, hình thành hồ sơ tìm nhà, nhận lựa chọn đầu tiên và để lại feedback có thể dùng cho lần sau.

| Bước | Hành động của người dùng | Vai trò của AI | Kết quả người dùng nhìn thấy |
|---|---|---|---|
| 1. Bắt đầu hội thoại | Mô tả nhu cầu bằng ngôn ngữ tự nhiên | Nhận diện ý định tìm thuê và trích xuất thông tin đã có | Câu trả lời xác nhận ngắn và phần “AI đang hiểu gì về bạn” |
| 2. Hình thành profile | Kiểm tra các thông tin AI đã hiểu | Biến hội thoại thành ngân sách, số người, vị trí làm việc và các tiêu chí có cấu trúc | Profile progress và các trường đã biết/chưa biết |
| 3. Làm rõ | Trả lời câu hỏi về số phòng, commute, trường học hoặc tiêu chí quan trọng | Chỉ hỏi thông tin còn thiếu; phát hiện tiêu chí mâu thuẫn và trade-off | Hồ sơ rõ hơn mà không phải điền form dài |
| 4. Xác nhận nhu cầu | Xác nhận hoặc chỉnh sửa profile | Tóm tắt hard constraints, ưu tiên và tiêu chí linh hoạt | Bản tóm tắt có thể chỉnh sửa |
| 5. Nhận recommendation | Xem tối đa 3 căn | Đề xuất và giải thích tiêu chí đạt, chưa đạt, trade-off và dữ liệu thiếu | Danh sách ngắn, không phải duyệt quá nhiều tin |
| 6. Phản hồi | Save căn A; reject căn B vì bếp nhỏ; reject căn C vì đi làm xa | Ghi nhận hành động và lý do; xác nhận điều đã học được | Feedback state rõ ràng và shortlist được cập nhật |
| 7. Kết thúc phiên | Dừng hành trình sau khi đã có shortlist hoặc feedback | Lưu profile, lịch sử, feedback, shortlist và điểm đang dừng | Thông báo rằng hành trình có thể tiếp tục ở lần sau |

### Giá trị cần chứng minh

- AI hiểu được câu đầu tiên.
- AI hỏi làm rõ có chọn lọc.
- Recommendation có lý do và trade-off.
- Feedback được ghi nhận kèm lý do.
- Người dùng kết thúc phiên với memory và/hoặc shortlist có ý nghĩa.

## Session 2 — Người dùng quay lại và tiếp tục

### Mục tiêu phiên

Chứng minh rằng sản phẩm nhớ đúng ngữ cảnh và giúp người dùng tiến xa hơn mà không phải bắt đầu lại.

| Bước | Hành động của người dùng | Vai trò của AI | Kết quả người dùng nhìn thấy |
|---|---|---|---|
| 1. Quay lại | Mở lại sản phẩm | Nhận diện hành trình đang có và lấy đúng điểm tiếp tục | Lời chào cá nhân hóa và nút “Tiếp tục từ đây” |
| 2. Recap | Đọc và xác nhận tóm tắt | Nhắc lại ngân sách, nhu cầu, ưu tiên, shortlist và các lý do đã loại | Recap ngắn, có thể sửa nếu nhu cầu thay đổi |
| 3. Áp dụng memory | Không phải nhập lại dữ liệu đã biết | Dùng profile, lịch sử và feedback đã lưu | Repeat-question được giảm; profile vẫn hiển thị minh bạch |
| 4. Recommendation tốt hơn | Xem các lựa chọn mới | Ưu tiên căn có bếp phù hợp hơn và commute ngắn hơn theo feedback trước | Tối đa 3 đề xuất mới với giải thích “đã thay đổi vì sao” |
| 5. So sánh | So sánh căn mới với shortlist cũ | Tóm tắt khác biệt và trade-off theo ưu tiên cá nhân | Bảng compare và AI summary |
| 6. Tiếp tục feedback | Save, reject hoặc thay đổi ưu tiên | Cập nhật memory và xác nhận ảnh hưởng của feedback | Shortlist và profile phản ánh quyết định mới |
| 7. Tiến gần quyết định | Thu hẹp shortlist hoặc bày tỏ muốn xem một căn | Giúp tóm tắt lựa chọn; nếu cần chỉ ghi nhận yêu cầu xem nhà Pending | Người dùng biết bước tiếp theo nhưng không bị kéo vào booking phức tạp |

### Giá trị cần chứng minh

- Memory tồn tại qua phiên.
- AI không hỏi lại dữ liệu đã biết.
- Recap đúng và có thể chỉnh sửa.
- Recommendation mới phản ánh feedback cũ.
- Người dùng có thể tiếp tục, so sánh và thu hẹp lựa chọn.

## Điểm thất bại cần quan sát

- AI recap sai hoặc dùng memory của sai người dùng/hành trình.
- AI hỏi lại thông tin đã biết mà không có lý do.
- Recommendation không thay đổi sau feedback.
- UI không cho biết điều gì đã được ghi nhớ.
- Người dùng không hiểu vì sao một căn được đề xuất.
- Người dùng không thể sửa memory hoặc lý do feedback.
