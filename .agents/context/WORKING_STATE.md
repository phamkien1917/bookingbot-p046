# Goal

Nera (P-046) — trợ lý AI tìm nhà qua hội thoại, Team 046 LTD, chạy thật tại https://www.nerahome.space/
Giai đoạn hiện tại: hoàn thiện chất lượng hội thoại và độ trung thực của câu trả lời trước Demo Day.

# Current Task

**Cây đang đỏ, cần sửa trước khi làm tiếp.** Xem mục Open Issues.
4 commit chưa đẩy lên origin/develop.

# Relevant Files

Ba việc gần nhất (26/08), đều đã trên origin/develop:

- `frontend/src/app/chat/page.tsx` — thẻ xác nhận hiểu (`UnderstandingCard`). Nera hiện lại nhu cầu vừa nắm được; khách bấm mới đổ danh sách nhà. Gate theo từng tin nhắn bằng `revealedCards`, ảnh chụp `insights` gắn theo message chứ không đọc state chung.
- `src/utils/property_text.py` — `clean_property_description()`. Lọc theo từng câu, bỏ số điện thoại/lời chào môi giới. Cắm ở đúng hai chỗ: `serialize_property_item()` và validator của `PropertySchema`.
- `src/services/search_criteria_service.py` — `rent_signal` mở rộng (*phòng trọ, ở ghép, ký túc xá, tìm phòng*), có lookahead chặn nhầm "phòng ngủ".
- `src/agents/nodes/inventory_agent.py` — `count_rental_listings()`. Kho không có tin thuê nào thì nói thẳng, không gợi ý sửa tiêu chí.
- `src/services/affordability.py` — toàn bộ tính toán tiền bạc là tất định, LLM không được tự nhẩm ngân sách.

# Decisions

- **Đơn vị bán (mô hình tài chính lab Day 24):** ghế môi giới tại sàn, không bán cho người mua nhà. Hybrid 390k cố định + ~200k usage = ARPU 590k. Chi phí ẩn gấp 2,04 lần tiền API — Google Maps chiếm ~45% tiền API vì gọi ba SKU riêng (Geocoding, Routes, Places).
- **Thẻ xác nhận trước danh sách:** khách thấy Nera hiểu sai ở dòng đầu và sửa bằng một câu, thay vì cuộn qua năm căn sai.
- **Không trộn tin bán vào kết quả thuê**, kể cả khi kết quả rỗng.
- `AgentState` là TypedDict không có Annotated reducer — nên merge delta từ `astream(stream_mode="updates")` tương đương `ainvoke`.
- Giữ tên kỹ thuật cũ `bookingbot`/`visitops` (cookie, user DB, subdomain Render). Đổi sẽ hỏng phiên đăng nhập đang chạy.

# Completed

- Thẻ xác nhận hiểu + gate danh sách nhà theo từng lượt.
- Bộ lọc văn rác mô tả căn (đo trên 59 tin thật: 46 tin có đoạn liên hệ; giữ 90% ký tự).
- Từ vựng thuê + câu trả lời thật khi kho không có tin cho thuê.
- Merge develop vào main (main từng tụt 20 commit); xung đột duy nhất là README, lấy bản Nera.
- Sửa `F821 Undefined name Path` trong `src/main.py` — sinh ra do lấy chéo cả file từ main sang develop.
- Bài lab Day 24 (mô hình tài chính) ở `d:\AITHUCCHIEN\Track1-Day24-MHV-2A202602008-VuTheLuc\`.

# Validation

Trạng thái tốt gần nhất — 27/08, trước các commit ngày 28:

- `ruff check src/ tests/` → All checks passed
- `pytest tests/` → 123 passed
- frontend `npm run lint` → 0 lỗi (12 cảnh báo `<img>` cũ)
- `npm run build` → Compiled successfully

**Chạy bằng `py -3.12`, không phải `py`.** Máy đã cài thêm Python 3.13 và nó không có các gói của dự án.

# Open Issues

1. **`tests/test_booking_service.py` import hàm không tồn tại.** Nó gọi `get_available_slots`, nhưng `src/services/booking_service.py:133` định nghĩa `list_available_slots`. Đây là lỗi thật, không phải môi trường.
2. **Thiếu gói `cryptography`** trong môi trường 3.12 → 9 test module không thu thập được. Sửa: `py -3.12 -m pip install -r requirements.txt`.
3. **62 lỗi ruff** trong file mới thêm — 46 cái tự sửa được (`ruff check --fix`), phần lớn là W293/I001/F401. Còn 7 F841 biến thừa và 11 E402 import không ở đầu file phải sửa tay.
4. **CI của repo chết 40/40 lần chạy gần nhất.** Không phải lỗi mã: *"recent account payments have failed or your spending limit needs to be increased"* — hạn mức GitHub Actions của org `AI20K-Build-Phase-Cohort-3`. Job chết ở khâu cấp máy nên chưa từng chạy tới bước lint. Đây là lý do lỗi số 1 và 3 lọt được vào nhánh. Cần BTC xử lý.
5. **Bộ eval release của Kiên không gọi LLM.** `multiturn_extended` báo 12/12 và median 58ms, nhưng `ai_latency_ms` chỉ 1–17ms và nội dung trả về là template tĩnh — agent rơi vào nhánh heuristic dự phòng. Baseline không có trường `ai_latency_ms` nên hai lần chạy không so trực tiếp được. **Không đưa hai con số này vào slide Demo Day trước khi Kiên xác nhận.**
6. **Production thiếu commit.** Render kéo từ repo cá nhân `phamkien1917/bookingbot-p046`, không phải repo tổ chức. Cần Kiên đồng bộ.
7. **Backend production trả 503** lúc kiểm 27/08 (`/api/v1/health`). Chưa rõ là Render ngủ đông hay DB thật sự mất.
8. **Lỗ hổng xác thực chưa vá (cố ý).** `verify_password` chấp nhận `Demo@123` / `123456` cho mọi tài khoản có hash `DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH`, **không kiểm `APP_ENV`**. 10 tài khoản seed dùng hash này. Chặn sẽ làm hỏng đăng nhập Sale khi demo. README đã sửa để thôi tuyên bố có guard.
9. **`ai_model` trong response là hằng số.** `supervisor.py` gán cứng `"gpt-4o-mini"` và không bao giờ gán lại. Trace thật cho thấy model đang chạy là `nvidia/nemotron-3-ultra-550b-a55b:free`. Hồ sơ nộp đang khai sai model.

# Next Action

1. `py -3.12 -m pip install -r requirements.txt`
2. Sửa tên hàm trong `tests/test_booking_service.py` → `list_available_slots`
3. `py -3.12 -m ruff check src/ tests/ --fix` rồi sửa tay phần còn lại
4. Chạy lại `pytest` cho về xanh, rồi đẩy 4 commit đang treo

# Ghi chú bàn giao

`CHAT_EXPORT.md` cùng thư mục là bản rút gọn của phiên Claude Code (848 lượt, lọc từ 55 MB JSONL, đã bỏ toàn bộ tool call). Đọc file này khi cần bối cảnh vì sao một quyết định được đưa ra; đọc `WORKING_STATE.md` khi chỉ cần biết hiện trạng.
