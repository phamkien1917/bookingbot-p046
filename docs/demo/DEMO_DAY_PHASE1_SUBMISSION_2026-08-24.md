# Nera — Gói nộp Demo Day Phase 1

**Đội:** 046LTD  
**Hạn Phase 1:** 23:59 ngày 24/08/2026  
**Trạng thái kiểm tra:** 24/08/2026

## 1. Trạng thái nộp bài

| Hạng mục | Trạng thái | Nội dung/việc cần làm |
|---|---|---|
| Tên sản phẩm | READY | Nera |
| Mô tả ngắn | READY | Copy nội dung tại mục 2 |
| Mô tả dự án | READY | Copy nội dung tại mục 3 |
| Link MVP | READY | https://www.nerahome.space/ |
| Video demo | NEED LINK | Video đã làm từ tuần trước nhưng không tìm thấy URL trong repo; dán lại link YouTube/Drive vào form |
| Slides | BLOCKED | Hai PPTX trong repo là báo cáo Mentor Duty cũ, còn ghi XHome và “MVP đang hoàn thiện dataset”; không dùng để nộp |
| Ảnh đại diện | NEED LINK | Ưu tiên screenshot thật của trang chủ/chat; fallback khẩn cấp: https://www.nerahome.space/favicon.ico |
| Đóng góp thành viên | READY | 25% mỗi thành viên, tổng 100% |
| AI log | READY | 113 / 737 / 1077 / 117, tất cả đều vượt mức 50 |

## 2. Nội dung 1–2 câu hiển thị trên thẻ Demo Day

> Nera là trợ lý AI tìm nhà qua hội thoại tự nhiên: hiểu nhu cầu, ghi nhớ tiêu chí và gợi ý những bất động sản có thật phù hợp với người dùng. Khi khách chọn được căn phù hợp, Nera hỗ trợ đặt lịch xem nhà nhưng vẫn giữ nhân viên sale là người xác nhận cuối cùng.

## 3. Nội dung mô tả dự án — copy vào form

## Bài toán

Người tìm nhà phải đọc nhiều tin đăng rời rạc, lặp lại tiêu chí mỗi lần tìm và liên hệ thủ công để đặt lịch xem. Những bộ lọc truyền thống cũng khó thể hiện các nhu cầu mềm như gần trường, tiện đi làm, phù hợp gia đình hoặc chấp nhận đánh đổi giữa giá và vị trí.

## Giải pháp

Nera biến quá trình tìm nhà thành một cuộc hội thoại. Người dùng mô tả nhu cầu bằng ngôn ngữ tự nhiên; hệ thống làm rõ thông tin còn thiếu, duy trì tiêu chí qua nhiều lượt, tìm và so sánh bất động sản từ dữ liệu hệ thống, đồng thời giải thích lý do phù hợp. Người dùng có thể lưu căn, phản hồi thích/không thích và tiếp tục hành trình khi quay lại.

Khi người dùng muốn xem nhà, Nera kiểm tra các khung giờ khả dụng và tạo yêu cầu đặt lịch. AI không tự chốt lịch thay con người: sale phải xác nhận trước khi lịch hẹn trở thành chính thức.

## Giải pháp kỹ thuật

- **Frontend:** Next.js, triển khai trên Vercel.
- **Backend:** FastAPI, triển khai trên Render.
- **AI orchestration:** LangGraph kết hợp GPT-4o-mini.
- **Dữ liệu:** PostgreSQL cho dữ liệu bất động sản, người dùng và lịch hẹn; Redis cho trạng thái tạm với cơ chế fallback.
- **Grounding:** thông tin giá, diện tích, số phòng và địa điểm lấy từ dữ liệu hệ thống; LLM không tự tạo thông tin bất động sản.
- **Human-in-the-loop:** backend giữ quyền phân quyền và booking; sale xác nhận trước khi chốt lịch.
- **Minh bạch AI:** response công khai trạng thái `llm_grounded`, `llm_direct`, `llm_intent` hoặc `fallback`.

## Tính khả thi

MVP đang chạy công khai tại https://www.nerahome.space/. Luồng production đã được kiểm tra trực tiếp: website và backend trả HTTP 200; agent trả đúng ba bất động sản cho yêu cầu thử nghiệm, sử dụng `gpt-4o-mini` ở chế độ `llm_grounded`. Bộ kiểm thử hiện có **53 test pass**, Ruff pass, frontend lint pass và Next.js production build pass.

## Hướng phát triển

Giai đoạn tiếp theo tập trung vào benchmark chất lượng model trên bộ câu hỏi tiếng Việt cố định, browser automation cho các luồng chat quan trọng, dữ liệu khoảng cách/tiện ích thực tế và công cụ tính tài chính có kiểm chứng. Team ưu tiên tăng độ tin cậy và khả năng giải thích trước khi mở rộng thêm chức năng.

## 4. Link cần điền vào form

- **Sản phẩm:** https://www.nerahome.space/
- **Repository:** https://github.com/AI20K-Build-Phase-Cohort-3/P-046
- **Video:** `[DÁN LINK VIDEO ĐÃ NỘP TUẦN TRƯỚC]`
- **Slides:** `[DÁN LINK GOOGLE SLIDES/DRIVE SAU KHI CẬP NHẬT NERA]`
- **Ảnh đại diện:** `[DÁN LINK SCREENSHOT TRANG CHỦ/CHAT ĐỂ ANYONE WITH THE LINK CÓ THỂ XEM]`
- **Ảnh fallback khẩn cấp:** https://www.nerahome.space/favicon.ico

## 5. Cấu trúc slides cần làm

Không dùng deck Mentor Duty hiện tại. Deck Phase 1 nên có 8 slide:

1. **Nera — Tìm nhà bằng một cuộc trò chuyện**  
   Tên đội, bốn thành viên, link/QR MVP.
2. **Người tìm nhà đang phải tự ghép một hành trình rời rạc**  
   Tin đăng phân tán, bộ lọc cứng, quên tiêu chí, đặt lịch thủ công.
3. **Nera hiểu nhu cầu trước khi gợi ý căn**  
   Conversation → clarification → persistent criteria → recommendation.
4. **Demo thật: từ câu nói tự nhiên tới property card có dữ liệu**  
   Dùng screenshot thật từ `www.nerahome.space`, không dùng mockup.
5. **AI giải thích; backend giữ nguồn sự thật**  
   Next.js → FastAPI/LangGraph → PostgreSQL → grounded response.
6. **Sale vẫn là người chốt lịch**  
   User chọn căn → hệ thống kiểm tra slot → sale xác nhận → booking.
7. **MVP đã được kiểm chứng**  
   Live URL, 53 test pass, lint/build pass, AI mode grounded.
8. **Phase 2: đo chất lượng trước khi mở rộng**  
   Benchmark model, browser automation, bản đồ/tiện ích và financial tool.

## 6. Kịch bản demo 3–4 phút

### Chuẩn bị trước khi quay/demo

1. Mở `https://www.nerahome.space/` trước ít nhất 10 phút để đánh thức backend.
2. Mở `https://www.nerahome.space/` và kiểm tra `/chat`.
3. Chuẩn bị một customer account và một sale account đã đăng nhập ở hai cửa sổ riêng.
4. Tạo chat mới để tránh lịch sử cũ ảnh hưởng kết quả.
5. Quay video backup kể cả khi dự định demo live.

### Lời thoại và thao tác

**0:00–0:25 — Bài toán**  
“Người tìm nhà không chỉ có giá và số phòng. Họ có nhu cầu mềm, phải xem nhiều nguồn và thường phải nói lại từ đầu. Nera thay hành trình đó bằng một cuộc trò chuyện.”

**0:25–1:20 — Tìm kiếm có grounding**  
Nhập: `Tôi muốn tìm 3 căn hộ ở Hà Nội, ngân sách dưới 5 tỷ.`  
Chỉ ra ba property card, giá/địa điểm lấy từ dữ liệu hệ thống và nhãn `llm_grounded`.

**1:20–1:55 — Hội thoại nhiều lượt**  
Nhập một tiêu chí bổ sung, ví dụ: `Ưu tiên khu Thanh Xuân và 3 phòng ngủ.`  
Nhấn mạnh người dùng không phải nhập lại ngân sách hoặc loại căn.

**1:55–2:35 — Chọn căn và đặt lịch**  
Chọn một căn bằng số hoặc tiêu đề, sau đó yêu cầu xem lịch trống. Dừng trước bước xác nhận cuối nếu không muốn tạo dữ liệu demo.

**2:35–3:05 — Human-in-the-loop**  
Mở giao diện Sale và giải thích sale mới là người nhận/từ chối yêu cầu; AI không tự chốt lịch với khách hàng thật.

**3:05–3:35 — Kiến trúc và bằng chứng**  
“LLM hiểu ý định và viết giải thích; backend kiểm soát dữ liệu, quyền truy cập và booking. MVP hiện có 53 test pass, lint/build pass và đang chạy công khai.”

**3:35–3:50 — Kết**  
“Nera không bắt người dùng học cách dùng bộ lọc — Nera học cách hiểu người dùng.”

## 7. Checklist trước khi bấm Submit

- [ ] Tên hiển thị thống nhất là **Nera**, không còn XHome/VisitOps trong slide nộp.
- [ ] Link sản phẩm dùng `https://www.nerahome.space/`.
- [ ] Video mở được ở chế độ ẩn danh, quyền YouTube Unlisted hoặc Drive Anyone with the link.
- [ ] Slide mở được ở chế độ ẩn danh.
- [ ] Ảnh đại diện mở trực tiếp được và không yêu cầu đăng nhập.
- [ ] Không đưa API key, mật khẩu hoặc tài khoản cá nhân vào slide/video.
- [ ] Video có phụ đề hoặc âm thanh rõ, 1080p nếu có thể.
- [ ] Mở sẵn backend health trước demo để tránh cold start 30–60 giây.
- [ ] Có video backup nếu demo live gặp lỗi mạng/provider.
- [ ] Bốn thành viên xác nhận tỷ lệ 25% và nội dung đóng góp.
