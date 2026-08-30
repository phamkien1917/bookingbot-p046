# Information Architecture — 5 trải nghiệm MVP

## Mục tiêu IA

- Đặt AI Conversation ở trung tâm, không biến sản phẩm thành portal bất động sản có gắn chatbot.
- Cho người dùng luôn nhìn thấy AI biết gì, đã ghi nhớ gì và vì sao đề xuất.
- Hỗ trợ một hành trình liên tục từ hội thoại đến feedback, shortlist, compare và resume.
- Chỉ định nghĩa 5 trải nghiệm MVP; không bổ sung dashboard, booking flow hoặc màn hình sale/admin.

## Cấu trúc cấp cao

```text
AI Home Search Companion
├── 1. AI Conversation — điểm vào chính
│   ├── Hội thoại hiện tại
│   ├── Profile progress
│   ├── AI đang hiểu gì về bạn
│   ├── Clarification
│   └── Property cards / quick actions trong hội thoại
├── 2. Profile / AI Memory
│   ├── Nhu cầu hiện tại
│   ├── Must-have và ưu tiên
│   ├── Tiêu chí linh hoạt và trường chưa biết
│   ├── Lịch sử thay đổi
│   └── Sửa / xóa / xác nhận memory
├── 3. AI Recommendations
│   ├── Tối đa 3 lựa chọn
│   ├── Lý do phù hợp
│   ├── Chưa phù hợp / trade-off / dữ liệu thiếu
│   └── Like / dislike / save / reject + lý do
├── 4. Shortlist & Compare
│   ├── Danh sách đang cân nhắc
│   ├── So sánh side-by-side
│   └── AI summary theo ưu tiên cá nhân
└── 5. Journey History / Resume
    ├── Recap phiên trước
    ├── Căn đã xem / lưu / loại
    ├── Feedback và lý do
    └── Tiếp tục từ điểm đã dừng
```

## Điều hướng chính

| Vị trí | Mục đích | Hành vi |
|---|---|---|
| AI Conversation | Điểm vào mặc định và nơi tiếp tục hội thoại | Mở phiên hiện tại hoặc bắt đầu journey mới khi chưa có dữ liệu |
| Recommendations | Xem tập đề xuất hiện tại | Hiển thị tối đa 3 căn và giải thích |
| Shortlist & Compare | Ra quyết định giữa các căn đã lưu | Mở shortlist và chế độ compare |
| Journey | Xem lại và tiếp tục hành trình | Hiển thị recap, lịch sử và CTA resume |
| Profile / Memory | Kiểm tra điều AI đang ghi nhớ | Cho phép xác nhận, sửa hoặc xóa dữ liệu |

Profile/Memory phải dễ truy cập từ mọi trải nghiệm vì người dùng cần kiểm soát memory. AI Conversation vẫn là mục điều hướng nổi bật nhất.

## Luồng Session 1

```text
AI Conversation
→ Profile được trích xuất và làm rõ
→ AI Recommendations
→ Feedback
→ Shortlist & Compare
→ Journey được lưu tại điểm dừng
```

## Luồng Session 2

```text
Journey History / Resume
→ AI recap
→ người dùng xác nhận hoặc sửa Profile / Memory
→ AI Recommendations đã cá nhân hóa
→ Shortlist & Compare
→ feedback mới cập nhật hành trình
```

## Quan hệ giữa các trải nghiệm

| Nguồn | Đích | Lý do chuyển |
|---|---|---|
| AI Conversation | Profile / Memory | Xem hoặc sửa điều AI vừa trích xuất |
| AI Conversation | AI Recommendations | Khi đã đủ thông tin để đề xuất |
| AI Recommendations | Profile / Memory | Điều chỉnh tiêu chí sau khi thấy trade-off |
| AI Recommendations | Shortlist & Compare | Save một căn hoặc so sánh lựa chọn |
| Shortlist & Compare | AI Conversation | Hỏi thêm về trade-off hoặc thay đổi ưu tiên |
| Journey History / Resume | AI Conversation | Tiếp tục hội thoại tại điểm đã dừng |
| Journey History / Resume | Shortlist & Compare | Tiếp tục cân nhắc các căn đã lưu |
| Mọi trải nghiệm | Profile / Memory | Kiểm tra, xác nhận hoặc sửa memory |

## Mô hình thông tin dùng chung

Các trải nghiệm phải sử dụng cùng một cách gọi và cùng một trạng thái hiển thị cho:

- nhu cầu hiện tại;
- must-have, ưu tiên và tiêu chí linh hoạt;
- trường đã biết, chưa biết hoặc cần xác nhận;
- căn đã xem, đã lưu, đã loại;
- LIKE, DISLIKE, SAVE, REJECT và lý do;
- recommendation hiện tại;
- shortlist;
- điểm đang dừng trong journey;
- nguồn và mức độ đầy đủ của dữ kiện căn hộ.

## Nguyên tắc hiển thị

1. AI phải giải thích hành động hoặc đề xuất có ảnh hưởng đến quyết định.
2. Người dùng phải phân biệt được dữ kiện nguồn, diễn giải của AI và dữ liệu còn thiếu.
3. Memory phải minh bạch và có thể chỉnh sửa.
4. Feedback phải được xác nhận ngay sau hành động.
5. Resume phải chỉ rõ nội dung được khôi phục từ phiên trước.
6. Property detail mở trong ngữ cảnh recommendation/compare, không tạo thêm một trải nghiệm MVP độc lập.
7. “Tôi muốn xem căn này” là hành động phụ tạo trạng thái Pending, không mở booking flow mới.

## Ngoài IA MVP

- Sale Dashboard;
- Admin Dashboard;
- booking calendar;
- chọn time slot;
- soft-hold countdown;
- tự động phân công sale;
- CRM hoặc notification center;
- portal quản lý bất động sản đầy đủ.
