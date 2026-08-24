# P-046 — Biên bản tích hợp và QA phần Kiên/Lực

**Ngày:** 24/08/2026  
**Phạm vi:** Review các thay đổi chat/tìm kiếm của Kiên và đầu việc Product/BA/QA do Lực phụ trách.

## 1. Phân chia trách nhiệm

### Kiên — triển khai chức năng

- Cải thiện tìm kiếm bất động sản toàn quốc và hội thoại nhiều lượt.
- Nhận diện số lượng kết quả, hạn chế lặp lại căn đã giới thiệu.
- Cho phép chọn căn theo tiêu đề hiển thị hoặc mã bất động sản.
- Khôi phục phiên chat gần nhất và hạn chế gửi yêu cầu trùng.
- Duy trì luồng deploy Vercel/Render.

### Lực — tích hợp sản phẩm và kiểm soát chất lượng

- Chuyển chức năng đã làm thành acceptance criteria và bằng chứng demo.
- Review giao điểm giữa đăng nhập, quyền sở hữu hội thoại và memory.
- Bổ sung regression test cho các trường hợp chọn nhầm bất động sản.
- Kiểm tra backend test, frontend lint/build và phản hồi AI trên deployment.
- Ghi nhận rõ phần đã xong, giới hạn hiện tại và việc cần làm tiếp.

## 2. Trạng thái acceptance

| Năng lực | Trạng thái | Bằng chứng |
|---|---|---|
| Tìm nhà bằng ngôn ngữ tự nhiên | DONE | Chat production trả kết quả grounded |
| Tinh chỉnh nhu cầu qua nhiều lượt | DONE | Backend test và production smoke test |
| Tìm theo miền/tỉnh/quận | DONE | Search criteria test và truy vấn deployment |
| Yêu cầu số lượng kết quả | DONE | Truy vấn yêu cầu ba căn trả đúng ba kết quả |
| Chọn căn theo tiêu đề hoặc mã | DONE | Unit test cho full title, partial title và property code |
| Không chọn căn chỉ từ tên địa điểm | DONE | Regression test với yêu cầu chỉ nêu Thanh Xuân |
| Khôi phục hội thoại gần nhất | DONE | Đã review implementation; còn checklist browser thủ công |
| Chặn double submit khi AI đang trả lời | DONE | Input, submit và quick reply bị khóa khi loading |
| Ngăn tái sử dụng session giữa hai tài khoản | DONE | Logout xóa chat session ID trên trình duyệt |
| Frontend interaction test tự động | NOT STARTED | Repo chưa cấu hình test runner cho frontend |

## 3. Rủi ro và xử lý

### P1 — Quyền sở hữu session

Backend kiểm tra hội thoại thuộc đúng customer, trong khi frontend lưu session ID ở `sessionStorage`. Nếu tài khoản A đăng xuất rồi tài khoản B đăng nhập trong cùng tab, session cũ có thể gây HTTP 403. Bản tích hợp xóa session ID khi logout, nhưng vẫn giữ được hành trình guest đăng nhập để tiếp tục đặt lịch.

### P1 — Chọn nhầm căn do địa danh trong tiêu đề

Tiêu đề tin đăng thường lặp lại quận/tỉnh. Câu chỉ nêu địa điểm phải được hiểu là tiêu chí tìm kiếm, không được tự động chọn một căn bất kỳ. Matcher đã loại token thuộc address/ward/district/province khỏi điểm fuzzy matching và yêu cầu property code khớp đúng ranh giới token.

### P2 — Chưa có browser automation

Reload, restore session, stop generation và double click hiện được kiểm tra bằng review, lint/build và checklist thủ công. Chỉ nên thêm Playwright khi team sẵn sàng duy trì test frontend.

### P2 — Benchmark model

Deployment đang dùng `gpt-4o-mini`. Trước khi đổi model, cần so sánh trên cùng bộ câu hỏi tiếng Việt theo relevance, groundedness, khả năng hỏi lại, latency và chi phí.

## 4. Checklist regression thủ công

1. Chat ở chế độ guest, đăng nhập customer và xác nhận có thể tiếp tục hành trình.
2. Reload `/chat`; hội thoại cũ được khôi phục và prompt không bị gửi lại.
3. Mở URL có `?prompt=...`, reload; prompt chỉ được gửi một lần.
4. Double-click nút gửi và quick reply; chỉ một request được tạo.
5. Nhấn Stop; ô nhập hoạt động lại và không xuất hiện error banner.
6. Logout tài khoản A, login tài khoản B; B không gặp HTTP 403 do session của A.
7. Chọn căn bằng full title, một cụm tên riêng đặc trưng và property code.
8. Nói “đặt lịch căn ở Thanh Xuân”; agent phải yêu cầu chọn căn cụ thể thay vì tự chọn.

## 5. Nội dung báo mentor

Kiên đã hoàn thiện phần triển khai chính của chat và tìm kiếm. Lực phụ trách review tích hợp và quality gate, bổ sung regression coverage cho chọn bất động sản, xử lý ranh giới session giữa các tài khoản, kiểm tra production build và ghi nhận các giới hạn còn lại. Luồng AI deploy đang hoạt động và trả kết quả dựa trên dữ liệu hệ thống; mốc chất lượng tiếp theo là browser automation và benchmark model thay vì mở rộng thêm chức năng.
