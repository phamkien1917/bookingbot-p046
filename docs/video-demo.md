# Video Demo — Nera AI Real Estate Platform (P-046)

> **Deliverable #6 — Ban Tổ Chức AI20K Build Phase (Cohort 3)**  
> **Dự án:** Nera — Trợ lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O  
> **Đội thi:** P-046 / 046LTD  
> **Thành viên:** Vũ Thế Lực (PM & AI Product Lead) · Phạm Trung Kiên (Tech Lead)  
> **Bản chạy thật (Live URL):** [https://www.nerahome.space/](https://www.nerahome.space/)  

---

## 📺 Link Video Demo

- **Link Google Drive:** <https://drive.google.com/file/d/1o6ARDVOoEcJxOWv9sOlvjT2fQkIvIcIX/view?usp=drive_link>
- **Thời lượng:** 5 phút 50 giây (đo từ file gốc `Demo phase 2 T046.mp4`, 185 MB)
- **File gốc không nằm trong repo:** `.gitignore` loại `*.mp4` để giữ repo dưới ngưỡng dung lượng BTC yêu cầu.

---

## ⏱️ Cấu trúc video

Sáu phân đoạn theo đúng thứ tự trong video. Mốc thời gian cụ thể chưa đối chiếu
lại với bản đã quay nên không ghi ở đây.

```
Phần 1: Giới thiệu đội ngũ & nỗi đau đứt gãy kép (Dual Friction Funnel)
Phần 2: Demo chat khách hàng — tìm nhà tự nhiên, trích xuất tiêu chí & Goong Maps
Phần 3: Demo trí nhớ đa lượt (Customer Memory) & so sánh căn hộ
Phần 4: Demo đặt lịch xem nhà O2O & khóa giữ chỗ 15 phút (PropertyHold)
Phần 5: Demo màn hình Sale (/sale) duyệt lịch thực tế (Human-in-the-loop)
Phần 6: Minh chứng kỹ thuật — Langfuse tracing, đo token, stage timings & chốt
```

---

## 📝 Chi tiết từng phân đoạn trong Video

### Phân đoạn 1: Mở đầu & Bài toán thực tế
- **Hình ảnh:** Bìa Nera, hai diễn giả (Vũ Thế Lực & Phạm Trung Kiên), bảng số liệu đối chứng thị trường.
- **Nội dung:** Giới thiệu Nera — nền tảng giải quyết bài toán đứt gãy giữa nhu cầu tìm nhà trên mạng và kết nối lịch xem thực tế với Sale:
  - Khách mất 3–5 lần nhập lại form; Sale mất 80% thời gian trả lời câu hỏi lặp lại.
  - Tỷ lệ trùng lịch xem nhà thực tế lên tới 15–20% vào khung giờ cao điểm.

### Phân đoạn 2: Trải nghiệm Khách hàng tìm nhà
- **Thao tác:** Mở giao diện `https://www.nerahome.space/chat`.
- **Câu lệnh chat 1:** *"Tìm căn hộ 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ gần ĐH Quốc Gia Hà Nội"*.
- **Điểm nổi bật:**
  - AI bóc tách tiêu chí tức thì: Quận Cầu Giấy, 2PN, trần giá 5 tỷ.
  - Truy vấn CSDL 3.796 BĐS thật tại PostgreSQL.
  - Gọi Goong Maps API tính khoảng cách & thời gian di chuyển đi làm (< 15 phút), hiển thị badge và iframe bản đồ trực tiếp trong khung chat.

### Phân đoạn 3: Trí nhớ hội thoại đa lượt & So sánh
- **Câu lệnh chat 2:** *"Chỉ lấy những căn diện tích trên 60m2 và có sổ đỏ"*.
- **Điểm nổi bật:** Nera tự động kế thừa tiêu chí cũ (Cầu Giấy + 2PN + 5 tỷ) mà không bắt khách nhập lại, lọc bổ sung điều kiện diện tích và pháp lý.
- **Câu lệnh chat 3:** *"So sánh căn số 1 và căn số 2 giúp mình"*.
- **Điểm nổi bật:** Xuất bảng so sánh đối chiếu chi tiết điểm mạnh/yếu của 2 căn.

### Phân đoạn 4: Đặt lịch xem nhà O2O
- **Câu lệnh chat 4:** *"Mình muốn đặt lịch xem căn số 1 vào 9h sáng mai"*.
- **Điểm nổi bật:**
  - Hệ thống kiểm tra slot trống của Sale và kích hoạt khóa giữ chỗ 15 phút (`PropertyHold`) bằng Row-lock CSDL.
  - Khách nhận thông báo yêu cầu đã được gửi tới chuyên viên Sale phụ trách khu vực.

### Phân đoạn 5: Human-In-The-Loop trên Dashboard của Sale
- **Thao tác:** Chuyển sang màn hình Sale `/sale` (đăng nhập bằng `kien.sale@example.com`).
- **Điểm nổi bật:**
  - Sale nhận thông báo yêu cầu đặt lịch mới với đầy đủ thông tin căn hộ và giờ hẹn.
  - Sale bấm **Chấp nhận**.
  - Quay lại màn hình khách hàng: Lịch hẹn được chuyển trạng thái sang **Xác nhận thành công**, cấp mã Booking chính thức và hiển thị tên/SĐT Sale.

### Phân đoạn 6: Minh chứng Kỹ thuật & Observability
- **Hình ảnh:** Màn hình Dashboard Langfuse Tracing và Terminal log.
- **Điểm nổi bật:**
  - Hiển thị cây trace Langfuse: chia tách thời gian từng node (`supervisor`, `inventory`, `respond`) và log riêng thời gian gọi Goong Maps.
  - Đo lường token và chi phí runtime: ~13.9 VNĐ/lượt, Cost/Job ~5.000 VNĐ.
  - 720 automated tests pass 100%.

---

## 🛡️ Demo các trường hợp Biên & Khả năng Chống lỗi (Edge Cases)

1. **Chống ảo giác (Out-of-Scope Guardrail):** Khi hỏi *"Tháp Eiffel cao bao nhiêu?"*, Nera từ chối lịch sự và quay lại chủ đề BĐS, không tốn token gọi model diễn dịch ngoài lề.
2. **Xử lý lỗi Tool bản đồ (Tool Failure):** Khi Goong Maps gặp sự cố, Nera báo rõ "chưa xác minh được khoảng cách" thay vì tự bịa số km.
3. **Chống Double-Booking:** Khi 2 phiên chat cùng đặt 1 slot, hệ thống xử lý qua PostgreSQL Advisory Lock đảm bảo 1 người giữ chỗ thành công và 1 người nhận cảnh báo trùng lịch an toàn.

---

## 🔑 Tài khoản kiểm thử cho Giám khảo

| Vai trò | Email đăng nhập | Mật khẩu Demo | URL giao diện |
|---|---|---|---|
| **Khách hàng** | `customer.demo@example.com` | `Demo@123` | `https://www.nerahome.space/chat` |
| **Chuyên viên Sale** | `kien.sale@example.com` | `Demo@123` | `https://www.nerahome.space/sale` |
| **Quản trị viên (Admin)** | `admin.demo@example.com` | `Demo@123` | `https://www.nerahome.space/admin` |
