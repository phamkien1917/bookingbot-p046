# Field Survey — Bài toán "phễu đứt gãy kép"

## Mục đích

Lấp 7 khoảng trống dữ liệu mà báo cáo nghiên cứu (Gemini Deep Research, 08/2026) không
trả lời được vì không có nguồn công khai cho thị trường Việt Nam:

| # | Khoảng trống | Bản A (môi giới) | Bản B (người tìm nhà) |
|---|---|---|---|
| 1 | Số phút/ngày môi giới mất để chốt lịch | A1, A2, A3 | — |
| 2 | Tần suất trùng lịch (double-booking) | B1, B2, B3 | C? gián tiếp |
| 3 | Tỷ lệ lead bị bỏ rơi tại VN | C1, C2, C3 | C1, C2 |
| 4 | Speed-to-lead thực tế tại VN | C1 | C1 |
| 5 | Số căn xem thật + % chuyến đi lãng phí do tin ảo | — | B2, B3 |
| 6 | Chỉ số tắc nghẽn bộ lọc / tiêu chí không lọc được | — | A1, A2, A3, A4 |
| 7 | Willingness to pay (SaaS per-seat) + tác động Luật 2024 | D1–D5 | — |

Nguyên tắc (theo `INTERVIEW_GUIDE.md`): hỏi hành vi và lần xảy ra gần nhất trước, không
dẫn dắt người trả lời khen giải pháp AI. Phần AI để cuối.

## Cỡ mẫu mục tiêu (đủ dùng cho pitch, không phải nghiên cứu hàn lâm)

- Bản A: ≥ 15 môi giới, từ ≥ 3 sàn khác nhau ở Hà Nội. Đừng lấy 1 sàn.
- Bản B: ≥ 20 người đang hoặc vừa tìm nhà trong 12 tháng qua.
- Pilot 2 người mỗi bản trước, chỉnh câu khó hiểu, rồi mới chạy tiếp.

## Ghi dữ liệu

- 1 Google Sheet, mỗi người trả lời = 1 dòng, mỗi câu = 1 cột.
- Câu mở: chép nguyên văn, không diễn giải tại chỗ.
- Mỗi bản ghi cỡ mẫu và ngày: "n=16 môi giới, 3 sàn, Hà Nội, 09/2026".

## Câu đồng thuận (đọc trước khi bắt đầu)

> Nhóm em đang tìm hiểu cách mọi người tìm nhà và chốt lịch đi xem, cùng những chỗ khó
> trong quá trình đó. Không có câu trả lời đúng hay sai. Khảo sát khoảng [6] phút, ẩn danh,
> anh/chị bỏ qua câu nào cũng được.

---

# BẢN A — Môi giới / Quản lý sàn (~6–8 phút)

### Sàng lọc
- S1. Anh/chị làm môi giới BĐS bao lâu rồi? _____ (dưới 6 tháng / 6–24 tháng / trên 2 năm)
- S2. 3 tháng qua có trực tiếp nhận khách và dẫn đi xem nhà không?  ☐ Có  ☐ Không → **dừng**
- S3. Khu vực hoạt động chính: _____   Vai trò: ☐ Môi giới  ☐ Trưởng nhóm  ☐ Quản lý sàn

### A. Điều phối lịch và thời gian
- A1. Một ngày làm việc điển hình, anh/chị mất khoảng bao nhiêu thời gian **chỉ để nhắn tin / gọi điện chốt giờ đi xem nhà** với khách?
  ☐ < 15 phút ☐ 15–30 phút ☐ 30–60 phút ☐ 1–2 giờ ☐ > 2 giờ
- A2. Trước khi chốt được một lịch xem, thường phải trao đổi qua lại mấy lượt tin nhắn với khách?
  ☐ 1–2 ☐ 3–5 ☐ 6–10 ☐ > 10
- A3. Để biết một căn còn trống / còn chìa khóa để dẫn xem, anh/chị làm cách nào? *(chọn nhiều)*
  ☐ Tự nhớ ☐ Nhắn chủ nhà qua Zalo ☐ Hỏi quản lý ☐ Tra Excel/CRM ☐ Khác: ___
- A4. Công cụ chính đang dùng để quản lý lịch hẹn và khách? *(chọn nhiều)*
  ☐ Zalo/Messenger cá nhân ☐ Nhóm Zalo ☐ Sổ tay/giấy ☐ Excel/Google Sheets ☐ Google Calendar ☐ Phần mềm CRM ☐ Khác: ___

### B. Trùng lịch
- B1. 3 tháng qua, anh/chị hoặc đội có gặp **trùng lịch** không? (2 khách cùng 1 giờ, hoặc 2 sale cùng dẫn 1 căn cùng lúc)
  ☐ Chưa lần nào ☐ 1 lần ☐ 2–3 lần ☐ > 3 lần
- B2. Lần gần nhất, hậu quả là gì? ☐ Mất khách ☐ Khách phàn nàn ☐ Phải dời lịch ☐ Chủ nhà khó chịu ☐ Không đáng kể
  Kể ngắn: ________________________________________
- B3. Ước tính mỗi vụ trùng/hủy lịch làm mất khoảng bao nhiêu (doanh thu hoặc chi phí cơ hội)? _____

### C. Lead và tốc độ phản hồi
- C1. Trong 10 khách để lại thông tin / inbox, trung bình bao nhiêu người anh/chị trả lời **trong vòng 1 giờ**?  ___/10
- C2. Bao nhiêu người anh/chị **không kịp trả lời trong 24 giờ hoặc bỏ luôn**?  ___/10
- C3. Lý do chính khiến lead bị trả lời chậm / bỏ sót? *(chọn 1–2)*
  ☐ Quá nhiều lead ☐ Đang bận dẫn khách khác ☐ Lead rác nhiều ☐ Ngoài giờ làm ☐ Quên ☐ Khác: ___

### D. Tác động Luật 2024 và mức sẵn sàng chi trả
- D1. Từ 1/8/2024 (Luật Kinh doanh BĐS mới), cách sàn quản lý khách/lead của anh/chị có thay đổi không?
  ☐ Có — quản lý tập trung hơn ☐ Có — phải mua thêm phần mềm ☐ Chưa thay đổi ☐ Không rõ
- D2. Sàn/anh chị hiện có trả phí phần mềm quản lý khách hàng không? Bao nhiêu / tháng / người? _____
- D3. Nếu có trợ lý AI trả lời khách trong 1 phút (kể cả ngoài giờ), chốt đúng khung giờ rảnh và tự ghi vào lịch — sẵn sàng trả bao nhiêu **/tháng cho mỗi tài khoản sale**?
  ☐ Không trả ☐ < 100k ☐ 100–300k ☐ 300–500k ☐ 500k–1tr ☐ > 1tr
- D4. Hoặc sẵn sàng trích bao nhiêu **% hoa hồng** mỗi giao dịch chốt nhờ công cụ? _____
- D5. Điều gì khiến anh/chị **không** dùng một công cụ như vậy? ________________________________________

- Đóng: Còn điều gì về việc chốt lịch / quản lý khách mà em chưa hỏi không?

---

# BẢN B — Người tìm / thuê / mua nhà (~5–6 phút)

### Sàng lọc
- S1. 12 tháng qua anh/chị có đang hoặc đã tìm nhà không?  ☐ Có  ☐ Không → **dừng**
- S2. ☐ Mua  ☐ Thuê   Khu vực tìm: _____
- S3. Đã đi xem nhà thực tế chưa?  ☐ Rồi  ☐ Chưa

### A. Bộ lọc và ngữ cảnh
- A1. Khi tìm trên Batdongsan / Chợ Tốt / trang khác, **tiêu chí quan trọng nào anh/chị KHÔNG chọn được bằng bộ lọc có sẵn**? *(ghi nguyên văn; chỉ gợi ý nếu người trả lời bí: yên tĩnh, an ninh, hàng xóm, ngập nước, hướng/phong thủy, gần chỗ làm tính theo thời gian đi)*
  ________________________________________
- A2. Anh/chị mô tả căn nhà mong muốn bằng khoảng mấy tiêu chí? ___  Trong đó mấy tiêu chí lọc được trên web? ___
- A3. Mỗi lần mở lại web tìm tiếp, có phải nhập lại bộ lọc từ đầu không?
  ☐ Luôn luôn ☐ Thường ☐ Hiếm ☐ Web nhớ giúp
- A4. Việc phải chỉnh lại bộ lọc nhiều lần đã khiến anh/chị bỏ cuộc giữa chừng bao giờ chưa?  ☐ Rồi  ☐ Chưa

### B. Tìm kiếm và thời gian
- B1. Anh/chị tìm được bao lâu rồi?  ☐ < 2 tuần ☐ 2–4 tuần ☐ 1–2 tháng ☐ 2–3 tháng ☐ > 3 tháng
- B2. Đã đi xem thực tế bao nhiêu căn?  ___
- B3. Trong số đó, bao nhiêu căn tới nơi thấy **khác xa tin đăng, hoặc bị dẫn qua căn khác** (tin ảo)?  ___

### C. Tốc độ phản hồi của môi giới
- C1. Lần gần nhất để lại thông tin / nhắn hỏi một căn, **bao lâu môi giới phản hồi lần đầu**?
  ☐ < 5 phút ☐ 5–30 phút ☐ 30 phút–1 giờ ☐ 1–24 giờ ☐ > 24 giờ ☐ Không ai trả lời
- C2. Trong 10 lần anh/chị liên hệ hỏi nhà, khoảng bao nhiêu lần bị **lơ hoàn toàn**?  ___/10
- C3. Khi một môi giới phản hồi chậm, anh/chị làm gì?  ☐ Chờ tiếp ☐ Hỏi môi giới khác ☐ Bỏ căn đó
- C4. Đợt tìm này anh/chị làm việc với mấy môi giới?  ___

### D. Chấp nhận AI
- D1. Giữa hai cách: **(A)** nhắn qua lại với môi giới 5–7 câu mất ~30 phút mới chốt được giờ xem; **(B)** nói thẳng với một AI "cho tôi xem căn này chiều mai sau 5h, sắp người cho tôi" — anh/chị thấy cách nào hợp hơn?
  ☐ A ☐ B ☐ Tùy tình huống ☐ Không chắc
- D2. Anh/chị có ngại để AI chốt lịch thay không? Ngại điều gì? ________________________________________
- D3. Cần thấy gì để tin lịch AI chốt là **thật**, không phải bẫy dẫn đi xem nhà mồi? ________________________________________

- Đóng: Điều gì bực nhất khi tìm nhà mà em chưa hỏi tới?

---

## Phân tích sau khi thu

- Mỗi câu số: báo cáo **trung vị** (median) kèm n, không dùng trung bình nếu mẫu lệch.
- Ghép lên slide đúng chỗ theo bảng ánh xạ ở đầu file.
- Chọn 2–3 câu nói nguyên văn mạnh nhất đưa lên slide — nặng ký hơn con số.
- Số nào mẫu < 10 thì ghi rõ "khảo sát nhanh, n=…", không gọi là "nghiên cứu".
