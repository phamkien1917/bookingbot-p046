# Decision Log

## Mục đích

Ghi lại các quyết định sản phẩm đã có bằng chứng trong repository. File này không suy diễn hoặc gán quyết định cho mentor.

## Trạng thái

- `CONFIRMED`: Được `PROJECT_SOURCE_OF_TRUTH.md` hoặc `AGENTS.md` xác nhận rõ.
- `PROPOSED`: Đề xuất đang chờ quyết định.
- `SUPERSEDED`: Đã được một quyết định mới thay thế.

## Các quyết định đã được xác nhận

| ID | Quyết định | Lý do/Bối cảnh | Nguồn | Trạng thái |
|---|---|---|---|---|
| D-001 | `PROJECT_SOURCE_OF_TRUTH.md` có mức ưu tiên cao hơn PRD, SDS, Project Brief và mockup cũ khi có mâu thuẫn | Repository chứa hai hướng sản phẩm khác nhau | `PROJECT_SOURCE_OF_TRUTH.md`, `AGENTS.md` | CONFIRMED |
| D-002 | Định vị hiện tại là **AI Home Search Companion** | Trọng tâm là đồng hành xuyên suốt hành trình tìm nhà | `PROJECT_SOURCE_OF_TRUTH.md` mục 1 | CONFIRMED |
| D-003 | Người tìm thuê nhà là core user; sale là stakeholder phụ/future | Product cần user-centered thay vì sale-centered | `PROJECT_SOURCE_OF_TRUTH.md` mục 3 | CONFIRMED |
| D-004 | AI phải nằm ở trung tâm trải nghiệm | Không xây portal bất động sản rồi gắn chatbot | `PROJECT_SOURCE_OF_TRUTH.md` mục 1 và 13 | CONFIRMED |
| D-005 | MVP UI chỉ ưu tiên 5 trải nghiệm: Conversation, Profile/Memory, Recommendations, Shortlist/Compare và Journey/Resume | Đây là tập trải nghiệm tối thiểu để chứng minh outcome | `PROJECT_SOURCE_OF_TRUTH.md` mục 13 | CONFIRMED |
| D-006 | Demo chính phải có hai phiên và chứng minh memory, personalization, retention và explainability | Session 2 là nơi giá trị khác biệt của sản phẩm trở nên rõ nhất | `PROJECT_SOURCE_OF_TRUTH.md` mục 12 và 14 | CONFIRMED |
| D-007 | Mỗi tập recommendation chính có tối đa 3 căn và phải có giải thích | Giảm quá tải và giúp người dùng hiểu trade-off | `PROJECT_SOURCE_OF_TRUTH.md` mục 11 và 13 | CONFIRMED |
| D-008 | Feedback MVP gồm LIKE, DISLIKE, SAVE, REJECT và lý do | Feedback là đầu vào cho memory và cá nhân hóa | `PROJECT_SOURCE_OF_TRUTH.md` mục 9 và 12 | CONFIRMED |
| D-009 | Booking trong MVP chỉ là nút “Tôi muốn xem căn này” tạo request Pending | Không xây hệ thống booking phức tạp trong MVP | `PROJECT_SOURCE_OF_TRUTH.md` mục 13 | CONFIRMED |
| D-010 | Không ưu tiên Multi-Agent, Microservices, Event Bus, TSP, complex soft hold, Calendar sync, CRM, multichannel notification hoặc complex Sale Dashboard | Dự án cần một happy path AI rõ ràng trong phạm vi 6 tuần | `PROJECT_SOURCE_OF_TRUTH.md` mục 7 và 19 | CONFIRMED |
| D-011 | AI không được bịa giá, địa chỉ, trạng thái hoặc dữ kiện căn hộ; dữ kiện phải có nguồn | Trust và explainability là điều kiện bắt buộc | `PROJECT_SOURCE_OF_TRUTH.md` mục 6, 15 và 20 | CONFIRMED |
| D-012 | Các success criteria hiện là giả thuyết mục tiêu MVP, không phải kết quả hoặc cam kết kinh doanh đã đạt | Repository chưa có kết quả test xác nhận | `PROJECT_SOURCE_OF_TRUTH.md` mục 15; `eval/results/report.md` đang là template | CONFIRMED |

## Quyết định đang chờ

Chưa có quyết định `PROPOSED` nào được repository ghi nhận tại thời điểm tạo tài liệu. Khi thêm quyết định mới, cần ghi rõ owner quyết định, ngày, lựa chọn được cân nhắc và liên kết bằng chứng.

## Mẫu ghi quyết định mới

| ID | Ngày | Quyết định cần đưa ra | Các lựa chọn | Người quyết định | Bằng chứng | Kết quả/Trạng thái |
|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | PROPOSED |
