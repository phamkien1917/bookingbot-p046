# Product Alignment Review Checklist

## Mục đích

Giúp team review bộ P0 Product Alignment và ghi nhận rõ nội dung nào được xác nhận, cần sửa hoặc còn câu hỏi. Checklist này không tự tạo phê duyệt.

## Trạng thái

- Trạng thái: Bản nháp, chưa có buổi review được repository ghi nhận
- Facilitator đề xuất: Product/PM
- Người cần tham gia: Project Lead, Product/PM, UI/UX, Frontend Coordinator, Demo Lead
- Mentor: tham gia khi có lịch hoặc feedback cần xác nhận
- Thời lượng đề xuất: 45–60 phút

## Pre-read

- `PROJECT_SOURCE_OF_TRUTH.md`
- `docs/product/PRODUCT_BRIEF.md`
- `docs/product/MVP_SCOPE.md`
- `docs/product/USER_JOURNEY.md`
- `docs/product/PRODUCT_OUTCOMES.md`
- `docs/product/SCOPE_STATUS.md`
- `docs/ui/INFORMATION_ARCHITECTURE.md`
- `docs/ui/SCREEN_REQUIREMENTS.md`
- `docs/management/DECISION_LOG.md`
- `docs/management/RISK_LOG.md`
- `docs/management/ACTION_TRACKER.md`

## 1. Product Brief

- [ ] Core user là người tìm thuê nhà, không phải sale.
- [ ] Problem statement phản ánh vấn đề cần kiểm chứng.
- [ ] Định vị là AI Home Search Companion.
- [ ] Giá trị AI thể hiện understand, clarify, memory, personalize và explain.
- [ ] Desired/Product Outcome thống nhất với Source of Truth.
- [ ] Success criteria được ghi là mục tiêu giả thuyết, không phải kết quả đã đạt.

Quyết định/câu hỏi: `TBD`

## 2. MVP Scope

- [ ] MUST HAVE đủ để chứng minh happy path hai phiên.
- [ ] SHOULD HAVE không chặn MVP cốt lõi.
- [ ] FUTURE không bị đưa ngược vào backlog MVP.
- [ ] Booking chỉ dừng ở Pending request.
- [ ] Booking/Sale/Multi-Agent cũ được đánh dấu đúng trạng thái.
- [ ] Không có feature mới ngoài Source of Truth.

Quyết định/câu hỏi: `TBD`

## 3. User Journey và Outcomes

- [ ] Session 1 chứng minh extraction, clarification, recommendation và feedback.
- [ ] Session 2 chứng minh memory, recap, personalization và resume.
- [ ] Journey kết nối được với North Star Metric.
- [ ] Supporting metrics có cách hiểu thống nhất.
- [ ] Test hypotheses chưa bị trình bày như finding.

Quyết định/câu hỏi: `TBD`

## 4. IA và Screen Requirements

- [ ] IA chỉ có 5 trải nghiệm MVP.
- [ ] AI Conversation là điểm vào chính.
- [ ] Profile/Memory minh bạch và có thể sửa/xóa.
- [ ] Recommendations giới hạn tối đa 3 và có explainability.
- [ ] Shortlist/Compare thể hiện trade-off.
- [ ] Journey/Resume thể hiện đúng điểm đã dừng.
- [ ] Reuse mock UI chỉ giữ pattern phù hợp, không giữ booking semantics.
- [ ] Acceptance criteria có thể dùng cho frontend handoff sau khi được xác nhận.

Quyết định/câu hỏi: `TBD`

## 5. Management readiness

- [ ] Mọi quyết định trong Decision Log có nguồn.
- [ ] Không có mentor feedback bị suy diễn.
- [ ] Risk Cao/Cao có owner cần xác nhận.
- [ ] Action Tracker không đánh dấu hoàn tất khi chỉ mới có bản nháp.
- [ ] Owner theo vai trò được thay bằng tên sau khi team xác nhận.
- [ ] Deadline được thống nhất hoặc tiếp tục để TBD có lý do.
- [ ] Source of Truth và governance files có kế hoạch version control.

Quyết định/câu hỏi: `TBD`

## 6. User validation readiness

- [ ] Đã review `docs/research/RESEARCH_PLAN.md`.
- [ ] Tiêu chí tuyển 5–8 người phù hợp persona.
- [ ] Interview Guide ưu tiên hành vi, không dẫn dắt.
- [ ] Có cách tách observation, interpretation và product implication.
- [ ] Có owner tuyển, phỏng vấn, ghi chú và synthesis.
- [ ] Có quy tắc bảo vệ dữ liệu người tham gia.

Quyết định/câu hỏi: `TBD`

## Output bắt buộc sau buổi review

| Output | Owner | Trạng thái |
|---|---|---|
| Danh sách nội dung được xác nhận | TBD | Chưa có |
| Danh sách thay đổi cần thực hiện | TBD | Chưa có |
| Open questions và người xử lý | TBD | Chưa có |
| Owner/RACI theo tên | TBD | Chưa có |
| Deadline ưu tiên P0 | TBD | Chưa có |
| Decision Log được cập nhật | TBD | Chưa có |
| Mentor feedback được ghi đúng nguồn, nếu có | TBD | Chưa có |

## Sign-off record

| Vai trò | Người xác nhận | Ngày | Kết quả | Ghi chú |
|---|---|---|---|---|
| Project Lead | TBD | TBD | Chưa review | TBD |
| Product/PM | TBD | TBD | Chưa review | TBD |
| UI/UX | TBD | TBD | Chưa review | TBD |
| Frontend Coordinator | TBD | TBD | Chưa review | TBD |
| Demo Lead | TBD | TBD | Chưa review | TBD |

Chỉ cập nhật trạng thái tài liệu thành “được xác nhận” khi có sign-off hoặc bằng chứng quyết định tương đương.
