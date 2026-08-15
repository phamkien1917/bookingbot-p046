# Product Brief — AI Home Search Companion

## Trạng thái tài liệu

- Trạng thái: Baseline định hướng sản phẩm hiện tại
- Nguồn chính: `PROJECT_SOURCE_OF_TRUTH.md`
- Tài liệu lịch sử tham khảo: `Booking_bot_PRD.docx`, `PROJECT BRIEF.pdf`
- Nguyên tắc: Nếu có mâu thuẫn, ưu tiên `PROJECT_SOURCE_OF_TRUTH.md`.

## WHO — Người dùng mục tiêu

MVP ưu tiên người trẻ hoặc gia đình trẻ đang tìm **thuê nhà để ở**:

- khoảng 24–35 tuổi;
- sống tại Hà Nội hoặc thành phố lớn;
- dự kiến chuyển nhà trong 1–3 tháng;
- có ngân sách tương đối rõ;
- phải xem và so sánh nhiều tin trong nhiều ngày hoặc nhiều tuần;
- cần cân bằng vị trí, ngân sách, diện tích, số phòng, thời gian đi làm, trường học và tiện ích.

Người tìm nhà là người dùng trung tâm. Sale chỉ là stakeholder phụ hoặc phạm vi tương lai.

## WHAT — Vấn đề của người dùng

Người dùng không thiếu tin bất động sản; họ thiếu một cách liên tục và có hệ thống để tiến gần hơn đến quyết định.

Các khó khăn chính:

- quá tải vì thông tin rời rạc;
- khó nhớ đã xem, lưu hoặc loại căn nào;
- không nhớ lý do đã thích hoặc loại một căn;
- khó nhận biết tiêu chí nào thật sự quan trọng;
- khó so sánh các lựa chọn và trade-off;
- mỗi lần quay lại gần như phải bắt đầu từ đầu;
- dễ bỏ cuộc hoặc quyết định theo cảm tính.

## HOW — Cách sản phẩm giải quyết

Sản phẩm dùng hội thoại AI làm điểm bắt đầu và trung tâm trải nghiệm:

1. Hiểu yêu cầu bằng ngôn ngữ tự nhiên.
2. Trích xuất nhu cầu thành hồ sơ có cấu trúc.
3. Hỏi làm rõ những thông tin còn thiếu hoặc mâu thuẫn.
4. Đề xuất tối đa 3 căn phù hợp và giải thích lý do.
5. Ghi nhận like, dislike, save, reject và lý do.
6. Ghi nhớ hồ sơ, lịch sử và feedback qua nhiều phiên.
7. Hỗ trợ shortlist, so sánh và diễn giải trade-off.
8. Khi người dùng quay lại, tóm tắt phiên trước và tiếp tục đúng điểm đã dừng.

## Định vị sản phẩm

**AI Home Search Companion** — trợ lý AI đồng hành cùng người dùng trong hành trình tìm nhà, thay vì một website đăng tin bất động sản có gắn thêm chatbot hoặc một hệ thống tự động hóa booking cho sale.

## Giá trị khác biệt của AI

AI tạo giá trị khi:

- hiểu nhu cầu diễn đạt tự nhiên thay vì bắt người dùng điền form cố định;
- biết câu hỏi làm rõ nào cần hỏi tiếp theo;
- phát hiện xung đột và trade-off giữa các tiêu chí;
- ghi nhớ điều người dùng đã nói, đã xem và đã phản hồi;
- cá nhân hóa đề xuất ở lần tiếp theo;
- giải thích tiêu chí đạt, chưa đạt và chưa có dữ liệu;
- không bịa giá, địa chỉ, trạng thái hoặc dữ kiện căn hộ.

## Desired Outcome

Giúp người tìm nhà tiếp tục hành trình ở đúng điểm đã dừng, nhanh chóng thu hẹp lựa chọn và tự tin hơn khi quyết định.

## Product Outcome

Người dùng quay lại phiên thứ hai và tiếp tục tìm nhà bằng hồ sơ, lịch sử và feedback đã có mà không phải nhập lại từ đầu.

## MVP Success Criteria

| Tiêu chí | Mục tiêu MVP |
|---|---:|
| AI trích xuất đúng thông tin | >= 90% |
| AI phát hiện đúng trường còn thiếu | >= 90% |
| AI không hỏi lại dữ liệu đã biết | >= 90% |
| Hồ sơ được người dùng xác nhận đúng | >= 90% |
| Recommendation có giải thích | 100% |
| Dữ liệu căn hộ có nguồn | 100% |
| AI bịa giá, địa chỉ hoặc trạng thái | 0 |
| Phiên test có ít nhất một feedback | >= 70% |
| Phiên test tạo được shortlist | >= 60% |
| Người dùng test quay lại Session 2 | >= 50% |

Các con số trên là giả thuyết mục tiêu MVP, chưa phải cam kết kinh doanh và chưa được repository chứng minh là đã đạt.
