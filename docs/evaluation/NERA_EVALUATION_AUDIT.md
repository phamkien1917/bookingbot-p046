# Nera — Phase 1: Repository & AI Evaluation Audit

**Ngày:** 01/09/2026 · **Phạm vi:** audit, chưa sửa code
**Nguyên tắc:** repository là nguồn sự thật. Chỗ nào tài liệu lệch code, code thắng.

---

## 0. Lệch so với context được cung cấp

Bốn chỗ context trong đề bài không khớp repository. Ghi lại vì chúng đổi cả thiết kế eval.

| Context | Thực tế trong repo/production | Bằng chứng |
| :--- | :--- | :--- |
| "167 bất động sản thật tại Hà Nội" | **3.796 căn, 27 tỉnh/thành** (TPHCM 2.449 · Hà Nội 687 · Bình Dương 330 · Đà Nẵng 152) | `GET /api/v1/properties` trên production, 01/09/2026 |
| "khoảng 157 unit tests" | **253 test** | `pytest --collect-only -q` |
| Node: Supervisor, Inventory, Booking, RespondNode | Còn thêm **`assignment`** và **`hitl`** là node thật trong graph | `src/agents/graph.py:68–73` |
| `ai_mode` có `llm_intent` | Giá trị này **không bao giờ được gán**, chỉ nằm trong comment và docstring | grep toàn `src/`: 3 giá trị thật là `llm_grounded`, `llm_direct`, `fallback` |

Hệ quả cho eval: golden set **không được giới hạn ở Hà Nội**, và **phải phủ hai node `assignment`/`hitl`** mà đề bài bỏ sót.

---

## 1. Trajectory thực tế

Tên node lấy nguyên từ `build_agent_graph()` — `src/agents/graph.py:63–99`.

```
POST /api/v1/chat  (hoặc /chat/stream)
        ↓
  rate limiter (Redis, 120 req/60s)
        ↓
  build_agent_graph().ainvoke(state)
        ↓
    supervisor            ← entry point
        ↓ route_from_supervisor
   ┌────┴─────┬───────────┬────────┬─────────┐
inventory  booking   assignment   hitl    respond ──→ END
   │          │           │         ↑
   │          └───────────┴─────────┘  _route_after_worker:
   │                                    "hitl" nếu state["awaiting_human"]
   └────────────────────────────────→ respond
```

| Bước | Node / hàm | Vào | Ra | Tool | Failure mode chưa được chặn |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `supervisor_node` | `query`, lịch sử | `intent`, `criteria`, `requested_date/hour`, `ordinal` | LLM structured output, regex fast-path | Phân loại sai intent; nuốt constraint; đọc "3 giờ chiều" thành số thứ tự |
| 2 | `inventory_agent` | `criteria` | `search_results`, `distance_evidence` | SQL, Goong DistanceMatrix | Lọc sai; xếp hạng sai; khẳng định khoảng cách khi Goong lỗi |
| 3 | `booking_agent` | `current_property_id`, ngày/giờ | slot, `tour_request` | `list_available_slots`, `PropertyHold` | Đặt sai giờ; kẹt phase; hold hết hạn vẫn dùng |
| 4 | `assignment_agent` | property, slot | sale phụ trách | SQL | Gán sale không phụ trách căn đó |
| 5 | `hitl_agent` | `awaiting_human` | hitl case | SQL | Nói "đã xác nhận" khi sale chưa duyệt |
| 6 | `respond_node` | toàn bộ state | `response`, `ai_mode` | LLM | Diễn đạt vượt quá dữ liệu đang có |

Mọi node bọc trong `_timed()` (`graph.py:39`) → ghi `stage_timings[node] = ms`.

---

## 2. Kiểm thử hiện có — 253 test

### Phân loại

| Loại | Số test | Ví dụ |
| :--- | ---: | :--- |
| **A. Deterministic unit** | ~200 | `test_crawl_pipeline` (40), `test_search_criteria_service` (25), `test_chat_state_service` (17), `test_freshness` (10) |
| **B. Agent behavioral** | ~35 | `test_rental_honesty` (3), `test_booking_slot_phase` (15), `test_geo_constraints` (8), `test_hitl_case_reuse` (4), `test_stage_timings` (4) |
| **C. Integration** | ~10 | `test_booking_service` (12, có DB), `test_property_hold_service` (2) |
| **D. End-to-end** | **0** | Không có test nào chạy trọn graph từ `query` tới `response` |
| **E. Eval / gold-set trong pytest** | **0** | 222 kịch bản có tồn tại nhưng nằm ngoài pytest — xem mục 3 |

### Bảng phủ theo năng lực

| Năng lực | Unit | Integration | Eval | Khoảng trống |
| :--- | :---: | :---: | :---: | :--- |
| Trích xuất constraint | ✅ 25 | — | ✅ 82 case | Đủ tốt |
| Trung thực thuê/bán | ✅ 3 | — | ✅ | Ổn |
| Xếp hạng kết quả | ❌ | ❌ | ❌ | **Không có gì** |
| Chọn đúng tool | ❌ | ❌ | ❌ | **Không có gì** |
| Goong lỗi → không bịa | ❌ | ❌ | ⚠️ `geo_grounded` chỉ khi tool chạy được | **Không mô phỏng lỗi tool** |
| PropertyHold tranh chấp | — | ⚠️ 2 test qua unique index | ❌ | **Không có test đồng thời thật** |
| HITL chống xác nhận giả | ⚠️ 5 test về vòng đời case | ❌ | ❌ | **Không test câu "đã xác nhận"** |
| Chuỗi node (trajectory) | ❌ | ❌ | ❌ | **Không có gì** |
| Token / cost | ❌ | ❌ | ❌ | **Không đo runtime** |

---

## 3. Tài sản eval đã có — bị bỏ quên

Repo **đã có 222 kịch bản**, nhiều hơn con số 20–30 mà đề bài yêu cầu tạo mới:

| File | Số case | Cấu trúc |
| :--- | ---: | :--- |
| `eval/chat_agent_acceptance.json` | 150 | `id`, `category`, `turns`, `expect` |
| `eval/chat_scenarios.json` | 60 | `id`, `category`, `authenticated`, `turns`, `assertions` |
| `eval/chat_agent_multiturn_extended.json` | 12 | `id`, `category`, `turns`, `expect_turns` |

Nhóm theo category (bộ 150): location 15 · hard_filter 15 · multi_turn 15 · geo 12 · persona 10 · property_kind 10 · budget 10 · reference 10 · consultation 10 · safety 10 · transaction 8 · language 8.

**Các phép khẳng định đang dùng** (đếm trên 150 case): `criteria_equals` 82 · `no_property_cards` 32 · `contains_any` 21 · `response_non_empty` 19 · `property_all` 18 · `not_contains` 14 · `geo_grounded` 12 · `search_pool_min` 11 · `auth_required` 8 · `criteria_absent` 6 · `min_properties` 6 · `max_properties` 6 · `round_trip_ms_lte` 4.

### Ba vấn đề

**Không nằm trong CI.** `.github/workflows/ci.yml` chỉ chạy `ruff check src/ tests/` và `pytest tests/`. Bộ 222 kịch bản không bao giờ tự chạy.

**Cần server sống.** `scripts/run_chat_agent_eval.py` gọi HTTP qua `urllib` tới `BOOKINGBOT_API_BASE`. Không chạy in-process được nên không cắm vào pytest như hiện trạng.

**Chấm điểm đến, không chấm hành trình.** Mọi trường `expect` đều nhìn kết quả cuối: criteria, số card, chuỗi trong câu trả lời. Không trường nào kiểm tra node nào đã chạy, tool nào được gọi với tham số gì, hold ở trạng thái nào, HITL đã chuyển trạng thái đúng chưa.

> Đây là kết luận chính của Phase 1: Nera **không thiếu kịch bản**. Nera thiếu **chấm trajectory** và **tự động hoá**.

---

## 4. Observability

### Đang có

| Thứ | Ở đâu |
| :--- | :--- |
| `stage_timings` — ms từng node | `graph.py:39` `_timed()`, trả về trong mọi response |
| `ai_mode` — nguồn gốc câu trả lời | `schemas.py:42` |
| `ai_model`, `ai_latency_ms` | `schemas.py:43–44` |
| Langfuse callback | `graph.py:115–132`, chỉ bật khi có đủ hai key, thiếu package thì cảnh báo rồi chạy tiếp |
| SSE `event: stage` | `routes/__init__.py:328` — sáu nhãn tiếng Việt cho người dùng |

### Thiếu so với schema mục tiêu

| Trường yêu cầu | Trạng thái |
| :--- | :--- |
| `trace_id`, `conversation_id` | ⚠️ có `session_id`, chưa có trace id xuyên suốt |
| `node`, `model`, `model_latency` | ✅ |
| `tool`, `tool_latency` | ❌ **không đo riêng từng tool** |
| `input_tokens`, `output_tokens` | ❌ **không đếm** — `src/services/llm.py` không đọc `usage` từ response |
| `retrieved_property_ids` | ⚠️ có trong state, không log ra |
| `hold_id`, `booking_id` | ⚠️ có trong DB, không gắn vào trace |
| `error`, `final_status` | ✅ qua `ai_mode` và exception handler |

**Hệ quả trực tiếp:** không đếm token thì **cost/conversation không đo được ở runtime**. Con số trong `docs/research/COST_MODEL.md` là **mô hình tính tay**, không phải đo. Phải ghi `NOT MEASURED` cho mọi ô cost trong scorecard cho tới khi có instrumentation.

---

## 5. Trả lời 10 câu hỏi

**Q1 — Đang chứng minh "code works" hay "AI works"?**
Chủ yếu **code works**. 200/253 test là deterministic unit. Có ~35 test chạm hành vi agent, nhưng không test nào chạy trọn graph.

**Q2 — 253 test cover gì?** Xem bảng mục 2. Mạnh ở parser, schema, business rule, crawl. Yếu ở trajectory, ranking, tool.

**Q3 — Critical failure nào chưa có regression test?**
Bịa property khi kho rỗng ở **loại hình khác thuê/bán** · Goong lỗi mà vẫn khẳng định khoảng cách · hai user tranh cùng slot đồng thời · nói "đã xác nhận" khi sale chưa duyệt · gán sale không phụ trách căn · dùng hold đã hết 15 phút.

**Q4 — Trace được một request xuyên LangGraph không?**
**Một phần.** `stage_timings` cho biết node nào chạy và mất bao lâu. Không biết tool nào được gọi, tham số gì, trả về gì. Langfuse có sẵn nhưng phụ thuộc key môi trường — chưa xác nhận đang bật trên production.

**Q5 — Recommendation sai thì biết sai ở đâu không?**
**Phân biệt được extraction, không phân biệt được retrieval với ranking.** `criteria_equals` bắt được lỗi trích xuất. Nhưng không có phép đo nào tách "căn đúng không được lấy ra" khỏi "căn đúng có lấy ra nhưng xếp thấp".

**Q6 — Goong fail thì agent có bịa khoảng cách không?**
**UNKNOWN.** `geo_service.py` có bắt exception ở 6 chỗ, nhưng **không test nào mô phỏng lỗi tool** — grep `side_effect|raise|Timeout` trong `test_geo_service.py` và `test_geo_constraints.py` không ra kết quả. Đây là câu hỏi chưa trả lời được, và nó thuộc nhóm nghiêm trọng nhất.

**Q7 — Guardrail chống bịa khi hết inventory đã test chưa?**
**Có, nhưng hẹp.** `test_rental_honesty` phủ đúng ba ca thuê/bán. Chưa phủ: sai quận, sai khoảng giá, sai số phòng ngủ.

**Q8 — PropertyHold có test concurrency không?**
**Không.** `pg_advisory_xact_lock` tồn tại ở `property_hold_service.py:36`, nhưng 2 test hiện có đi qua khoá FK và unique index tuần tự. Không có `asyncio.gather` mô phỏng hai request cùng lúc.

**Q9 — HITL có test chống xác nhận giả không?**
**Không.** 5 test HITL nói về vòng đời case (tạo, tái dùng, giải quyết). Không test nào khẳng định câu trả lời **không chứa** từ "đã xác nhận" khi `approval_requests.status != 'APPROVED'`.

**Q10 — Biết p50 / p95 / token / cost không?**
p95 = **9,52s** (đo 23 lượt trên production, `eval/results/DEMO_DAY_TRAFFIC_EVALUATION_REPORT.md`), ngưỡng 6s → trượt, và số này lẫn cold start Render gói free.
p50: **NOT MEASURED**.
Token: **đã đo từ 01/09/2026** — mỗi response trả `input_tokens`, `output_tokens`,
`cached_input_tokens`, `llm_calls` (`src/services/token_usage.py`). Hai lượt thật:
4.294/210 và 4.956/280 token, 4.096 token đọc từ cache ở cả hai, **1 lượt gọi LLM mỗi lượt chat**.
Cost/conversation: **suy ra được từ token** — ~13,9 VND/lượt, ~97 VND cho hội thoại 7 lượt.

---

## 6. Đánh giá độ trưởng thành

| Trục | Mức | Lý do |
| :--- | :---: | :--- |
| Deterministic testing | **3/5** | 253 test, CI chạy mỗi PR |
| Kịch bản eval | **3/5** | 222 case chất lượng, nhưng không tự động |
| Chấm trajectory | **0/5** | Không tồn tại |
| Observability | **2/5** | Có timing từng node, không có tool/token |
| Đo hiệu năng | **2/5** | p95 đo một lần, chưa tách cold start |
| Đo chi phí | **1/5** | Chỉ có mô hình tính tay |
| Vòng lặp regression | **1/5** | Sửa lỗi có thêm test, nhưng không sinh từ trace |

**Tổng: 12/35.** Nera đang ở giai đoạn *"AI system that appears to work"* — đúng như đề bài mô tả.

---

## 7. Ưu tiên triển khai

Xếp theo **rủi ro sản phẩm ÷ công sức**, không theo thứ tự đẹp.

| # | Việc | Vì sao trước | Công |
| :-: | :--- | :--- | :--- |
| 1 | Test Goong lỗi → không bịa khoảng cách | Q6 đang UNKNOWN, và bịa khoảng cách là SEV-0 | Nhỏ |
| 2 | Test HITL chống câu "đã xác nhận" | SEV-0, hiện không có gì chặn | Nhỏ |
| 3 | Test PropertyHold đồng thời thật | SEV-0, là điểm nhấn demo mà chưa chứng minh | Vừa |
| 4 | Đếm token trong `llm.py` | Mở khoá toàn bộ trục Cost, hiện là NOT MEASURED | Nhỏ |
| 5 | Chạy 222 kịch bản in-process trong pytest | Biến tài sản có sẵn thành cổng CI | Vừa |
| 6 | Thêm assert trajectory (`expect_nodes`) | Chấm hành trình chứ không chỉ điểm đến | Vừa |
| 7 | Tách cold start khỏi p95, đo lại | Con số hiện tại không dùng để quyết định được | Nhỏ |

---

## 8. Danh sách file dự kiến

### CREATE

| File | Mục đích |
| :--- | :--- |
| `tests/test_geo_tool_failure.py` | Goong timeout/lỗi → response không chứa khoảng cách |
| `tests/test_hitl_no_false_confirmation.py` | Chưa APPROVED → không được nói "đã xác nhận" |
| `tests/test_property_hold_concurrency.py` | Hai coroutine tranh cùng slot qua `asyncio.gather` |
| `docs/evaluation/NERA_FAILURE_TAXONOMY.md` | Failure mode + severity riêng của Nera |
| `docs/evaluation/NERA_SCORECARD.md` | Metric + baseline (ghi NOT MEASURED chỗ chưa đo) |

### MODIFY

| File | Sửa gì |
| :--- | :--- |
| `src/services/llm.py` | Đọc `usage` từ response, trả token vào state |
| `src/models/schemas.py` | Thêm `input_tokens`, `output_tokens` |
| `eval/chat_agent_acceptance.json` | Thêm `expect_nodes` cho các case quan trọng |
| `scripts/run_chat_agent_eval.py` | Cho phép chạy in-process bên cạnh chế độ HTTP |
| `.github/workflows/ci.yml` | Thêm cổng golden set nhỏ vào PR gate |

### KEEP UNCHANGED

`src/agents/graph.py` — cấu trúc graph đúng, `_timed` đã làm tốt việc của nó.
`src/services/property_hold_service.py` — advisory lock đúng, chỉ thiếu test.
`src/agents/nodes/*` — không đổi hành vi sản phẩm khi chưa có bằng chứng.
253 test hiện có — không đụng.

---

## 9. Kết luận Phase 1

**Phát hiện quan trọng nhất:** Nera không thiếu kịch bản test. 222 case đã tồn tại, phân nhóm tốt, và kiểm tra được cả trích xuất constraint lẫn grounding. Vấn đề là chúng **không chạy tự động** và **chỉ chấm điểm đến**.

Bởi vậy việc đầu tiên không phải viết thêm golden set, mà là:
1. Bịt ba lỗ SEV-0 chưa có test nào (Goong lỗi, HITL xác nhận giả, hold đồng thời)
2. Đếm token để trục Cost thoát khỏi NOT MEASURED
3. Kéo 222 case có sẵn vào pytest và CI

**Release readiness sơ bộ: 🟡 YELLOW** — demo được, nhưng ba failure mode nghiêm trọng nhất hiện chưa có gì chứng minh là không xảy ra.
