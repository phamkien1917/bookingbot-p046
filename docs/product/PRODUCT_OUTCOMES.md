# Product Outcomes

## Outcome chain

Người dùng chia sẻ nhu cầu và feedback
→ AI hình thành memory đáng tin cậy
→ đề xuất và so sánh ngày càng phù hợp hơn
→ người dùng không phải bắt đầu lại
→ người dùng quay lại và tiến gần hơn đến quyết định.

## Desired Outcome

Giúp người tìm nhà tiếp tục hành trình ở đúng điểm đã dừng, nhanh chóng thu hẹp lựa chọn và tự tin hơn khi quyết định.

## Business Outcome

Giữ người dùng quay lại và tiếp tục hành trình tìm nhà.

Trong MVP, đây là giả thuyết cần kiểm chứng, chưa phải kết quả kinh doanh đã đạt.

## Product Outcome

Người dùng quay lại phiên thứ hai và tiếp tục bằng hồ sơ, lịch sử, shortlist và feedback đã có mà không phải nhập lại từ đầu.

## North Star Metric

**Second-session Resume Rate**

Tỷ lệ người dùng quay lại phiên thứ hai và tiếp tục hành trình bằng dữ liệu đã có mà không phải bắt đầu lại.

Đề xuất cách ghi nhận trong test:

`Số người hoàn tất hành động resume hợp lệ ở Session 2 / Số người đã hoàn thành Session 1`

Một resume hợp lệ cần có recap từ dữ liệu trước, không hỏi lại không cần thiết và ít nhất một hành động tiếp tục như xem recommendation, compare hoặc feedback.

## Supporting metrics

| Metric | Ý nghĩa | Mục tiêu/Trạng thái |
|---|---|---|
| Profile Completion Rate | Tỷ lệ hồ sơ đạt đủ thông tin tối thiểu để đề xuất | Cần thiết lập baseline |
| Time to First Value | Thời gian từ câu đầu tiên đến khi người dùng thấy AI hiểu đúng hoặc nhận gợi ý hữu ích | Cần thiết lập baseline |
| Second-session Return Rate | Tỷ lệ người test quay lại Session 2 | Mục tiêu >= 50% |
| Resume Success Rate | Tỷ lệ Session 2 tiếp tục đúng hành trình | Cần thiết lập baseline |
| Repeat-question Rate | Mức độ AI hỏi lại dữ liệu đã biết | AI không hỏi lại đúng >= 90% |
| Feedback Rate | Tỷ lệ phiên có ít nhất một feedback | Mục tiêu >= 70% |
| Shortlist Creation Rate | Tỷ lệ phiên tạo được shortlist | Mục tiêu >= 60% |
| Recommendation Acceptance | Tỷ lệ recommendation nhận SAVE/LIKE hoặc được đưa vào compare | Cần thiết lập baseline |
| Explanation Coverage | Recommendation có giải thích | 100% |
| Property Source Coverage | Dữ kiện căn hộ có nguồn | 100% |
| Hallucination Rate | Tỷ lệ bịa giá, địa chỉ hoặc trạng thái | 0 |

## Test hypotheses

Mọi giả thuyết dưới đây đang ở trạng thái **chưa kiểm chứng** trừ khi có báo cáo test được liên kết sau này.

| ID | Giả thuyết | Cách kiểm thử tối thiểu | Tín hiệu ủng hộ |
|---|---|---|---|
| H1 | Hội thoại tự nhiên giúp người dùng mô tả nhu cầu dễ hơn form cố định | Quan sát người dùng hoàn thành Session 1 | Người dùng tạo được profile mà không cần hướng dẫn ngoài sản phẩm |
| H2 | Profile hiển thị trực tiếp làm tăng niềm tin vào khả năng hiểu của AI | Usability test với và không che phần profile | Người dùng xác nhận hoặc sửa profile thành công |
| H3 | Câu hỏi làm rõ theo ngữ cảnh giúp giảm câu hỏi thừa | Kiểm tra transcript Session 1 | AI phát hiện trường thiếu >= 90% và không hỏi lại >= 90% |
| H4 | Giải thích và trade-off giúp người dùng thu hẹp lựa chọn | Quan sát feedback và shortlist | Recommendation có giải thích 100%; shortlist >= 60% phiên test |
| H5 | Ghi lại lý do reject giúp đề xuất lần sau phù hợp hơn | So sánh Session 1 và Session 2 | Recommendation mới phản ánh lý do đã reject |
| H6 | Recap và resume làm người dùng cảm nhận rõ giá trị khác biệt của AI | Phỏng vấn sau Session 2 | Người dùng nhận ra AI nhớ đúng và không phải bắt đầu lại |
| H7 | Giới hạn tối đa 3 recommendation làm giảm quá tải thông tin | Quan sát thời gian và khả năng so sánh | Người dùng có thể giải thích lựa chọn hoặc trade-off giữa các căn |

## Quy tắc báo cáo

- Không ghi “đã đạt” nếu chưa có bằng chứng test.
- Tách metric hệ thống, metric usability và nhận xét định tính.
- Báo cáo cả thất bại, dữ liệu thiếu và số mẫu test.
- Các mục tiêu MVP không được trình bày như cam kết kinh doanh.
