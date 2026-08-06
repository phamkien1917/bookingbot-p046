
AI20K – Ngân hàng đề  Khóa 3 & 4

100%
bds
1 trong tổng số 61
B22 BĐS – Kinh doanh O2O (Doanh nghiệp bất động sản X) 
B25

BĐS – Kinh doanh O2O (Doanh nghiệp bất động sản X)
AllTopics360


 
 	
BĐS – Kinh doanh O2O (Doanh nghiệp bất động sản X)
Bật chế độ hỗ trợ trình đọc màn hình
Để bật chế độ hỗ trợ đọc màn hình, nhấn Ctrl+Alt+Z Để tìm hiểu thêm về các phím tắt, nhấn Ctrl+dấu gạch chéoThông báo bị ẩnChuột lang nước ẩn danh đã rời khỏi tài liệu.

 
 	
📍 Thực trạng: Việc hẹn khách xem nhà mẫu/căn thực tế phải phối hợp lịch sale, xe đưa đón, tình trạng căn và phòng chờ; điều phối thủ công qua chat gây trùng lịch và bỏ lỡ khách.

🎯 Vấn đề: Cần AI Agent hiểu yêu cầu khách bằng ngôn ngữ tự nhiên, dùng công cụ kiểm tra lịch trống của sale và trạng thái căn, đề xuất khung giờ, đặt lịch và giữ căn tạm thời (soft-hold), tự gửi nhắc và xử lý dời/hủy.

🔒 Ràng buộc: HITL cho sale xác nhận trước khi chốt lịch và giữ căn; tránh double-booking bằng khóa giao dịch; bảo mật thông tin khách; xử lý lỗi khi API lịch/căn không phản hồi và cảnh báo giới hạn giữ căn.


Tech stack gợi ý

LLM function-calling (GPT-4o)
CrewAI/LangGraph điều phối tool
Google/Outlook Calendar API
Postgres inventory với row-lock
FastAPI + Next.js
WebSocket cập nhật real-time
deploy Fly.io.

Yêu cầu đầu ra (Cơ bản + Nâng cao) - gợi ý
Cơ bản:

App đăng nhập (khách/sale hoặc sale/điều phối viên), agent hội thoại đặt lịch xem nhà, kiểm tra & giữ căn, gửi xác nhận, HITL duyệt.

Nâng cao:

Tối ưu lộ trình dẫn nhiều khách trong ngày, tự động dời lịch khi xung đột, tích hợp bản đồ tiện ích, eval tỉ lệ đặt lịch thành công và no-show, memory ưu tiên khung giờ của từng khách.