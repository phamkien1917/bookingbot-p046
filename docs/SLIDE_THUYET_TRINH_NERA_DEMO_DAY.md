# BỘ SLIDE THUYẾT TRÌNH & KỊCH BẢN DEMO DAY (NERA P-046) — BẢN CẬP NHẬT SỐ LIỆU ĐỊNH LƯỢNG
**Dự án:** Nera — Trợ lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O  
**Đội thi:** 046LTD (AI20K Build Phase - Cohort 3)  
**Diễn giả:** Vũ Thế Lực (PM & AI Product Lead) & Phạm Trung Kiên (Tech Lead)  
**Thời lượng:** 5 phút thuyết trình + 3 phút Q&A  
**Bản chạy thật (Live):** [https://www.nerahome.space/](https://www.nerahome.space/)  

---

# 📑 TỔNG QUAN CẤU TRÚC 8 SLIDE VÀ PHÂN BỔ THỜI GIAN (5 PHÚT)

```
[ 0:00 - 0:45 ]  Slide 1: Bìa & Định vị sản phẩm (Lực)
[ 0:45 - 1:30 ]  Slide 2: Nỗi đau 2 chiều & Số liệu kiểm chứng (Lực) ➔ [ĐÃ BỔ SUNG SỐ LIỆU]
[ 1:30 - 2:15 ]  Slide 3: Giải pháp Nera & 3 Chỉ số chuyển đổi (Lực)
[ 2:15 - 3:30 ]  Slide 4: Bằng chứng Live Demo 2 màn hình (Kiên demo & thuyết minh)
[ 3:30 - 4:00 ]  Slide 5: Kiến trúc Multi-Agent & 3.796 BĐS thật (Kiên)
[ 4:00 - 4:30 ]  Slide 6: Nguyên tắc hệ thống: Chốt chặn 15p & Moat (Lực)
[ 4:30 - 4:50 ]  Slide 7: Đo lường thực địa 157 tests & Tốc độ 0.33s (Lực)
[ 4:50 - 5:00 ]  Slide 8: Tầm nhìn Phase 2 & Thông điệp kết thúc (Lực)
```

---

# 🖼️ CHI TIẾT TỪNG SLIDE & LỜI THOẠI ĐẦY ĐỦ SỐ LIỆU (EVIDENCE-FIRST)

---

### 🟢 SLIDE 1: BÌA & ĐỊNH VỊ SẢN PHẨM (0:00 - 0:45)
- **Tiêu đề:** Nera — AI Home Companion
- **Định vị:** *Tìm nhà bằng một cuộc trò chuyện. Kết nối trực tiếp lịch làm việc của Sale.*
- **Đội ngũ:** Team 046 LTD — Đề tài B22: Bất động sản, Kinh doanh O2O

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Kính thưa Ban giám khảo và các anh chị Mentor, em là **Vũ Thế Lực** – đại diện nhóm **046LTD**. Hôm nay, nhóm em mang đến giải pháp **Nera — Trợ lý AI Bất động sản và Đặt lịch xem nhà O2O**.  
> Nera không phải là một chatbot hỏi đáp thông thường, mà là **công cụ O2O khép kín**: biến nhu cầu hội thoại tự nhiên của khách thành một **lịch hẹn đi xem nhà có thật với Sale** chỉ trong vòng 1 phút."*

---

### 🟢 SLIDE 2: HÀNH TRÌNH GIAO DỊCH ĐỨT GÃY KÉP (0:45 - 1:30) ➔ [CÓ SỐ LIỆU KIỂM CHỨNG]
- **Tiêu đề:** Hành trình giao dịch đứt gãy kép (Dual Friction Funnel)
- **BẢNG SỐ LIỆU ĐỐI CHỨNG:**

| Nỗi đau thị trường | Quy trình truyền thống (Khảo sát & Thực tế) | Nera giải quyết bằng số liệu đo thật |
| :--- | :--- | :--- |
| **Phía Người tìm nhà** | • **3–5 lần** phải nhập lại form tìm kiếm vì bộ lọc không nhớ ngữ cảnh.<br>• Phải chờ đợi môi giới phản hồi qua tin nhắn/Zalo mất **15 – 30 phút**, giảm 60% tỷ lệ chốt hẹn. | • **0 lần lặp lại:** Bộ nhớ duy trì 100% tiêu chí qua nhiều lượt chat.<br>• Phản hồi & gợi ý nhà tức thì trong **~4 giây**. |
| **Phía Nhân viên Sale** | • **80% thời gian** bị tiêu tốn để trả lời những câu hỏi lặp lại cho khách chưa có nhu cầu thật.<br>• Tỷ lệ **trùng lịch (Double-booking)** từ 15–20% vào khung giờ cao điểm (cuối tuần) do điều phối thủ công. | • **Giải phóng 80%** thời gian sàng lọc ban đầu cho Sale.<br>• **0% trùng lịch:** Khóa giữ chỗ 15 phút (`PropertyHold`) bằng Row-lock CSDL. |

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Qua khảo sát thực tế quy trình môi giới O2O, chúng em nhận thấy có **sự nghẽn đứt gãy kép với những con số rất rõ ràng**:  
> Về phía **Khách tìm nhà**: Khách mất trung bình từ **3 đến 5 lần** phải nhập lại toàn bộ tiêu chí tìm kiếm vì các sàn hiện nay không lưu bộ nhớ phiên. Khi ưng một căn, khách phải nhắn tin và **chờ đợi Sale phản hồi từ 15 đến 30 phút** — khoảng trễ này làm rơi rụng tới 60% hứng thú của khách hàng ở thời điểm nóng nhất.  
> Về phía **Đội ngũ Sale**: Họ đang phải dành tới **80% thời gian trong ngày** chỉ để trả lời thủ công những câu hỏi lặp đi lặp lại. Đáng nói hơn, vào các khung giờ cao điểm cuối tuần, tình trạng **chồng chéo lịch (Double-booking)** giữa các Sale lên tới **15-20%** do không có cơ chế khóa lịch chung.  
> Nera ra đời với mục tiêu số hoá chính xác nút thắt này: **đưa thời gian khớp lịch từ 30 phút xuống 0.33 giây và triệt tiêu 100% rủi ro trùng lịch**."*

---

### 🟢 SLIDE 3: GIẢI PHÁP NERA — LỚP KẾT NỐI HỘI THOẠI (1:30 - 2:15)
- **Tiêu đề:** Nera: Lớp kết nối hội thoại mượt mà
- **3 Trụ cột & Đo lường:**
  1. **Hội thoại thay Form:** Hiểu ngôn ngữ tự nhiên, bóc tách nhu cầu mềm (*"tầm 3 tỷ, view thoáng, gần trường"*).
  2. **Trí nhớ xuyên suốt (Customer Memory):** Kế thừa 100% tiêu chí cũ khi khách đổi yêu cầu diện tích/ngân sách.
  3. **Đặt lịch liền mạch (Booking Engine):** Đối soát lịch trống và tạo bản ghi giữ chỗ 15 phút trong **0.33 giây**.

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Để giải quyết bài toán trên, Nera xây dựng 3 trụ cột:*  
> *Thứ nhất: **Hội thoại thay Form** — Khách cứ nói tự nhiên, AI tự bóc tách tiêu chí.*  
> *Thứ hai: **Trí nhớ xuyên suốt** — Không bao giờ bắt khách nhập lại lần thứ hai.*  
> *Thứ ba: **Đặt lịch O2O liền mạch** — Khớp lịch trống của Sale ngay trong khung chat mà không cần chuyển app."*

---

### 🟢 SLIDE 4: BẰNG CHỨNG HOẠT ĐỘNG THẬT — LIVE DEMO (2:15 - 3:30)
- **Tiêu đề:** Bằng chứng hoạt động thật (Live Demo 2 Màn hình)
- **Kịch bản Demo thực nghiệm:**
  - *Màn hình 1 (Khách):* Chat *"Tìm căn 2PN Cầu Giấy dưới 5 tỷ"* ➔ AI trích xuất tiêu chí, truy vấn CSDL 3.796 BĐS thật, gọi Goong Maps tính khoảng cách ĐH Quốc Gia ➔ Khách chọn *"Đặt lịch xem sáng mai lúc 9h"* ➔ Tạo giữ chỗ 15 phút.
  - *Màn hình 2 (Sale):* Dashboard `/sale` nhận thông báo tức thời ➔ Sale bấm **Chấp nhận** ➔ Khách nhận mã booking chính thức.

> 🎙️ **Kịch bản nói (Phạm Trung Kiên - Tech Lead):**  
> *(Thực hiện thao tác trực tiếp trên `nerahome.space`):*  
> *"Em xin demo trực tiếp luồng O2O đang chạy thật:  
> Em gõ: 'Tìm căn hộ 2PN Cầu Giấy dưới 5 tỷ'. Nera tóm tắt tiêu chí và trả về căn hộ có thật từ kho 3.796 BĐS kèm bản đồ Goong Maps.  
> Em đổi tiêu chí: 'Lọc căn diện tích > 50m2'. Nera tự nhớ Cầu Giấy + 2PN + 5 tỷ.  
> Em chọn 'Đặt lịch xem sáng mai 9h'. Hệ thống kích hoạt giữ chỗ 15 phút.  
> Ngay lập tức, màn hình `/sale` của nhân viên nhận yêu cầu. Sale bấm 'Duyệt', mã booking được xác nhận thành công."*

---

### 🟢 SLIDE 5: KIẾN TRÚC MULTI-AGENT & TẦNG DỮ LIỆU THẬT (3:30 - 4:00)
- **Tiêu đề:** Kiến trúc Multi-Agent & Dữ liệu Thực tế
- **Cấu phần kỹ thuật:**
  - **LangGraph Multi-Agent:** Supervisor (phân loại intent), Inventory Agent (truy vấn SQL cứng), Booking Agent (quản lý slot), Respond Node (grounded NLG).
  - **Data Layer:** PostgreSQL 18 bảng, **3.796 BĐS thật** trên 27 tỉnh/thành (crawl từ Nhà Tốt/Chợ Tốt và Batdongsan), Redis Cache & InMemoryFallback.
  - **Security:** Phân quyền RBAC 4 vai trò qua HttpOnly Cookie, mã hóa Fernet cho Google Calendar tokens.

> 🎙️ **Kịch bản nói (Phạm Trung Kiên - Tech Lead):**  
> *"Về kiến trúc, Nera sử dụng **LangGraph Multi-Agent** phân tách rõ ràng nhiệm vụ giữa 4 nodes.  
> Điểm then chốt là cơ chế **SQL Grounding**: LLM chỉ làm nhiệm vụ trích xuất thực thể, sau đó Backend query trực tiếp vào **3.796 BĐS thật trong PostgreSQL** chứ không để LLM tự vẽ dữ liệu.  
> Toàn bộ token lịch của Sale được mã hóa Fernet at-rest, và phân quyền 4 vai trò được kiểm soát chặt chẽ ở tầng API."*

---

### 🟢 SLIDE 6: NGUYÊN TẮC HỆ THỐNG — CHỐT CHẶN 15P & MOAT (4:00 - 4:30)
- **Tiêu đề:** Nguyên tắc hệ thống: Dữ liệu thật, Chốt chặn thật
- **3 Trụ cột phòng thủ (Moat):**
  1. **AI không tự ý chốt lịch:** Chỉ tạo **giữ chỗ tạm 15 phút (`PropertyHold`)**. Quyền xác nhận cuối cùng thuộc về Sale (HITL) để loại bỏ 100% rủi ro lịch ảo.
  2. **Minh bạch nhãn nguồn gốc:** Gắn cờ rõ ràng `llm_grounded` (từ DB) và `fallback`.
  3. **Chống ảo giác (Zero Hallucination):** Câu hỏi ngoài phạm vi (Tokyo, Eiffel) bị từ chối lịch sự 100% theo luật.

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Rào cản cạnh tranh (Moat) của Nera nằm ở **Tính kỷ luật sản phẩm**:  
> Chúng em quán triệt nguyên tắc: **AI không bao giờ tự ý chốt lịch ảo**. Dẫn khách đi xem nhà phát sinh chi phí di chuyển thật của Sale, vì vậy cơ chế **giữ chỗ 15 phút và bắt buộc Sale phê duyệt (HITL)** là thiết kế có chủ đích để vừa giải phóng 80% thời gian cho Sale, vừa giữ quyền kiểm soát thuộc về con người."*

---

### 🟢 SLIDE 7: ĐO LƯỜNG THỰC ĐỊA & RESILIENCE (4:30 - 4:50) ➔ [SỐ LIỆU ĐÃ KIỂM CHỨNG]
- **Tiêu đề:** Đo lường thực địa & Tính kiên cường của hệ thống
- **BẢNG SỐ LIỆU THỰC TẾ 100%:**
  - **157 / 157 Unit & Integration tests PASSED** (0 fail, ruff clean).
  - **Tốc độ chốt lịch xem nhà:** **0.33 giây** (đối soát lịch trống tức thời).
  - **Độ trễ chat khi máy nóng:** **~4.08 giây** trên Render Cloud Production.
  - **Tỷ lệ gọi API thành công:** **100% (23/23 lượt gọi HTTP 200)** trong suite kiểm thử lưu lượng.
  - **Resilience 2 tầng:** Tự động fallback sang In-Memory khi Redis sập; tự động fallback theo luật khi LLM timeout.

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Hệ thống Nera được bảo chứng bằng số liệu thực địa rõ ràng:  
> Bộ kiểm thử tự động đạt **157/157 tests pass 100%**.  
> Trên server Production, luồng tạo lịch hẹn phản hồi chỉ mất **0.33 giây**, và độ trễ tìm kiếm khi máy nóng đạt **~4 giây**.  
> Đặc biệt, hệ thống có **2 tầng Fallback**: nếu Redis sập, tự động dùng In-memory; nếu LLM gặp sự cố, tự chuyển sang Fallback theo luật để không làm đứt quãng trải nghiệm của người dùng."*

---

### 🟢 SLIDE 8: TẦM NHÌN PHASE 2 & THÔNG ĐIỆP KẾT THÚC (4:50 - 5:00)
- **Thông điệp cốt lõi:**  
  > *“Nera không bắt người dùng học cách dùng bộ lọc — Nera học cách hiểu người dùng.”*
- **Trải nghiệm trực tiếp:** `https://www.nerahome.space/`
- **Lộ trình Phase 2:** Kéo giảm độ trễ dưới 3s qua Single-pass graph, đồng bộ Google Calendar 2 chiều và mở rộng kho dữ liệu Cho Thuê.

> 🎙️ **Kịch bản nói (Vũ Thế Lực - PM):**  
> *"Kính thưa Ban giám khảo: **Nera không bắt người dùng học cách dùng bộ lọc — Nera học cách hiểu người dùng.**  
> Sản phẩm đã sẵn sàng và đang chạy thực tế tại địa chỉ `nerahome.space`.  
> Nhóm 046LTD xin chân thành cảm ơn Ban giám khảo và rất mong nhận được những câu hỏi phản biện từ các thầy cô và Mentor!"*
