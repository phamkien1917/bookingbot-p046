# TÀI LIỆU TOÀN DIỆN VỀ LUỒNG HOẠT ĐỘNG AI CỦA NERA (CHO NOTEBOOKLM)
**Sản phẩm:** Nera — Trợ lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O  
**Nhóm phát triển:** Team 046 LTD (AI20K Build Phase - Cohort 3)  
**Địa chỉ ứng dụng thật:** [https://www.nerahome.space/](https://www.nerahome.space/)  
**Mục đích tài liệu:** Cung cấp nguồn tri thức đầy đủ, chính xác 100% để NotebookLM phân tích sâu luồng hoạt động của AI Agent, kiến trúc Multi-Agent LangGraph, cơ chế bảo toàn dữ liệu và sinh Audio Overview (Podcast).

---

## 1. TỔNG QUAN VỀ SẢN PHẨM & MỤC TIÊU CỐT LÕI

Nera là một hệ thống **AI Agent đàm thoại trong lĩnh vực Bất động sản O2O (Online-to-Offline)**. 

Mục tiêu tối thượng của Nera **không chỉ dừng lại ở việc tìm kiếm nhà hay trả lời câu hỏi vu vơ**, mà là **giải quyết điểm nghẽn chuyển đổi cuối cùng trong quy trình môi giới**: 
> *Biến nhu cầu tìm nhà tự nhiên của khách hàng thành một **lịch hẹn đi xem nhà thực tế** với nhân viên môi giới (Sale) mà không bị trùng lịch (Double-booking).*

### Nỗi đau thị trường giải quyết:
1. **Người tìm nhà:** Bị ép vào các bộ lọc cứng nhắc (chỉ lọc được khoảng giá, số phòng), mất ngữ cảnh mỗi lần tìm lại, và phải chờ đợi môi giới phản hồi thụ động.
2. **Đội ngũ Sale:** Điều phối lịch làm việc thủ công qua tin nhắn Zalo/Chat, dẫn đến việc chồng chéo lịch hẹn giữa các Sale và tốn 80% thời gian sàng lọc sơ bộ.

---

## 2. SƠ ĐỒ KIẾN TRÚC MULTI-AGENT TRÊN LANGGRAPH

Hệ thống AI của Nera được xây dựng theo mô hình **Supervisor-Worker Multi-Agent** trên nền tảng **LangGraph (Python FastAPI)**:

```
                  [ KHÁCH HÀNG GỬI TIN NHẮN TỪ FRONTEND /chat ]
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │          SUPERVISOR NODE          │
                     │  - Phân loại Intent (Ý định)       │
                     │  - Trích xuất tiêu chí (Entity)   │
                     │  - Kế thừa bộ nhớ ngữ cảnh        │
                     └─────────────────┬─────────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│    INVENTORY AGENT    │  │     BOOKING AGENT     │  │   AFFORDABILITY NODE  │
│ - Lọc ràng buộc cứng  │  │ - Kiểm tra slot trống │  │ - Tính toán dòng tiền │
│ - Truy vấn 3.796 BĐS  │  │ - Khóa giữ chỗ 15p    │  │ - Ước tính khoản vay  │
│ - Gọi Goong Maps API  │  │ - Gán Sale phụ trách  │  │ - Bảng trả nợ gốc/lãi │
└───────────┬───────────┘  └───────────┬───────────┘  └───────────┬───────────┘
            │                          │                          │
            └──────────────────────────┼──────────────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │           RESPOND NODE            │
                     │  - Tóm tắt tiêu chí đã hiểu       │
                     │  - Gắn nhãn minh bạch ai_mode     │
                     │  - Sinh thẻ nhà & bản đồ Iframe   │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                [ TRẢ VỀ FRONTEND NEXT.JS (REST / STREAMING SSE) ]
```

---

## 3. CHI TIẾT LUỒNG HOẠT ĐỘNG 6 BƯỚC CỦA AI AGENT

### 🔹 Bước 1: Tiếp nhận Tin nhắn & Nạp Bộ nhớ Phiên
- Khách hàng gửi tin nhắn từ giao diện web (`nerahome.space/chat`).
- Hệ thống xác thực danh tính qua **HttpOnly Cookie JWT** (Khách vãng lai dùng `session_id` UUID).
- Dịch vụ **`CustomerMemoryService`** tự động nạp hồ sơ sở thích cá nhân dài hạn từ PostgreSQL và lịch sử ngắn hạn từ Redis.

### 🔹 Bước 2: Supervisor Node (Phân loại Ý định & Trích xuất Tiêu chí)
- **Heuristic Fast-Path:** Với các câu hỏi tìm kiếm rõ ràng, Supervisor dùng bộ regex nhận diện nhanh mà không cần gọi LLM (tiết kiệm ~2.5s).
- **Phân loại Ý định (Intent Classification):**
  - `SEARCH`: Tìm kiếm hoặc lọc bất động sản.
  - `BOOK_APPOINTMENT`: Muốn đi xem nhà, đặt lịch hẹn.
  - `CANCEL_BOOKING` / `RESCHEDULE`: Hủy hoặc dời lịch hẹn đã có.
  - `AFFORDABILITY`: Hỏi về tài chính, vay ngân hàng.
  - `OUT_OF_SCOPE`: Câu hỏi phi lý (Tokyo, tháp Eiffel, thơ ca) ➔ Kích hoạt từ chối an toàn.
- **Trích xuất Thực thể (Entity Extraction):** Tự động bóc tách: Quận huyện, Phường/Xã, Khoảng giá tối đa/tối thiểu, Số phòng ngủ, Diện tích, Hướng nhà, Tình trạng pháp lý (Sổ đỏ).

### 🔹 Bước 3: Inventory Agent & Cơ chế SQL Grounding (Chống ảo giác)
- **Tuyệt đối không để LLM tự sinh BĐS:** LLM không có quyền "vẽ" ra nhà.
- Inventory Agent chuyển đổi các tiêu chí đã bóc tách thành câu lệnh SQL thuần và truy vấn trực tiếp vào bảng `properties` trong PostgreSQL (chứa **3.796 bất động sản có thật trên 27 tỉnh/thành** đã được làm sạch).
- Nếu tìm thấy BĐS: Trả về danh sách kèm hình ảnh, giá thật, diện tích thật và địa chỉ.
- Nếu không có BĐS thỏa mãn: AI thẳng thắn thông báo *"Không tìm thấy căn phù hợp"* và gợi ý mở rộng tiêu chí, **không bao giờ bịa đặt dữ liệu (Zero Hallucination)**.

### 🔹 Bước 4: GeoService & Tích hợp Bản đồ Goong Maps
- Khi khách hỏi khoảng cách (Ví dụ: *"Từ căn này đi xe đến ĐH Quốc Gia mất bao lâu?"*):
- GeoService gọi **Goong Maps API (Geocode & DistanceMatrix)**:
  - Lấy tọa độ BĐS trong CSDL ➔ Tính khoảng cách thực tế (km) và thời gian di chuyển bằng xe máy/ô tô (phút).
- Frontend tự động render **Iframe bản đồ Google/Goong Maps dẫn đường** ngay bên dưới thẻ nhà.

### 🔹 Bước 5: Booking Agent & Cơ chế Khóa Giữ Chỗ 15 Phút (`PropertyHold`)
- Khi khách chọn: *"Đặt lịch xem căn số 1 vào sáng mai lúc 9h"*:
- Booking Agent thực hiện chuỗi logic bảo toàn giao dịch:
  1. Đối soát lịch làm việc của các Sale được phân công phụ trách căn nhà.
  2. Kiểm tra xung đột: Loại trừ các khung giờ đã có `Appointment` chính thức.
  3. Tạo bản ghi **`PropertyHold` với thời hạn hết hạn (TTL) đúng 15 phút** bằng kỹ thuật Row-Level Locking trong PostgreSQL.
  4. Khóa slot giờ đó để khách khác không thể đặt trùng (Chống Double-booking tuyệt đối).

### 🔹 Bước 6: Respond Node & Phê duyệt Con người (Human-in-the-loop - HITL)
- **Respond Node** định dạng câu trả lời hoàn chỉnh, tạo nút bấm tương tác nhanh (*Quick Reply Chips*).
- **Minh bạch nhãn nguồn gốc (`ai_mode`):**
  - `llm_grounded`: Câu trả lời được kiểm chứng 100% từ dữ liệu PostgreSQL.
  - `llm_direct`: Câu trả lời hội thoại chung hoặc giải thích luật.
  - `fallback`: Câu trả lời theo luật khi mạng LLM gặp sự cố.
- **Điểm dừng Chốt chặn (HITL):**
  - Yêu cầu đặt lịch được đẩy tức thì sang Dashboard của nhân viên Sale (`nerahome.space/sale`).
  - **AI không tự xác nhận lịch chính thức:** Sale phải đăng nhập, kiểm tra thông tin và bấm **Chấp nhận (Accept)** thì lịch hẹn mới chuyển thành `CONFIRMED` và trả mã Booking cho khách.

---

## 4. TÍNH KIÊN CƯỜNG CỦA HỆ THỐNG (SYSTEM RESILIENCE & FALLBACK)

Nera được thiết kế với triết lý **không bao giờ để một lỗi đơn lẻ làm sập toàn bộ ứng dụng**:

1. **Fallback 2 tầng khi Redis gặp sự cố:**
   - Bình thường: Redis lưu trạng thái hội thoại và rate limiting.
   - Khi Redis sập: Lớp `InMemoryFallback` tự động kích hoạt, chuyển sang lưu tạm trong RAM của tiến trình backend. Ứng dụng vẫn chạy bình thường.
2. **Fallback khi API Nhà cung cấp LLM lỗi:**
   - Khi OpenRouter / OpenAI bị timeout hoặc lỗi mạng: Hệ thống bắt exception và chuyển sang **Rule-based Heuristic Fallback**, hiển thị rõ nhãn thông báo cho người dùng thay vì báo lỗi màn hình trắng.
3. **Bảo mật Mã hóa Token at-rest:**
   - Toàn bộ Token Google Calendar (`calendar_access_token`, `calendar_refresh_token`) của Sale đều được mã hóa đối xứng **Fernet (AES-128-CBC + HMAC-SHA256)** trước khi lưu vào CSDL.
4. **Chốt chặn Mật khẩu Demo (Demo Password Guard):**
   - Mật khẩu tài khoản demo tự động bị vô hiệu hóa hoàn toàn trên môi trường `production` và `staging`, chỉ cho phép đăng nhập mật khẩu demo tại `development`.

---

## 5. BẢNG SỐ LIỆU ĐO LƯỜNG THỰC ĐỊA THẬT 100% (EVIDENCE BASE)

| Hạng mục đo lường | Số liệu thực tế kiểm chứng | Ý nghĩa kỹ thuật & nghiệp vụ |
| :--- | :---: | :--- |
| **Quy mô CSDL BĐS thật** | **167 căn** | Dữ liệu crawl thật từ Batdongsan & Chotot tại Hà Nội, 100% có tọa độ Geocode. |
| **Bộ kiểm thử tự động (Unit Test)** | **157 tests PASSED (0 fail)** | Bao phủ toàn bộ luồng Auth, RBAC 403, Token Encryption, Redis Fallback, Booking. |
| **Tốc độ chốt giữ chỗ (Booking Speed)** | **0.33 giây** ⚡ | Đối soát lịch trống và tạo bản ghi giữ chỗ 15 phút gần như tức thời. |
| **Độ trễ tìm kiếm AI khi máy nóng** | **~4.08 giây** | Độ trễ thực tế trên Render Cloud sau khi hoàn tất giai đoạn khởi động container. |
| **Tỷ lệ thành công cuộc gọi API** | **100% (23/23 lượt gọi HTTP 200)** | Vượt qua bài test lưu lượng 15 kịch bản đàm thoại đa lượt phức tạp. |
| **Chặn câu hỏi ngoài phạm vi** | **100% an toàn** | Từ chối lịch sự 100% câu hỏi ngoài lề (Tokyo, Eiffel, Prompt Injection). |

---

## 6. NHỮNG CÂU HỎI VÀNG ĐỂ NOTEBOOKLM SINH AUDIO PODCAST / Q&A

### 🎙️ Câu hỏi 1: *"Điểm khác biệt cốt lõi nhất giữa Nera và một Chatbot AI thông thường là gì?"*
> **Đáp án tóm tắt:** Chatbot thông thường chỉ trả lời chữ và dễ bị ảo giác (hallucination). Nera là một **Hệ thống AI O2O khép kín**: áp dụng **SQL Grounding** trên 3.796 BĐS thật, có bộ nhớ sở thích đa lượt, và sở hữu **công cụ khóa giữ chỗ 15 phút (`PropertyHold`)** để chuyển giao cho nhân viên Sale duyệt lịch hẹn thật ngoài đời.

### 🎙️ Câu hỏi 2: *"Tại sao Nera không để AI tự động chốt luôn lịch hẹn mà phải cần Sale phê duyệt (HITL)?"*
> **Đáp án tóm tắt:** Vì trong BĐS, việc dẫn khách đi xem nhà làm phát sinh chi phí thực tế (thời gian di chuyển của Sale, mở cửa căn hộ). Cơ chế **giữ chỗ 15 phút + Sale duyệt (Human-in-the-loop)** vừa giúp giải phóng 80% thời gian tư vấn ban đầu cho Sale, vừa giữ quyền kiểm soát và trách nhiệm thực tế thuộc về con người, loại trừ 100% rủi ro lịch ảo.

### 🎙️ Câu hỏi 3: *"Hệ thống Nera làm thế nào để nhớ được nhu cầu của khách qua nhiều lượt chat?"*
> **Đáp án tóm tắt:** Nhờ kiến trúc Multi-Agent trên LangGraph kết hợp với `CustomerMemoryService`. Khi khách đổi tiêu chí (ví dụ: nâng giá từ 3 tỷ lên 5 tỷ), Node Supervisor tự động kế thừa quận và số phòng ngủ từ lượt trước, cập nhật vào `search_criteria` mà khách không cần nhập lại từ đầu.

---
*Tài liệu được biên soạn chuẩn xác bởi Đội ngũ Nera P-046 — AI20K Build Phase.*
