# HỒ SƠ DỰ ÁN NERA (P-046)

**Đội:** 046LTD — Vũ Thế Lực, Phạm Trung Kiên
**Sản phẩm:** Nera, trợ lý AI tìm nhà và đặt lịch xem nhà
**Chương trình:** AI20K Build Phase Cohort 3
**Bản chạy thật:** https://www.nerahome.space/
**Mã nguồn:** https://github.com/AI20K-Build-Phase-Cohort-3/P-046
**Số liệu trong hồ sơ này đo ngày:** 29/08/2026

Mọi con số dưới đây đều kèm cách kiểm chứng lại. Không có con số nào chép từ bản báo cáo cũ.

---

## Mục lục

1. [Bài toán và giải pháp](#1-bài-toán-và-giải-pháp)
2. [Kiến trúc và cơ chế vận hành](#2-kiến-trúc-và-cơ-chế-vận-hành)
3. [Phân công và đóng góp](#3-phân-công-và-đóng-góp)
4. [Số liệu đo được và cách kiểm chứng](#4-số-liệu-đo-được-và-cách-kiểm-chứng)
5. [Giới hạn đã biết](#5-giới-hạn-đã-biết)
6. [Đối chiếu phản hồi của mentor](#6-đối-chiếu-phản-hồi-của-mentor)
7. [Kịch bản thuyết trình 5 phút](#7-kịch-bản-thuyết-trình-5-phút)
8. [Câu hỏi phản biện](#8-câu-hỏi-phản-biện)
9. [Kế hoạch Phase 2](#9-kế-hoạch-phase-2)

---

## 1. Bài toán và giải pháp

### 1.1. Hai chỗ đứt gãy trong quy trình xem nhà

Người tìm nhà phải tự ghép thông tin từ hàng loạt tin đăng rời rạc. Bộ lọc trên các sàn hiện nay chỉ hiểu tiêu chí cứng như giá, số phòng, quận. Những nhu cầu thật của người mua thì không nằm gọn trong bộ lọc: gần chỗ làm, tiện đưa con đi học, chấp nhận xa trung tâm để đổi lấy diện tích. Mỗi lần quay lại tìm, họ nhập lại từ đầu.

Phía doanh nghiệp, việc điều phối lịch xem nhà chạy thủ công qua Zalo và tin nhắn. Hai Sale cùng nhận một khung giờ cho một căn là chuyện xảy ra thường xuyên, và mỗi lần trùng lịch là một lần khách mất thiện cảm.

### 1.2. Nera làm gì

Nera biến việc tìm nhà thành một cuộc hội thoại. Khách mô tả nhu cầu bằng câu nói thường ngày, hệ thống hỏi lại phần còn thiếu, giữ tiêu chí qua nhiều lượt, rồi truy vấn dữ liệu thật để trả về những căn phù hợp kèm lý do.

Khi khách chọn được căn muốn xem, Nera đối chiếu khung giờ rảnh của Sale trong cơ sở dữ liệu và khóa tạm căn đó trong 15 phút để tránh hai khách cùng đặt. Lịch chỉ thành chính thức sau khi Sale bấm duyệt. AI không tự chốt lịch với khách hàng thật.

---

## 2. Kiến trúc và cơ chế vận hành

```
[ Frontend: Next.js 14 / Vercel ]
        │ REST + SSE Streaming, HttpOnly Cookie
        ▼
[ Backend: FastAPI / Render ] ── [ Auth & RBAC: CUSTOMER, SALE, COORDINATOR, ADMIN ]
        │
        ▼
[ Multi-Agent Orchestration: LangGraph StateGraph ]
  ├── Supervisor Node      phân loại intent, giữ ngữ cảnh đa lượt
  ├── Inventory Agent      truy vấn 3.796 BĐS thật, lọc ràng buộc cứng
  ├── Booking Tools        đối chiếu slot, tạo yêu cầu đặt lịch
  └── Respond Node         sinh câu trả lời, gắn nhãn ai_mode
        │
        ├── LLM Service            OpenRouter, định tuyến model động
        ├── Goong Maps             Geocode, Distance Matrix, Nearby Search
        ├── Affordability Engine   tính khoản vay bằng công thức, không qua LLM
        └── CustomerMemoryService  PostgreSQL, cache qua Redis
```

### 2.1. Bốn vai trò và quyền tương ứng

| Vai trò | Làm được gì | Chặn ở đâu |
| :--- | :--- | :--- |
| `CUSTOMER` | Chat, tìm nhà, xem chi tiết, đặt lịch, quản lý lịch tại `/my-bookings` | |
| `SALE` | Nhận yêu cầu, duyệt hoặc từ chối lịch, xem lịch trình ngày tại `/sale` | `require_roles(UserRole.SALE)` |
| `COORDINATOR` | Phân bổ lại lịch khi Sale bận, xử lý hàng đợi HITL | `hitl_service.py:69` |
| `ADMIN` | Quản lý người dùng, khóa mở tài khoản, xem KPI tại `/admin` | `admin.py`, 6 endpoint |

Cả bốn vai trò đều đi qua một hàm gác duy nhất là `require_roles` trong `src/api/routes/auth.py`. Bộ test `tests/test_role_authorization.py` kiểm cả chiều từ chối lẫn chiều cho qua, vì một guard chỉ biết chặn mà chặn nhầm cả người đúng vai thì cũng hỏng.

### 2.2. Hệ thống hỏng từng phần thay vì sập

Redis mất kết nối thì `InMemoryFallback` trong `src/services/redis_service.py` tiếp quản, giữ trạng thái chat trong RAM tiến trình. Ứng dụng chạy tiếp, chỉ mất khả năng chia sẻ trạng thái giữa nhiều tiến trình.

LLM lỗi hoặc quá hạn chờ thì `supervisor_node` và `respond_node` bắt exception rồi rơi về nhánh luật cứng. Trạng thái này không bị giấu: API trả `ai_mode: fallback` và giao diện hiển thị nhãn tương ứng.

Tiền bạc không đi qua LLM. Toàn bộ phép tính khoản vay và khả năng chi trả nằm trong `src/services/affordability.py`, tất định, có 13 test phủ. Model chỉ được đọc lại con số đã tính, không được tự nhẩm.

---

## 3. Phân công và đóng góp

### 3.1. Vũ Thế Lực — PM, AI Product và Data Quality

Định hình nghiệp vụ sản phẩm: xây User Journey cho bốn nhóm người dùng, thiết kế cơ chế giữ căn 15 phút (`PropertyHold`) và luồng phê duyệt của Sale.

Quyết định sản phẩm về explainability (`feat(chat): confirm what Nera understood`): trước khi đổ danh sách nhà, Nera phải tóm tắt lại nó hiểu gì để khách kịp sửa. Khách thấy Nera hiểu sai ở dòng đầu và sửa bằng một câu, thay vì cuộn qua năm căn sai.

Chốt chặn trung thực (`fix(search): recognise rental vocabulary`): khi khách hỏi thuê mà kho chỉ có tin bán, Nera nói thẳng là chưa có dữ liệu thuê. Không trộn tin bán vào kết quả thuê để lấp chỗ trống.

Làm sạch dữ liệu (`fix(inventory): strip broker contact pitch`): bộ lọc bỏ số điện thoại và lời chào môi giới khỏi mô tả căn. Đo trên 59 tin thật, 46 tin có đoạn liên hệ, bộ lọc giữ lại 90% ký tự có nghĩa.

Bảo mật và chất lượng: mã hóa Fernet cho token Google Calendar lưu trong cơ sở dữ liệu, dựng bộ test tự động, chuẩn hóa hồ sơ dự án.

### 3.2. Phạm Trung Kiên — Tech Lead, AI Core và Fullstack

Kiến trúc multi-agent trên LangGraph: thiết kế StateGraph điều phối Supervisor, Inventory, Booking và RespondNode.

Tích hợp bản đồ: chuyển toàn bộ tầng địa lý từ Google Maps Platform sang Goong (Geocode, Distance Matrix, Nearby Search), thêm badge khoảng cách trên PropertyCard và khung bản đồ chỉ đường.

Engine tài chính `affordability.py`: thuật toán tính dòng tiền trả góp theo lãi suất và thời hạn vay.

Bảo mật và giao diện: chốt chặn mật khẩu demo theo môi trường, mật khẩu ngẫu nhiên cho tài khoản OAuth, global exception handler, đồng bộ nhận diện thương hiệu và dựng giao diện Next.js.

---

## 4. Số liệu đo được và cách kiểm chứng

### 4.1. Quy mô dữ liệu

3.796 bất động sản thật trên 27 tỉnh/thành trong cơ sở dữ liệu production, thu thập từ Nhà Tốt qua `database/crawler_chotot.py` và nạp bằng `database/004_crawled_data.sql`. Bốn thị trường lớn nhất: TP Hồ Chí Minh 2.449, Hà Nội 687, Bình Dương 330, Đà Nẵng 152.

Kiểm chứng: `GET https://bookingbot-api-q0t9.onrender.com/api/v1/properties?page_size=1` trả về trường `total`.

### 4.2. Độ trễ thật

| Luồng | Đo được | Ghi chú |
| :--- | ---: | :--- |
| Chốt lịch booking | 0,53s | Không gọi LLM |
| Chat tìm kiếm, production, máy đã nóng | 8–9s | Hai lượt gọi LLM mỗi turn |
| Chat tìm kiếm, lượt đầu sau cold start | ~16s | Render free tier ngủ sau 15 phút |
| Suite đánh giá lưu lượng, 23 lượt | avg 5,27s, P95 9,52s | `eval/results/DEMO_DAY_TRAFFIC_EVALUATION_REPORT.md` |

Release gate của đội đặt ở mức trung bình 4,0s và P95 6,0s. Cả hai chỉ số hiện chưa đạt, và báo cáo đánh giá ghi rõ trạng thái "Chưa đạt" thay vì làm tròn thành đạt. Nguyên nhân đã xác định, cách xử lý nằm ở mục 9.

### 4.3. Bộ kiểm thử

157 test pass, 0 fail. `ruff check src/ tests/` sạch. Chạy lại bằng `pytest` và `ruff check src/ tests/`.

Bộ test không phụ thuộc API key, cơ sở dữ liệu hay mạng, nên chạy được trên máy trống.

Một số test đáng nói:

`tests/test_role_authorization.py` kiểm khách hàng gọi endpoint của Sale và của Admin đều nhận 403, Sale gọi endpoint Admin cũng nhận 403, và đúng vai thì được đi qua.

`tests/test_redis_service.py` kiểm nhánh fallback in-memory: khóa phân tán, rate limit, và quan trọng nhất là hai khách không được giữ cùng một căn. Chính bộ test này phát hiện `acquire_hold` ở chế độ fallback đọc trạng thái từ một nơi rồi ghi vào nơi khác, nên chưa bao giờ thấy hold đang tồn tại.

`tests/test_geo_constraints.py` kiểm câu đặt lịch không bị đọc nhầm thành ràng buộc đi lại. Trước khi có test này, câu "đặt lịch 10h" sinh ra ràng buộc đi lại 600 phút.

`tests/test_token_encryption.py` kiểm token Google Calendar mã hóa và giải mã đúng, và bản mã không còn giữ tiền tố `ya29.` của token gốc.

`tests/test_llm_model_selection.py` kiểm câu trả lời khai đúng tên model đã chạy, và khai `null` khi lượt đó chạy bằng luật cứng thay vì mượn tên một model không tham gia.

### 4.4. Tình trạng production

`GET /health` trả `{"status":"ok","database":"ok","env":"production"}`. Một lượt chat thật trả về 20 bất động sản với `ai_mode: llm_grounded`.

---

## 5. Giới hạn đã biết

Phần này liệt kê những gì chưa xong, để người đọc không phải tự đi tìm.

**Độ trễ chưa đạt gate.** 8–9s so với mục tiêu 4,0s. Nguyên nhân là mỗi lượt tìm kiếm gọi LLM hai lần: một lần ở Supervisor để phân loại intent và trích tiêu chí, một lần ở Inventory để viết đoạn giới thiệu kết quả. Cộng thêm model đang dùng là bản miễn phí trên OpenRouter.

**Văn bản giới thiệu do LLM viết.** Thẻ bất động sản lấy nguyên số liệu từ cơ sở dữ liệu, không qua LLM. Nhưng đoạn văn giới thiệu phía trên thẻ thì do model viết lại từ payload gồm giá, diện tích, số phòng. Prompt cấm bịa số và có nhánh dự phòng tất định khi model lỗi, nhưng chưa có bước đối chiếu tự động giữa văn bản và dữ liệu gốc. Đây là đánh đổi có chủ đích để câu trả lời tự nhiên hơn.

**Goong không có chế độ đi bộ.** API chỉ hỗ trợ ô tô và xe hai bánh. Yêu cầu đi bộ hiện dùng hồ sơ xe đạp nên thời gian là ước lượng, không phải số đo. Mã nguồn ghi rõ chỗ này thay vì im lặng.

**Không có dữ liệu giao thông theo thời gian thực.** Distance Matrix của Goong không nhận tham số thời gian khởi hành, nên API trả `traffic_aware: false`. Bản Google trước đây có, bản hiện tại thì không, và hồ sơ không khai ngược lại.

**Thông báo ngoài ứng dụng chưa bật.** Mã cho email, SMS và Zalo đã có và chỉ kích hoạt khi có cấu hình tương ứng. Hiện chưa cấu hình nên chỉ còn thông báo trong ứng dụng.

**CI chưa chạy được.** 40 lần chạy gần nhất trên GitHub Actions đều dừng ở khâu cấp máy do hạn mức thanh toán của tổ chức, chưa lần nào tới bước lint. Đội chạy `pytest` và `ruff` tại máy trước mỗi lần đẩy code.

---

## 6. Đối chiếu phản hồi của mentor

| Vấn đề mentor nêu | Hiện trạng | Minh chứng |
| :--- | :---: | :--- |
| Schema cũ mâu thuẫn, thư mục MOCKUI chết, README hardcode đường dẫn Windows | Xong | Đã xóa `database/mvp/`, `README_boilerplate.md`, `MOCKUI/`. README dùng đường dẫn tương đối |
| Thiếu test cho service lớn, không có test từ chối quyền 403, test mem0 lấy lệ | Xong | 157 test pass. `test_role_authorization.py`, `test_redis_service.py`, `test_booking_service.py`, `test_token_encryption.py`. Test mem0 lấy lệ bị xóa thay vì vá |
| Token Calendar lưu plaintext, rò `str(e)` ra client, `/docs` mở ở production | Xong | `auth_service.py` mã hóa Fernet at-rest. `src/main.py` tắt Swagger ngoài môi trường development và có global exception handler. `logger.exception()` giữ chi tiết SQL ở phía máy chủ |
| Lỗi ruff thiếu import `Path` làm crash auto-seed | Xong | `src/main.py` import `from pathlib import Path`, auto-seed chạy bình thường |
| `verify_password` nhận mật khẩu demo ở mọi môi trường | Xong | `auth_service.py` chặn bằng `if settings.app_env != "development": return False` |
| Tài khoản Google OAuth có mật khẩu đoán được `gauth_{email}` | Xong | `google_oauth.py` sinh ngẫu nhiên bằng `secrets.token_urlsafe(32)`, có test hồi quy |

---

## 7. Kịch bản thuyết trình 5 phút

### Phút 1 — Bài toán (Lực)

"Em là Vũ Thế Lực, nhóm P-046, sản phẩm Nera: trợ lý AI tìm nhà và đặt lịch xem nhà.

Người tìm nhà hôm nay gặp hai chuyện. Thứ nhất, họ bị ép vào bộ lọc cứng và mất ngữ cảnh mỗi lần tìm lại. Thứ hai, việc điều phối lịch xem nhà chạy thủ công qua tin nhắn nên trùng lịch xảy ra thường xuyên.

Nera giải quyết bằng multi-agent, grounding trên 3.796 bất động sản thật, và cơ chế người duyệt cuối."

### Phút 2 đến 3 — Kiến trúc và demo (Kiên)

"Hệ thống đang chạy tại nerahome.space. Giao diện Next.js gọi FastAPI. Trên đó là LangGraph điều phối bốn agent: Supervisor giữ ngữ cảnh, Inventory lọc nhà, Booking quản lý slot, Respond sinh câu trả lời. Dữ liệu nằm trong PostgreSQL, Redis giữ trạng thái chat.

*(Demo trực tiếp)*

Khách gõ: 'Tìm căn 2PN ở Cầu Giấy dưới 3 tỷ, đi xe đến Đại học Quốc gia dưới 10 phút.'

Nera tóm tắt lại tiêu chí nó hiểu được. Khách xác nhận. Hệ thống gọi Goong đo khoảng cách thật rồi trả về thẻ nhà có trong cơ sở dữ liệu, kèm bản đồ.

Khách chọn đặt lịch 9 giờ sáng. Hệ thống tạo bản ghi giữ căn 15 phút.

Chuyển sang màn hình `/sale`. Sale nhận yêu cầu, bấm duyệt. Lúc này lịch mới thành chính thức."

### Phút 4 đến 5 — Kỷ luật kỹ thuật và kế hoạch (Lực)

"Điểm nhóm em muốn nói không phải là danh sách tính năng, mà là cách nhóm xử lý những chỗ chưa tốt.

AI không tự chốt lịch. Sale là người duyệt cuối, vì mỗi lịch xem nhà tiêu tốn thời gian di chuyển thật của một người thật.

Hệ thống hỏng từng phần chứ không sập. Redis mất thì chuyển sang in-memory. LLM lỗi thì rơi về luật cứng, và nhãn `ai_mode: fallback` hiện ra cho người dùng thấy.

Bộ test hiện có 157 case pass, ruff sạch. Trong lượt rà gần nhất, chính bộ test phát hiện một lỗi thật: ở chế độ fallback, hai khách có thể giữ cùng một căn. Lỗi đã sửa và có test chặn.

Về độ trễ, nhóm đo được 8 đến 9 giây trên bản cloud miễn phí, chưa đạt mức 4 giây nhóm tự đặt. Nguyên nhân là hai lượt gọi LLM mỗi turn. Phase 2 rút còn một lượt và bật cache prompt.

Nhóm chọn nói thẳng con số này thay vì làm tròn nó."

---

## 8. Câu hỏi phản biện

**Tại sao không để AI tự chốt lịch cho nhanh?**

Mỗi lịch xem nhà phát sinh chi phí thật: Sale di chuyển, chủ nhà mở cửa, đôi khi có xe đưa đón. Nếu AI tự chốt thì chỉ cần khách spam hoặc AI hiểu nhầm là lãng phí nguồn lực của người khác. Giữ căn 15 phút cộng với Sale duyệt là điểm cân bằng: AI lo phần sàng lọc ban đầu, trách nhiệm cuối vẫn thuộc về con người.

**Làm sao đảm bảo AI không bịa giá nhà hay địa chỉ?**

Cần tách làm hai phần vì hai phần này có mức đảm bảo khác nhau.

Thẻ bất động sản hiển thị cho khách lấy nguyên số liệu từ PostgreSQL, không đi qua LLM. Giá, diện tích, số phòng, địa chỉ trên thẻ không thể lệch so với cơ sở dữ liệu.

Đoạn văn giới thiệu phía trên thẻ thì do model viết, dựa trên payload chứa đúng những con số đó. Prompt cấm bịa số và có nhánh dự phòng tất định khi model lỗi. Nhưng nhóm chưa có bước đối chiếu tự động giữa văn bản và dữ liệu gốc, nên đây là điểm nhóm ghi nhận là còn hở, và là hạng mục P1 trong Phase 2.

Ngoài ra, LLM không có quyền truy vấn cơ sở dữ liệu. Nó chỉ trích xuất tiêu chí, backend mới là bên chạy câu truy vấn.

**Nếu OpenRouter timeout hoặc Redis sập thì sản phẩm chết không?**

Không. Redis sập thì `InMemoryFallback` giữ trạng thái trong RAM tiến trình, ứng dụng chạy tiếp và chỉ mất khả năng chia sẻ trạng thái giữa nhiều tiến trình. LLM lỗi thì hệ thống rơi về nhánh luật cứng và trả `ai_mode: fallback`, người dùng nhìn thấy nhãn đó chứ không bị lừa rằng AI vẫn đang trả lời.

Cả hai nhánh fallback đều có test. Nhóm không tin vào một nhánh dự phòng chưa từng được chạy qua.

**Khác gì so với bộ lọc trên Batdongsan.com.vn?**

Bộ lọc hiểu tiêu chí cứng và bắt người dùng nhập lại từ đầu mỗi phiên. Nera giữ tiêu chí qua nhiều lượt và hiểu nhu cầu mềm: "tìm căn vừa tiền cho vợ chồng mới cưới, gần viện Bạch Mai để tiện đi làm". Khách đổi một tiêu chí thì những tiêu chí còn lại vẫn giữ nguyên.

Điểm khác thứ hai là Nera nói thẳng khi không có dữ liệu. Khách hỏi nhà cho thuê mà kho chỉ có tin bán thì Nera trả lời là chưa có, không trộn tin bán vào cho đủ số.

**Vì sao chuyển từ Google Maps sang Goong?**

Chi phí và phạm vi phủ dữ liệu Việt Nam. Đánh đổi là Goong không có chế độ đi bộ và không nhận tham số thời gian khởi hành, nên nhóm bỏ luôn tuyên bố về dữ liệu giao thông theo thời gian thực thay vì giữ một cái nhãn không đúng.

---

## 9. Kế hoạch Phase 2

**P0 — Kéo độ trễ xuống dưới 4 giây.** Gộp hai lượt gọi LLM mỗi turn thành một, bật prompt caching, và cân nhắc model trả phí có độ trễ ổn định hơn bản miễn phí hiện tại.

**P1 — Đối chiếu văn bản với dữ liệu gốc.** Thêm bước kiểm sau khi model sinh đoạn giới thiệu: mọi con số xuất hiện trong văn bản phải khớp với payload, lệch thì rơi về bản tất định. Việc này đóng lại điểm hở đã nêu ở mục 5.

**P2 — Mở rộng dữ liệu.** Bổ sung tin cho thuê và mở rộng phạm vi quận huyện, vì hiện tại kho chỉ có tin bán.

**P3 — Đồng bộ lịch hai chiều.** Tạo sự kiện trực tiếp trong Google Calendar của Sale sau khi lịch được duyệt.

**P4 — Bật lại CI.** Cần hạn mức GitHub Actions của tổ chức. Chưa có CI thì lỗi chỉ được phát hiện khi có người chạy tay, và đó là lý do một số lỗi ở lượt rà gần nhất lọt được vào nhánh develop.
