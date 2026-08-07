# Product Risk Log

## Thang đánh giá

- Khả năng: Thấp / Trung bình / Cao
- Tác động: Thấp / Trung bình / Cao
- Trạng thái: Open / Monitoring / Mitigated / Closed

Không đánh dấu `Mitigated` hoặc `Closed` nếu chưa có bằng chứng.

## Risk register

| ID | Rủi ro | Bằng chứng/Tín hiệu hiện tại | Khả năng | Tác động | Owner theo vai trò | Hành động giảm thiểu | Tín hiệu cần theo dõi | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| R-001 | Scope creep quay lại booking, sale workflow hoặc kiến trúc phức tạp | PRD, Project Brief và phần lớn mock UI vẫn mô tả hướng cũ | Cao | Cao | Product/PM | Dùng `MVP_SCOPE.md` và `SCOPE_STATUS.md` trong mọi buổi planning/review; yêu cầu quyết định rõ cho mọi đề xuất ngoài scope | Backlog xuất hiện soft hold, sale assignment, calendar hoặc dashboard phức tạp | Open |
| R-002 | Xung đột giữa định hướng cũ và mới làm team hiểu sản phẩm khác nhau | `PROJECT_SOURCE_OF_TRUTH.md` đối lập với `Booking_bot_PRD.docx`, `PROJECT BRIEF.pdf` và mockup BookingBot | Cao | Cao | Product/PM + Project Lead | Gắn trạng thái Current/Historical/Deprecated; review Product Brief với toàn team | Thành viên tiếp tục dùng booking KPI hoặc sale persona làm cơ sở quyết định | Open |
| R-003 | UI và khả năng sản phẩm thực tế không khớp | UI hiện là mockup tĩnh hướng booking; chưa có UI cho Memory, Compare và Resume | Cao | Cao | UI/UX + Frontend Coordination | Dùng `SCREEN_REQUIREMENTS.md`, ưu tiên happy path hai phiên và review state trước handoff | UI hứa memory/recommendation/feedback nhưng demo không thể hiện nhất quán | Open |
| R-004 | Giá trị AI không nhìn thấy trong demo/UI | Mockup hiện tại làm nổi bật booking, countdown và sale; profile/memory/explainability chưa có màn hình | Cao | Cao | Product/PM + UI/UX | Đặt “AI hiểu gì”, clarification, reason, trade-off và recap vào các checkpoint demo | Người xem mô tả sản phẩm là website nhà đất có chatbot | Open |
| R-005 | Thiếu user validation | Source of Truth yêu cầu phỏng vấn 5–8 người; repository chưa có interview plan hoặc research findings | Cao | Cao | Product/Research | Lập kế hoạch phỏng vấn, tiêu chí mẫu, script và synthesis; không báo cáo insight trước khi có dữ liệu | Persona/problem dựa chủ yếu vào giả định nội bộ | Open |
| R-006 | Thiếu đồng thuận liên nhóm | Chưa có Decision Log, feedback log hoặc action tracker trước bộ tài liệu này | Trung bình | Cao | Project Lead + Product/PM | Review và xác nhận owner, scope, journey, UI acceptance criteria; ghi lại quyết định | Các nhóm dùng thuật ngữ, scope hoặc success criteria khác nhau | Open |
| R-007 | Source of Truth chưa được bảo toàn trong version history | `.agents/AGENTS.md`, `PROJECT_SOURCE_OF_TRUTH.md` và `CODEX_START_PROMPT.txt` đang untracked tại thời điểm assessment | Cao | Cao | Project Lead / Repository Admin | Xác nhận nội dung và đưa tài liệu governance vào quy trình version control phù hợp | Thành viên khác không nhận được định hướng mới hoặc file bị thất lạc | Open |
| R-008 | Metric bị trình bày như kết quả đã đạt | `eval/results/report.md` chưa có dữ liệu; các con số trong Source of Truth là mục tiêu giả thuyết | Trung bình | Cao | Product/PM | Gắn nhãn target/baseline/result rõ ràng và yêu cầu bằng chứng test | Slide/report nói “đạt 90%” khi chưa có test report | Open |
| R-009 | Demo không chứng minh Session 2 | Chưa có pitch deck, video hoặc demo storyboard trong `presentation/` | Cao | Cao | Demo Lead + Product/PM | Viết storyboard hai phiên, rehearsal và phương án fallback | Demo chủ yếu hiển thị tìm căn/booking trong một phiên | Open |
| R-010 | Tái sử dụng UI cũ làm kéo theo semantics cũ | Design system gắn nhiều component với booking, hold và time slot | Trung bình | Trung bình | UI/UX | Tái sử dụng visual token nhưng đổi component semantics theo `SCREEN_REQUIREMENTS.md` | Tên button/status cũ xuất hiện trong bản thiết kế mới | Open |

## Quy tắc review rủi ro

- Review trước mỗi mentor checkpoint và demo rehearsal.
- Mọi rủi ro Cao/Cao cần owner và hành động cụ thể.
- Chỉ đóng rủi ro khi có output hoặc bằng chứng liên kết được.
- Rủi ro kỹ thuật chỉ được ghi nhận ở đây khi ảnh hưởng đến scope, UI, outcome hoặc demo; hành động triển khai kỹ thuật thuộc owner chuyên môn tương ứng.
