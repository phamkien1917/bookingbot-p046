# Demo Storyboard — Hai phiên tìm nhà

## Trạng thái

- Trạng thái: Bản nháp narrative, chưa được xác nhận chạy end-to-end
- Nguồn: `PROJECT_SOURCE_OF_TRUTH.md` mục Demo chính
- Thời lượng mục tiêu: 5–7 phút
- Mục tiêu: Chứng minh memory, personalization, retention, explainability và giá trị AI

Storyboard này không khẳng định backend hoặc UI đã hỗ trợ đầy đủ các cảnh.

## Demo promise

> Người dùng mô tả nhu cầu tự nhiên, AI làm rõ và ghi nhớ điều quan trọng, học từ feedback, rồi giúp họ tiếp tục đúng điểm đã dừng với đề xuất tốt hơn ở lần quay lại.

## Nhân vật và dữ liệu mẫu

- Người dùng: Người tìm thuê nhà cho gia đình ba người.
- Ngân sách ban đầu: khoảng 18 triệu đồng/tháng.
- Nơi làm việc: Cầu Giấy.
- Thông tin cần làm rõ: số phòng, commute tối đa, trường học nếu có.
- Property facts: chỉ dùng dữ liệu seed/nguồn đã được team xác minh; storyboard dùng `[Căn A/B/C]` thay cho dữ kiện chưa có.

## Storyboard

| Cảnh | Thời lượng | Người dùng/Hệ thống | Nội dung trên màn hình | Giá trị cần chứng minh |
|---|---:|---|---|---|
| 1. Problem setup | 20–30 giây | Presenter mô tả hành trình tìm nhà kéo dài nhiều ngày | Một câu problem statement; không mở dashboard booking | Pain là continuity và decision overload |
| 2. Session 1 bắt đầu | 30 giây | User: “Tôi muốn thuê nhà khoảng 18 triệu, gia đình 3 người, tôi làm ở Cầu Giấy.” | AI Conversation và panel “AI đang hiểu gì về bạn” cập nhật | Natural conversation + profile extraction |
| 3. Clarification | 30–45 giây | AI hỏi số phòng, commute và trường học khi phù hợp | Trường đã biết/chưa biết; profile progress | AI hỏi đúng phần thiếu, không dùng form cố định |
| 4. Xác nhận profile | 20–30 giây | User xác nhận hoặc chỉnh một tiêu chí | Profile/Memory tách must-have, priority và flexible criteria | Memory minh bạch, có thể kiểm soát |
| 5. Recommendation đầu tiên | 45–60 giây | AI đưa tối đa 3 căn | Mỗi card có source, matched/unmet/unknown và trade-off | Explainable recommendation, không bịa fact |
| 6. Feedback và shortlist | 45 giây | User save `[Căn A]`, reject `[Căn B]` vì bếp nhỏ, reject `[Căn C]` vì đi làm xa | Feedback state, lý do và shortlist được cập nhật | Feedback trở thành memory có ý nghĩa |
| 7. Kết thúc Session 1 | 15–20 giây | User dừng | Journey summary và điểm đang dừng | Hành trình đã được lưu, chưa cần booking |
| 8. Session 2 quay lại | 45–60 giây | User mở lại journey | AI recap nhu cầu, shortlist và lý do đã loại | Retention + resume, không nhập lại từ đầu |
| 9. Cá nhân hóa tốt hơn | 45–60 giây | AI đưa `[Căn D/E]` từ dữ liệu đã xác minh | Giải thích ưu tiên bếp phù hợp hơn và commute ngắn hơn | Feedback cũ ảnh hưởng recommendation mới |
| 10. Compare và kết | 30–45 giây | User so sánh căn mới với `[Căn A]` | Side-by-side compare và AI trade-off summary | Thu hẹp lựa chọn và tự tin hơn |

## Điểm chuyển Session 1 → Session 2

Phải có tín hiệu rõ ràng rằng đây là hai phiên khác nhau, ví dụ:

- kết thúc/đóng Session 1;
- chuyển sang nhãn “Lần quay lại”;
- mở Journey History/Resume;
- recap từ dữ liệu của phiên trước.

Không mô phỏng hai phiên bằng cách chỉ cuộn tiếp một hội thoại liên tục mà không chứng minh persistence.

## Evidence checkpoints

| Claim | Bằng chứng phải nhìn thấy |
|---|---|
| AI hiểu nhu cầu | Profile được trích xuất từ câu tự nhiên |
| AI biết làm rõ | Câu hỏi gắn với trường còn thiếu |
| AI giải thích | Matched/unmet/unknown và trade-off trên recommendation |
| AI ghi nhớ | Recap đúng ở Session 2 |
| AI học từ feedback | Recommendation mới liên hệ trực tiếp lý do reject cũ |
| Người dùng tiến gần quyết định | Shortlist/compare được thu hẹp |

## Không đưa vào demo chính

- soft-hold countdown;
- chọn time slot;
- tự động phân công sale;
- Google Calendar;
- Sale/Admin Dashboard;
- Multi-Agent hoặc sơ đồ kiến trúc phức tạp;
- tuyên bố AI tự xác nhận booking;
- dữ kiện căn hộ không có nguồn.

Nếu cần thể hiện ý định xem nhà, chỉ dùng nút “Tôi muốn xem căn này” và trạng thái `Pending` như một hành động phụ.

## Điều kiện chấp nhận storyboard

- [ ] Team xác nhận narrative đúng Source of Truth.
- [ ] Mỗi cảnh có owner trình bày.
- [ ] Property facts dùng trong demo có nguồn.
- [ ] Có cách chứng minh hai phiên thực sự tách biệt.
- [ ] Không claim chức năng chưa chạy.
- [ ] Có fallback cho mỗi checkpoint quan trọng.

Hiện các điều kiện trên chưa được repository ghi nhận là đã hoàn tất.
