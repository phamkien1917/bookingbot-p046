# Scope Status — Phân loại tài liệu và UI hiện có

## Quy tắc phân loại

| Trạng thái | Ý nghĩa |
|---|---|
| CURRENT | Đang đại diện cho định hướng sản phẩm hiện tại |
| REUSABLE | Có thể tái sử dụng một phần sau khi đổi ngữ cảnh/nội dung |
| HISTORICAL | Được giữ làm bằng chứng cho hướng cũ; không dùng để quyết định MVP |
| FUTURE | Không thuộc MVP nhưng có thể xem xét lại khi có quyết định mới |
| DEPRECATED | Không tiếp tục phát triển theo định hướng hiện tại; chưa xóa |

Một tài liệu hoặc màn hình chỉ có một trạng thái chính. Ghi chú có thể chỉ rõ phần tái sử dụng.

## CURRENT

| Material | Lý do |
|---|---|
| `PROJECT_SOURCE_OF_TRUTH.md` | Nguồn sản phẩm có thẩm quyền cao nhất |
| `AGENTS.md` | Quy tắc làm việc và giới hạn phạm vi hiện tại |
| `CODEX_START_PROMPT.txt` | Công cụ nội bộ nhắc AI ưu tiên Source of Truth |
| `docs/product/PRODUCT_BRIEF.md` | Bản tóm tắt Product Alignment từ Source of Truth |
| `docs/product/MVP_SCOPE.md` | Baseline phạm vi MVP hiện tại |
| `docs/product/USER_JOURNEY.md` | Hành trình hai phiên của người dùng trung tâm |
| `docs/product/PRODUCT_OUTCOMES.md` | Outcome và metric baseline hiện tại |
| `docs/product/SCOPE_STATUS.md` | Bảng phân loại phạm vi và material hiện tại |
| `docs/ui/INFORMATION_ARCHITECTURE.md` | IA cho 5 trải nghiệm MVP |
| `docs/ui/SCREEN_REQUIREMENTS.md` | Yêu cầu UI baseline cho 5 màn hình MVP |
| `docs/management/*.md` | Các log/tracker P0 mới tạo; đang là bản nháp chờ team review |
| `docs/research/*.md` | Research plan, interview guide và synthesis template; chưa có dữ liệu nghiên cứu |
| `docs/demo/*.md` | Storyboard, script, runbook và pitch outline hiện tại; chưa chứng minh demo đã chạy |

## REUSABLE

| Material | Phần có thể tái sử dụng | Điều kiện |
|---|---|---|
| `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai/DESIGN.md` | Màu sắc, typography, spacing, card, button, chip, badge, chat bubble | Loại bỏ ngôn ngữ booking/hold khỏi component semantics |
| `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai_chat_booking_bot_ai/code.html` | Bố cục hội thoại ba cột, chat và contextual panel | Đổi vai trò AI và thay booking summary bằng profile/memory |
| `MOCKUI/stitch_booking_bot_ai_agent/danh_s_ch_c_n_h_booking_bot_ai/code.html` | Property card, filter, map và metadata | Recommendation phải là trọng tâm; bổ sung lý do và source |
| `MOCKUI/stitch_booking_bot_ai_agent/chi_ti_t_c_n_h_booking_bot_ai/code.html` | Gallery, facts, amenities và CTA | Không dùng time-slot automation; CTA xem nhà chỉ tạo Pending request |
| `MOCKUI/stitch_booking_bot_ai_agent/l_ch_xem_c_a_t_i_booking_bot_ai/code.html` | Tab, status chip và card list | Chỉ tái sử dụng pattern cho journey history/feedback state |
| `README.md` | Cấu trúc hướng dẫn dự án | Cần viết lại toàn bộ nội dung theo sản phẩm hiện tại |
| `README_boilerplate.md` | Khung README | Phải viết lại theo dự án hiện tại trước khi sử dụng |
| `presentation/README.md` | Checklist bàn giao và cấu trúc pitch | Phải chuyển thành narrative demo hai phiên |
| `JOURNAL.md` | Khung nhật ký theo tuần | Hiện là template trống; không được coi là bằng chứng tiến độ |
| `WORKLOG.md` | Khung ghi nhận công việc | Hiện là template trống; không được coi là bằng chứng tiến độ |
| `eval/results/report.md` | Khung báo cáo đánh giá | Phải đổi sang metric hiện tại và điền bằng dữ liệu test thật |
| `docs/guide/deliverables/checklist.md` | Checklist bàn giao chung | Cần điều chỉnh cho output và demo của dự án |

## HISTORICAL

| Material | Lý do giữ lại |
|---|---|
| `Booking_bot_PRD.docx` | Ghi lại hướng BookingBot, booking automation và Multi-Agent trước đây |
| `PROJECT BRIEF.pdf` | Ghi lại problem/solution và định vị cũ |
| `ARCHITECTURE.md` | Template kiến trúc chưa hoàn thiện; không có thẩm quyền sản phẩm hiện tại |
| `docs/architecture_diagram.md` | Sơ đồ kiến trúc mẫu; không đại diện cho quyết định sản phẩm hiện tại |
| `MOCKUI/stitch_booking_bot_ai_agent/ch_n_ng_y_v_gi_booking_bot_ai/code.html` | Bằng chứng thiết kế luồng chọn thời gian cũ |
| `MOCKUI/stitch_booking_bot_ai_agent/tr_ng_th_i_gi_c_n_booking_bot_ai/code.html` | Bằng chứng thiết kế soft hold và tìm sale cũ |
| `MOCKUI/stitch_booking_bot_ai_agent/x_c_nh_n_th_nh_c_ng_booking_bot_ai/code.html` | Bằng chứng thiết kế xác nhận booking cũ |

## FUTURE

| Material/Phạm vi | Điều kiện xem xét lại |
|---|---|
| Quy trình xử lý yêu cầu “Tôi muốn xem căn này” sau trạng thái Pending | MVP cốt lõi đã được kiểm chứng và có owner vận hành |
| Calendar, notification và CRM | Có nhu cầu người dùng/stakeholder được xác thực và quyết định phạm vi mới |
| Dashboard vận hành đơn giản | Có quy trình vận hành thật cần hỗ trợ |
| Mobile app riêng | Web MVP chứng minh được retention và nhu cầu sử dụng |

Không material FUTURE nào tự động trở thành backlog MVP.

## DEPRECATED

| Material/Định hướng | Lý do |
|---|---|
| `MOCKUI/stitch_booking_bot_ai_agent/landing_page_booking_bot_ai/code.html` với thông điệp “đặt lịch xem nhà” | Định vị cũ; layout chỉ có thể tái sử dụng sau khi viết lại nội dung |
| `MOCKUI/stitch_booking_bot_ai_agent/dashboard_sale_booking_bot_ai/code.html` | Lấy sale workflow làm trung tâm, ngoài MVP |
| `MOCKUI/stitch_booking_bot_ai_agent/dashboard_qu_n_tr_booking_bot_ai/code.html` | Lấy booking KPI và vận hành sale làm trung tâm, ngoài MVP |
| Định vị “AI booking/soft-hold assistant” | Mâu thuẫn với AI Home Search Companion |
| Sale là core user | Mâu thuẫn với persona renter-first |
| Booking count và sale performance là outcome chính | Mâu thuẫn với retention/resume outcome |
| Multi-Agent/Microservices/Event Bus là mặc định của MVP | Tăng scope và không trực tiếp chứng minh giá trị sản phẩm |

`CURRENT` trong bảng này nghĩa là phù hợp với định hướng hiện tại, không đồng nghĩa tài liệu đã được team phê duyệt hoặc công việc đã hoàn tất.
