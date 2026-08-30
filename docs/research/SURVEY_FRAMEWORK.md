# Khung khảo sát — Kiểm chứng bài toán "phễu đứt gãy kép"

Tài liệu này là **khung nghiên cứu**: nói rõ đo cái gì, hỏi ai, hỏi thế nào, phân tích ra sao.
Bộ câu hỏi cụ thể nằm ở [`FIELD_SURVEY.md`](FIELD_SURVEY.md). Nghiên cứu định tính sâu về
người thuê nhà nằm ở [`RESEARCH_PLAN.md`](RESEARCH_PLAN.md) và [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md).
Khung này bổ sung phần **định lượng** phục vụ slide "Bài toán" và hồ sơ gọi vốn.

---

## 1. Mục tiêu nghiên cứu

1. Kiểm chứng cả hai phía của "phễu đứt gãy kép" là vấn đề có thật và đủ lớn ở thị trường
   Hà Nội, bằng số liệu sơ cấp — không chỉ suy từ nghiên cứu quốc tế.
2. Lấp 7 khoảng trống dữ liệu mà báo cáo Gemini Deep Research không có nguồn công khai.
3. Tìm điểm chuẩn giá (pricing benchmark) cho mô hình SaaS per-seat.
4. Thu câu nói nguyên văn của người dùng thật để đưa lên slide.

Nghiên cứu này **không** nhằm chứng minh trước rằng giải pháp AI là đúng. Phần phản ứng
với AI để cuối bảng hỏi và tách riêng khi phân tích.

---

## 2. Giả thuyết cần kiểm chứng

| Mã | Giả thuyết | Ngưỡng coi là "được xác nhận" | Câu hỏi đo |
|---|---|---|---|
| H1 | Môi giới mất nhiều thời gian mỗi ngày chỉ để chốt lịch xem nhà | Trung vị ≥ 30 phút/ngày | A/A1, A/A2 |
| H2 | Trùng lịch xảy ra thường xuyên và gây hậu quả thật | ≥ 40% môi giới gặp ≥ 1 lần/3 tháng | A/B1, A/B2 |
| H3 | Tỷ lệ lead bị bỏ rơi tại VN cao | Trung vị ≥ 3/10 lead không được trả lời trong 24h | A/C2, B/C2 |
| H4 | Phản hồi thực tế chậm hơn nhiều so với kỳ vọng của khách | Trung vị thời gian phản hồi ≥ 1 giờ | B/C1 |
| H5 | Bộ lọc hiện tại bỏ sót phần lớn tiêu chí khách quan tâm | Trung vị: > 40% tiêu chí không lọc được | B/A1, B/A2 |
| H6 | Khách phải làm lại thao tác mỗi phiên tìm | ≥ 50% trả lời "luôn/thường" nhập lại bộ lọc | B/A3 |
| H7 | Có mức sẵn sàng chi trả cho công cụ AI chốt lịch | ≥ 50% chủ sàn/quản lý chọn mức ≥ 100k/seat/tháng | A/D3 |

Ghi lại cả bằng chứng **phản bác** từng giả thuyết, không chỉ bằng chứng ủng hộ.

---

## 3. Biến số đo lường (mỗi biến = 1 con số cho slide)

**Phía môi giới**
- Thời gian điều phối lịch (phút/ngày)
- Số lượt tin nhắn để chốt 1 lịch xem
- Tần suất trùng lịch (lần/3 tháng) + loại hậu quả
- Tỷ lệ lead trả lời trong 1 giờ (x/10)
- Tỷ lệ lead bỏ rơi > 24 giờ (x/10)
- Công cụ đang dùng (phân bố %)
- Mức sẵn sàng chi trả (VND/seat/tháng) và % hoa hồng

**Phía người tìm nhà**
- Số tiêu chí mong muốn vs số tiêu chí lọc được (tỷ lệ)
- Tần suất phải nhập lại bộ lọc
- Thời gian tìm (tuần)
- Số căn đã đi xem thực tế
- Số căn "tin ảo" trong đó
- Thời gian môi giới phản hồi lần đầu (khoảng)
- Tỷ lệ bị lơ hoàn toàn (x/10)
- Số môi giới làm việc cùng trong 1 đợt
- Lựa chọn A (chat thủ công) vs B (nói với AI)

---

## 4. Đối tượng và cỡ mẫu

### Bản A — Môi giới / Quản lý sàn

| Tiêu chí | Yêu cầu |
|---|---|
| Nghề | Đang làm môi giới BĐS, có nhận khách và dẫn xem trong 3 tháng gần đây |
| Địa bàn | Hà Nội (ưu tiên), phân bố ≥ 3 sàn khác nhau |
| Vai trò | Trộn: môi giới thường, trưởng nhóm, quản lý sàn (cần ≥ 3 quản lý cho câu giá) |
| Loại trừ | Người chỉ môi giới đất nền tỉnh, người nghỉ nghề > 3 tháng |
| Cỡ mẫu | **≥ 15**, lý tưởng 20 |

### Bản B — Người tìm / thuê / mua nhà

| Tiêu chí | Yêu cầu |
|---|---|
| Trạng thái | Đang hoặc vừa tìm nhà trong 12 tháng qua, có tham gia quyết định |
| Địa bàn | Hà Nội hoặc thành phố lớn |
| Hành vi | Đã xem nhiều tin qua nhiều ngày; đã đi xem thực tế ≥ 1 căn (ưu tiên) |
| Loại trừ | Môi giới, người mua thuần đầu tư, người chưa từng tìm |
| Cỡ mẫu | **≥ 20**, lý tưởng 30 |

Mẫu này đủ cho pitch, **không** đại diện thống kê cho toàn thị trường. Luôn báo cáo kèm n.

---

## 5. Phương pháp

- **Hình thức:** bảng hỏi cấu trúc, tự điền hoặc phỏng vấn ngắn 1:1 (6–8 phút). Ưu tiên
  phỏng vấn trực tiếp với môi giới (tỷ lệ hoàn thành cao hơn, hỏi thêm được).
- **Kênh tiếp cận:**
  - Môi giới: đến trực tiếp 3–4 văn phòng sàn ở Hà Nội; nhóm Zalo môi giới; người quen giới thiệu.
  - Người tìm nhà: hội nhóm Facebook "tìm nhà Hà Nội", bạn bè đang thuê/mua, quét tại chung cư mới.
- **Thứ tự hỏi:** hành vi và lần gần nhất trước → số liệu → phần AI cuối cùng.
- **Không dẫn dắt:** không mô tả Nera trước khi hỏi xong phần hành vi. Không gợi ý đáp án
  cho câu mở trừ khi người trả lời bí.
- **Pilot:** 2 người mỗi bản trước, sửa câu khó hiểu, ghi lại thay đổi, rồi mới chạy tiếp.

---

## 6. Quy trình thực địa

1. Đọc câu đồng thuận (có trong `FIELD_SURVEY.md`). Xác nhận người trả lời đồng ý, ẩn danh.
2. Hỏi câu sàng lọc. Nếu không đạt → cảm ơn, dừng, không tính vào mẫu.
3. Chạy hết bảng hỏi. Câu mở chép nguyên văn.
4. Nhập ngay vào Google Sheet sau mỗi buổi (đừng để dồn).
5. Mỗi người = 1 dòng. Cột đầu: mã người (P-A-01…), ngày, sàn/khu vực, người khảo sát.

### Cấu trúc Google Sheet

- Sheet `A_moigioi`: 1 cột / câu hỏi bản A + cột metadata.
- Sheet `B_nguoitimnha`: tương tự bản B.
- Sheet `quotes`: mã người | câu hỏi | câu nói nguyên văn.
- Sheet `analysis`: tính trung vị, phân bố, đối chiếu ngưỡng giả thuyết ở mục 2.

---

## 7. Quy tắc phân tích

1. Tách rõ **Observation** (số/câu nói) — **Interpretation** (mình hiểu là gì) — **Slide implication**.
2. Câu số: báo cáo **trung vị** kèm n và khoảng (min–max). Không dùng trung bình nếu mẫu lệch.
3. Một ý kiến đơn lẻ không thành insight. Ghi số người ủng hộ mỗi pattern.
4. Ghi cả bằng chứng phản bác giả thuyết.
5. Mẫu < 10 → gọi là "khảo sát nhanh / định tính", không gọi "nghiên cứu".
6. Đối chiếu từng giả thuyết H1–H7 với ngưỡng: xác nhận / một phần / bác bỏ / chưa đủ dữ liệu.

---

## 8. Đưa kết quả vào bài thuyết trình

| Kết quả | Vị trí dùng |
|---|---|
| Phút/ngày chốt lịch, tần suất trùng lịch | Slide "Bài toán" — cột phải (phía Sale) |
| Tỷ lệ tiêu chí không lọc được, phải nhập lại bộ lọc | Slide "Bài toán" — cột trái (người tìm nhà) |
| Thời gian phản hồi, tỷ lệ lead bỏ rơi tại VN | Slide "Bài toán" — ô "chờ đợi phản hồi", ghép với số HBR quốc tế |
| Mức sẵn sàng chi trả | Slide mô hình kinh doanh / "The Ask" |
| 2–3 câu nói nguyên văn | Slide "Bài toán" — trích dẫn, nặng ký hơn con số |
| Bảng câu hỏi + data thô | Slide phụ lục (mở khi BGK hỏi sâu) |

---

## 9. Lịch trình đề xuất

| Ngày | Việc |
|---|---|
| 1 | Pilot 2+2 người. Chỉnh bảng hỏi. Lập Google Sheet. |
| 2–4 | Chạy thực địa: chia team đi hỏi môi giới (3 sàn) và người tìm nhà. |
| 5 | Nhập nốt data. Tính trung vị, đối chiếu giả thuyết. |
| 6 | Ráp số + câu nói vào slide "Bài toán" và slide phụ lục. Tập nói. |

Gửi số cho phần ráp slide khi đã có ≥ 10 phản hồi mỗi bản.

---

## 10. Rủi ro và cách xử lý

| Rủi ro | Xử lý |
|---|---|
| Không đủ 15 môi giới trước demo | Ưu tiên chất lượng: 8–10 phỏng vấn sâu vẫn dùng được nếu ghi rõ n |
| Môi giới trả lời lấy lệ mức chi trả | Hỏi thêm "sàn đang trả bao nhiêu cho phần mềm hiện tại" để có mốc đối chiếu |
| Mẫu lệch về 1 sàn | Bắt buộc ≥ 3 sàn; ghi tên sàn ở metadata để kiểm |
| Người tìm nhà không nhớ số liệu chính xác | Chấp nhận khoảng (dưới 5 phút / 5–30 phút…); không ép con số tuyệt đối |
| BGK nghi ngờ mẫu nhỏ | Chuẩn bị sẵn câu: "phỏng vấn định tính n=…, dùng để hiểu vấn đề, không phải đại diện thị trường" |
