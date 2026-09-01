# Monetization One-Pager — Nera

**Nhóm P-046 · 046 LTD · Bài tập Day 28 (AI Pricing · GTM · Evidence)**
Sản phẩm: trợ lý AI tìm nhà và đặt lịch xem — https://www.nerahome.space/

---

## 1. PRICING

### Value Metric: **Seat** (300.000đ/tài khoản/tháng), lộ trình sang Hybrid

Chấm theo ma trận Attribution × Autonomy:

| Trục | Nera | Vì sao |
| :--- | :--- | :--- |
| **Attribution** | **CAO** | Mỗi lịch hẹn là một bản ghi `tour_request` do chính agent tạo, gắn session và sale. Đo được tuyệt đối, không phải suy đoán. |
| **Autonomy** | **THẤP (cố ý)** | Nera dựng yêu cầu, nhưng sale phải bấm duyệt thì lịch mới thành `CONFIRMED`. Human-in-the-loop là điểm bán, không phải hạn chế. |

Ma trận trỏ vào ô **Usage**. Nhưng chọn **Seat**, vì hai lý do:

**Thị trường đã tự khai giá.** Khảo sát 20 môi giới và quản lý sàn: **85% (17/20)** sẵn sàng trả, trung vị đúng **300.000đ/seat/tháng**. Sàn đã có sẵn dòng ngân sách theo đầu người cho CRM — bán theo seat là cắm vào một ô ngân sách đã tồn tại, không phải xin duyệt một dòng mới.

**Nhược điểm của Seat không áp dụng ở đây.** Seat nguy hiểm khi khách dùng nhiều thì âm biên. Chi phí biến đổi của Nera là ~50.000đ/seat/tháng trên giá 300.000đ — một sale phải dùng gấp sáu lần mức trung bình mới chạm điểm hoà. Rủi ro thật rất thấp.

**Lộ trình:** đo `tour_request` chốt được ngay từ ngày đầu. Khi có đủ dữ liệu attribution qua 3 tháng, chuyển sang **Hybrid** — seat nền 200k + 10.000đ mỗi lịch hẹn được sale duyệt. Không bán Outcome ngay: chưa có pilot nào để chứng minh tỉ lệ.

### Cost/Job — chi phí để AI làm xong **một lịch hẹn được duyệt**

| Thành phần | VNĐ | Ghi chú |
| :--- | ---: | :--- |
| **API** (LLM + Goong) | 1.200 | 5 cuộc hội thoại × 240đ. `gpt-4o-mini`, đã tính prompt caching |
| **HITL** — phút duyệt của sale | **2.150** | 1,5 phút × sale 15tr/tháng (~86k/giờ) |
| **Infra** phân bổ | 1.500 | 1,5tr/tháng ÷ 1.000 lịch (50 seat × 20 lịch) |
| **Retry** | 240 | +20% API, phòng context phình và gọi lại |
| **Tổng Cost/Job** | **~5.100** | Làm tròn **5.000đ** |

> **Phát hiện đáng chú ý: token không phải chi phí lớn nhất.** Phút duyệt của con người tốn **gần gấp đôi** tiền LLM. Đúng ô "HITL — hay bị quên" trong công thức. Muốn giảm Cost/Job thì phải rút ngắn thao tác duyệt của sale, không phải đổi model rẻ hơn.

### Giá đề xuất

Quy tắc ≥3× Cost/Job → **≥15.000đ mỗi lịch hẹn**.
Một sale chốt ~20 lịch/tháng → **300.000đ/seat/tháng**.

**Hai hướng tính hoàn toàn độc lập cùng ra 300k:** từ dưới lên bằng Cost/Job × 3, và từ trên xuống bằng trung vị sẵn sàng chi trả đo trên 20 người. Đây là lý do tin được mức giá này chứ không phải chọn cho tròn số.

Gross margin ở 50 seat: **~70%** (vượt ngưỡng 60%).

### Cách neo giá

**Không neo vào ChatGPT $20.** Neo vào hai thứ khách đã trả tiền:

**Neo theo nhân công.** Môi giới mất trung vị **45 phút/ngày** chỉ để nhắn tin chốt lịch — 16,5 giờ mỗi tháng, tức **9,4%** quỹ thời gian. Với lương 12tr (~68k/giờ), đó là **~1,1tr/tháng** tiêu vào việc nhắn tin. Nera lấy 300k = **27%** phần tiết kiệm đó — cao hơn khoảng 10–25% thông thường, nên một mình neo này chưa đủ thuyết phục.

**Neo theo thiệt hại đã xảy ra.** 85% môi giới gặp trùng lịch ít nhất 1 lần/3 tháng. Thiệt hại họ tự khai cho **một** lần: 8.000.000đ, 6.500.000đ, 5.000.000đ, 2.000.000đ. Trả Nera cả năm là 3,6tr — chưa bằng nửa một sự cố.

**Vì vậy neo chính là neo thiệt hại, neo thời gian chỉ đi kèm.** Câu chốt khi gặp khách: *"Anh trả 300k một tháng để không mất 8 triệu một lần."*

---

## 2. GO-TO-MARKET

### Kênh phân phối: **Sales-Led → Partner-Led**

ARPU theo đầu sale là ~$11/tháng, nhưng **đơn vị bán không phải cá nhân mà là sàn**. Một sàn 30 sale = 9tr/tháng ≈ **$345/tháng** — rơi thẳng vào vùng chết $50–$1000.

Thoát vùng chết bằng lối 2 của bài giảng: **tăng giá trị đơn hàng + kèm service**, bán trọn gói cho sàn (onboarding, nạp kho tin, cấu hình lịch sale) thay vì bán lẻ từng ghế.

**Lợi thế đang có mà không phải nhóm nào cũng có:** 20 môi giới trong khảo sát đến từ **CenLand, Đất Xanh Miền Bắc, OneHousing** và nhóm tự do. Đó là 20 người đã ngồi nói chuyện 40 phút về đúng nỗi đau này. Không phải lead lạnh — là danh sách hẹn gặp lại.

### Pain Moment

> **Thời điểm:** khi môi giới **đang dẫn khách xem căn khác** thì lead mới nhắn tin.
> **Nơi họ đang ở:** trên Zalo, trên điện thoại, một tay cầm chìa khoá.

Đây không phải suy đoán. Khi hỏi vì sao phản hồi chậm, câu trả lời lặp lại nhiều nhất đúng là *"bận dẫn khách"*, rồi *"ngoài giờ làm"*, *"lái xe ngoài đường"*.

**Hệ quả thẳng thắn cho sản phẩm:** Nera hiện là web app. Pain moment nói rằng kênh đúng là **Zalo OA**, không phải một tab trình duyệt mới. Đúng nguyên tắc "đừng bắt khách mở thêm một tab mới". Đây là khoảng cách lớn nhất giữa sản phẩm hiện tại và kênh phân phối đúng — và là ưu tiên số một sau Demo Day.

### 90-Day Plan

| Giai đoạn | Việc | Mục tiêu đo được |
| :--- | :--- | :--- |
| **Tháng 1** — Sales-Led thuần | Quay lại 3 sàn đã phỏng vấn. Cài đặt tận tay, nạp kho tin của chính họ. Miễn phí đổi lấy dữ liệu và quyền dùng tên. | **2 sàn pilot, 10 sale dùng thật** |
| **Tháng 2** — Chứng minh | Đo tỉ lệ lead được phản hồi <5 phút, số lịch hẹn chốt, số lần trùng lịch bị chặn. Viết Pilot Report. | **1 Pilot Report có số thật** |
| **Tháng 3** — Partner-Led | Cầm Pilot Report đi gặp sàn thứ 4–6. Tích hợp Zalo OA. | **3 sàn trả tiền, ~60 seat** |

Không mở rộng sang loại hình khác (nhà riêng, đất) trong 90 ngày. Thắng tuyệt đối ở căn hộ chung cư Hà Nội trước.

---

## 3. EVIDENCE

### Eval Results — đã có

Đo trên bản deploy thật, 23 lượt, 15 kịch bản:

| Chỉ số | Kết quả | Ngưỡng |
| :--- | :--- | :--- |
| Tỷ lệ thành công | **100%** (23/23) | ≥98% ✅ |
| Lỗi hệ thống (500) | **0%** | 0% ✅ |
| Phản hồi có dữ liệu đỡ lưng | **22 lượt** `llm_grounded` | ✅ |
| Chặn câu hỏi ngoài phạm vi | **100%** (Tokyo, Eiffel, prompt injection) | 100% ✅ |
| **Độ trễ P95** | **9,52s** | ≤6,0s ❌ |

**Nói thẳng chỗ trượt.** P95 chưa đạt và số này bao gồm cold start của Render gói free. Chưa tách được phần cold start ra khỏi phép đo, nên chưa đưa lên slide bán hàng. Cách xử: lên gói Starter rồi đo lại. Đây là số cứng, không phải lời hứa — kể cả khi nó xấu.

Ngoài ra: **253 test tự động**, lint sạch backend và frontend.

### Risk Checklist — trả lời được bằng văn bản

Ba câu phòng mua hàng sẽ hỏi:

**"AI này có bịa không?"** Kết quả tìm kiếm sinh từ truy vấn SQL trên kho thật rồi mới đưa cho mô hình diễn đạt. Mỗi phản hồi API kèm trường `ai_mode` cho biết câu trả lời đến từ đâu. Bộ đo chặn 100% câu ngoài phạm vi.

**"Data có bị dùng train model không?"** ⚠️ **Chưa trả lời được bằng văn bản.** Nera gọi qua OpenRouter với fallback OpenAI; điều khoản không-huấn-luyện khác nhau theo nhà cung cấp phía sau. **Phải chốt điều khoản này trước khi gặp sàn đầu tiên** — đây là câu làm chết deal.

**"Startup chết thì data của tôi ở đâu?"** Chưa có chính sách. Cần viết cam kết trả dữ liệu trong 30 ngày.

Đã có sẵn: token Google Calendar mã hoá Fernet trước khi lưu, cookie HttpOnly, kiểm tra vai trò ở phía server, crawler tôn trọng `robots.txt` và che số điện thoại nguồn.

⚠️ **Nợ bảo mật phải xử trước khi bán:** tài khoản demo trên production vẫn đăng nhập được bằng mật khẩu công khai, và chuỗi kết nối database từng nằm trong repo.

### Pilot Report — **chưa có**

Số pilot: **0**. Không có khách hàng thật nào đang dùng.

Đây là khoảng trống lớn nhất trong ba tài sản bán hàng, và cũng là lý do tháng 1 của kế hoạch 90 ngày không nhắm doanh thu mà nhắm **đổi hai pilot miễn phí lấy một bản báo cáo có số thật**.

---

## Ba rủi ro tự nhận

**Chưa ai trả đồng nào.** 300k là con số 17/20 người *nói* sẽ trả. Khoảng cách giữa nói và rút ví là chỗ nhiều startup chết. Tháng 1 tồn tại để đóng khoảng cách đó.

**Kênh chưa khớp pain moment.** Sản phẩm ở web, khách ở Zalo. Biết rồi nhưng chưa làm.

**Cost/Job phụ thuộc phút duyệt của sale.** Nếu thao tác duyệt rườm rà hơn dự tính, Cost/Job phình theo phía con người chứ không phải phía AI — và biên lợi nhuận đi theo.

---

*Mọi số liệu trong tài liệu này đến từ: khảo sát thực địa n=20 môi giới + n=30 người tìm nhà (Hà Nội, 08/2026), `docs/research/COST_MODEL.md`, `scripts/cost_model.py`, và `eval/results/DEMO_DAY_TRAFFIC_EVALUATION_REPORT.md`.*
