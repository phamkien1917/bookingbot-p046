# Vũ Thế Lực — Product Manager & AI Product Lead

**Dự án:** Nera — Trợ lý AI bất động sản & đặt lịch xem nhà O2O (P-046 / 046LTD)
**Bản chạy thật:** <https://www.nerahome.space/>
**Mã nguồn:** [AI20K-Build-Phase-Cohort-3/P-046](https://github.com/AI20K-Build-Phase-Cohort-3/P-046)
**Đóng góp trong git:** 102 commit · trải trên tài liệu, kiểm thử, dữ liệu, agent và frontend

---

## Vai trò trong một câu

Trong khi Tech Lead trả lời câu hỏi *"làm sao hệ thống chạy được"*, phần việc của
tôi trả lời câu hỏi khó hơn với một sản phẩm AI: **"làm sao biết nó đúng, và nó
tốn bao nhiêu?"**

Ba thứ tôi mang vào dự án đều bắt đầu từ một chỗ trống có thể chỉ ra được:

| Trước | Sau | Kiểm chứng |
|:---|:---|:---|
| 168 tin đăng, một tỉnh | **3.796 căn, 27 tỉnh thành** | `GET /api/v1/properties` trên production |
| Chi phí mỗi lượt là mô hình trên giấy | **13,9 đ/lượt, đo thật** | `src/services/token_usage.py` |
| 222 kịch bản golden không có gì chạy chúng | **844 test trong CI** | `python -m pytest tests/ -q` |

---

## 1. Dữ liệu: từ 168 lên 3.796 căn

Kho ban đầu có 168 tin ở Hà Nội. Con số đó đủ để demo và không đủ để một khách
thật tìm được nhà — hỏi "2 phòng ngủ Cầu Giấy dưới 5 tỷ" là hết hàng.

**Cách tôi tìm ra nút thắt không phải bằng phỏng đoán mà bằng đo.** Tôi cho
crawler xuất ra báo cáo lý do loại tin, và nó chỉ thẳng: **3.698 trên 4.814 tin
bị loại chỉ vì thiếu trường "số tầng"** — một trường không ai lọc theo. Nới đúng
điều kiện đó, kèm mở rộng sang toàn quốc, kho nhảy lên 3.796 căn.

- [`database/crawler_chotot.py`](../database/crawler_chotot.py) — crawl Nhà Tốt
  toàn quốc, `region_v2` để trống nghĩa là không giới hạn tỉnh
- [`database/merge_crawls.py`](../database/merge_crawls.py) — gộp nhiều đợt
  crawl, khử trùng theo `property_id`, có self-check chạy được
- [`database/010_province_normalization.sql`](../database/010_province_normalization.sql)
  — gộp `'Hồ Chí Minh'` và `'Tp Hồ Chí Minh'` về một tên
- [`tests/test_crawl_pipeline.py`](../tests/test_crawl_pipeline.py) — 40 test cho
  đường ống này

**Bốn thị trường lớn nhất:** TP Hồ Chí Minh 2.449 · Hà Nội 687 · Bình Dương 330 ·
Đà Nẵng 152.

Kèm theo là trường `last_verified_at`: một tin được xác minh còn sống lúc nào thì
ghi lúc đó, tách khỏi `updated_at`. Tin quá 30 ngày bị đánh dấu `is_stale` và nói
rõ với khách, thay vì trình bày như tin mới — xem
[`src/utils/freshness.py`](../src/utils/freshness.py).

---

## 2. Chi phí: trục duy nhất không đo được, giờ đo được

Khung Accuracy–Performance–Cost có ba trục. Hai trục đầu có số. Trục Cost thì
không: **nhà cung cấp trả về khối `usage` trong mọi lời gọi và không ai đọc nó**,
nên mọi con số chi phí của đội đều là mô hình tự dựng.

Đọc từ giá trị trả về không đủ. `with_structured_output` trả về object đã parse,
không mang `usage` — nghĩa là **toàn bộ lời gọi của supervisor bị đếm sót**. Bộ
đếm móc vào `on_llm_end`, sự kiện bắn ở ranh giới model bất kể hàm trả về hình gì,
và sống trong `ContextVar` vì một client dùng chung phục vụ nhiều lượt chat song
song.

📄 [`src/services/token_usage.py`](../src/services/token_usage.py) ·
[`tests/test_token_usage.py`](../tests/test_token_usage.py)

**Đo trên hai lượt thật:** 4294/210 và 4956/280 token, trong đó 4096 token input
được phục vụ từ cache cả hai lần, **một lời gọi LLM mỗi lượt** chứ không phải hai
như mô hình giả định. Ra 13,9 đ/lượt so với 13 đ mô hình — nhưng khoảng 97 đ cho
một hội thoại bảy lượt so với 240 đ mô hình.

Bốn trường `input_tokens`, `output_tokens`, `cached_input_tokens`, `llm_calls`
giờ nằm trong mọi phản hồi của `/api/v1/chat` và có test giữ để không ai gỡ đi.

---

## 3. Đánh giá: ba hành vi không được phép sai

Rà repository theo khung Accuracy–Performance–Cost, tôi tìm ra ba hành vi nghiêm
trọng **không có một bài test nào đứng sau**. Cả ba hôm nay đều đúng — điều đáng
lo là không có gì ngăn ngày mai chúng sai.

| Hành vi | Vì sao nghiêm trọng | Test |
|:---|:---|:---|
| Goong lỗi → nói chưa xác minh, không bịa số km | Một khoảng cách bịa dẫn khách đi xem nhà sai | [`test_geo_tool_failure.py`](../tests/test_geo_tool_failure.py) |
| AI không bao giờ nói "sale đã duyệt" khi chưa duyệt | Lịch ảo làm mất uy tín cả sàn | [`test_hitl_no_false_confirmation.py`](../tests/test_hitl_no_false_confirmation.py) |
| Hai khách không giữ chỗ cùng một căn | Hai người cùng đến xem một căn lúc 9h | [`test_property_hold_concurrency.py`](../tests/test_property_hold_concurrency.py) |

Bài test HITL không so chuỗi cứng: nó quét **mọi literal node booking có thể phát
ra và mọi giá trị của động từ nội suy**, nên một nhánh mới trong tương lai mà
tuyên bố sale đã duyệt sẽ làm đỏ build.

**222 kịch bản golden trong `eval/` chưa từng được thứ gì trong CI chạy** — chúng
chỉ có một runner nói HTTP với server thật. Đo trước khi viết cho thấy bộ trích
xuất regex thuần quyết định **toàn bộ 124 khoá tiêu chí của 67 ca single-turn, 0
mâu thuẫn**, nên nửa đó thành cổng chặn PR không cần database và không cần model.
📄 [`tests/test_golden_set.py`](../tests/test_golden_set.py)

Báo cáo rà soát đầy đủ, gồm cả những chỗ tài liệu nói khác mã nguồn:
📄 [`docs/evaluation/NERA_EVALUATION_AUDIT.md`](evaluation/NERA_EVALUATION_AUDIT.md)

---

## 4. Quan sát hệ thống: tách thời gian AI khỏi thời gian bản đồ

Tích hợp Langfuse ban đầu là no-op — tôi phát hiện khi rà lại commit sau buổi
mentor review. Sửa lại thành helper `_trace_callbacks()` có cache trong
[`src/agents/graph.py`](../src/agents/graph.py), bỏ import lồng trong hàm và bỏ
việc ghi đè `os.environ` mỗi request.

Mỗi lượt gắn `langfuse_session_id` và `langfuse_user_id` để dashboard gom cả
phiên chat lên một dòng thời gian, thay vì rải ra thành các trace rời. Bọc
`GeoService.enrich_and_filter` bằng lớp đo riêng, nên **thời gian gọi Goong tách
hẳn khỏi thời gian LLM** — không có nó thì mọi cuộc bàn về độ trễ đều đoán mò.

📄 [`docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md`](demo/LANGFUSE_OBSERVABILITY_DEMO.md)

---

## 5. Sửa lỗi từ phản hồi người dùng thật

| Lỗi | Nguyên nhân gốc | Sửa |
|:---|:---|:---|
| Đặt "ngày 15" khi đã qua 15 → nhảy sang **2027** | Ngày quá khứ tự cộng một năm không giới hạn | Chặn ở chân trời 180 ngày, hỏi lại khách |
| Chọn khung giờ xong không thoát ra được | Pha chọn slot không có đường thoát | Nhận diện ý bỏ cuộc và đổi ngày, giải phóng pha |
| Đặt 3h chiều, hệ thống chốt giờ khác | Giờ không khớp bị bỏ qua âm thầm | Hỏi xác nhận thay vì tự chốt |
| "công viên gần đây" bị geocode như tên riêng | Bộ lọc từ đệm có `gan` nhưng thiếu `day` | Thêm một từ vào biểu thức chính quy |

📄 [`src/services/chat_state_service.py`](../src/services/chat_state_service.py) ·
[`src/agents/nodes/booking_agent.py`](../src/agents/nodes/booking_agent.py) ·
[`tests/test_booking_slot_phase.py`](../tests/test_booking_slot_phase.py)

---

## 6. Bài toán kinh doanh

Khảo sát **20 môi giới và người mua thật**, không phải persona tự nghĩ.

- **85% môi giới gặp trùng lịch ít nhất một lần trong ba tháng.** Thiệt hại họ tự
  khai cho *một* lần: 8.000.000đ · 6.500.000đ · 5.000.000đ · 2.000.000đ
- **Cost/Job ≈ 5.000đ** để AI làm xong một lịch hẹn được duyệt. Phát hiện đáng
  chú ý: **phút duyệt của con người tốn gần gấp đôi tiền LLM** — muốn giảm chi
  phí thì phải rút ngắn thao tác duyệt của sale, không phải đổi model rẻ hơn
- **Giá 300k/seat/tháng ra từ hai hướng tính độc lập:** từ dưới lên bằng
  Cost/Job × 3, và từ trên xuống bằng trung vị sẵn sàng chi trả. Hai đường không
  liên quan cùng chỉ vào một con số — đó là lý do tin được nó

📄 [`docs/research/MONETIZATION_ONE_PAGER.md`](research/MONETIZATION_ONE_PAGER.md) ·
[`docs/research/COST_MODEL.md`](research/COST_MODEL.md) ·
[`docs/research/FIELD_SURVEY.md`](research/FIELD_SURVEY.md)

---

## 7. Hồ sơ nộp bài

Toàn bộ 10 deliverable, đặt đúng đường dẫn Ban Tổ Chức mô tả:
[`architecture.md`](architecture.md) · [`evaluation.md`](evaluation.md) ·
[`journal.md`](journal.md) · [`worklog.md`](worklog.md) ·
[`video-demo.md`](video-demo.md) · [`pitch-deck.pdf`](pitch-deck.pdf)

Worklog dựng lại từ `git log` cho **28 ngày**, mỗi dòng kèm commit hash để đối
chiếu — trước đó chỉ có 9 ngày và tên 2 trên 4 thành viên.

---

## Nguyên tắc làm việc

**Đo trước khi sửa.** Nút thắt crawler tìm ra bằng báo cáo lý do loại tin, không
phải bằng đoán. Nửa bộ golden đưa được vào CI vì đo trước cho thấy regex đã quyết
định đủ 124 khoá.

**Không có số thì ghi là không có số.** Báo cáo đánh giá ghi `NOT MEASURED` ở chỗ
chưa đo, và nói thẳng coverage 52,79% chưa đạt mốc 60% cùng lý do, thay vì viết
test rỗng để đẩy con số.

**RAGAS bị loại có lý do ghi lại.** Hai trong bốn chỉ số của nó chấm khâu truy hồi
tài liệu — Nera không có vector store, kết quả đến từ SQL. Chạy chúng vẫn ra số,
nhưng con số đó không đo gì cả. Hai chỉ số còn lại được đo bằng cách xác định,
không để một mô hình chấm điểm cho một mô hình.
