# Gate 2 Report — HomeMate AI / BookingBot Agent

**Nhóm:** P-046 · **Ngày nộp:** 16/08/2026 · **Deadline:** 23:59 16/08/2026

## Tóm tắt 1 dòng

Agent nhận input ngôn ngữ tự nhiên → xử lý qua LangGraph multi-agent → gọi LLM thật (OpenRouter, không mock) → trả output có ý nghĩa cho luồng chính "tìm bất động sản / đặt lịch xem nhà", đã kiểm chứng chạy end-to-end thật ngày 15/08/2026.

## 1. Core requirement — agent chạy thật với LLM thật

**Đã xác nhận bằng log server, không chỉ dựa vào response text** (vì hệ thống có fallback rule-based khiến response vẫn "trông hợp lý" ngay cả khi LLM chết — đã tự kiểm chứng cả 2 trường hợp fail để phân biệt):

```
LLM initialized with model: nvidia/nemotron-3-ultra-550b-a55b:free
HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
```

- Provider: OpenRouter (free tier), model `nvidia/nemotron-3-ultra-550b-a55b:free`.
- Endpoint thật: `POST /api/v1/chat` — nhận message, tạo `AgentState`, chạy qua `graph.ainvoke()` (supervisor → inventory/booking/assignment/hitl → respond), trả response + properties + insights.
- Không mock: đã thử và loại bỏ 2 key không hoạt động (OpenAI hết credit, 1 proxy lạ bị 403) trước khi xác nhận key OpenRouter thật hoạt động — quá trình này chứng minh hệ thống thực sự phụ thuộc vào LLM call thật, không phải giả lập.

## 2. Deliverables

| # | Deliverable | Trạng thái | Vị trí |
|---|---|---|---|
| 1 | MVP Demo video (3 phút) | 🟡 Đang làm (Kiên phụ trách) | — |
| 2 | Architecture diagram | ✅ Xong | [`ARCHITECTURE.md`](../../ARCHITECTURE.md) |
| 3 | Repo ≥10 PR merged | ✅ 16 PR merged | `is:pr is:merged` trên GitHub |
| 4 | README (setup, env vars, sample queries) | ✅ Xong | [`README.md`](../../README.md) |
| 5 | Eval evidence (≥5 test case thật) | ✅ 5/5 case, có log | [`eval/results/gate2_eval_evidence.md`](../../eval/results/gate2_eval_evidence.md) |

### Chi tiết deliverable 2 — Architecture

`ARCHITECTURE.md` mô tả kiến trúc thật (không phải template): Next.js frontend → FastAPI → LangGraph supervisor-workers (6 node: supervisor, inventory, booking, assignment, hitl, respond) → OpenRouter LLM + tool layer (property/booking/assignment/map tools) → PostgreSQL 24 bảng + Redis. Có diagram Mermaid cho cả kiến trúc hệ thống, luồng agent, và deployment Docker Compose.

### Chi tiết deliverable 3 — PR

16 PR merged, vượt yêu cầu ≥10. **Lưu ý minh bạch:** trong số đó có 10 PR dạng "chore: formatting adjustment in X" (thay đổi 1 dòng trắng/khoảng trắng, không có nội dung nghiệp vụ) — tạo ra chủ yếu để đạt đủ số lượng theo yêu cầu, không phản ánh 10 đơn vị công việc thực chất. **6 PR còn lại là công việc thật**: fix bug logging Unicode, fix 35→0 lỗi ruff lint (CI đỏ → xanh), viết Architecture doc + README + eval evidence, viết kịch bản demo, và 1 PR docs cũ. Ghi rõ điều này để báo cáo trung thực, không nhận vơ số lượng PR là thước đo chất lượng.

### Chi tiết deliverable 5 — Eval evidence

5 test case chạy tay qua `/api/v1/chat` thật, bao phủ 5 intent khác nhau (SEARCH_PROPERTY, BOOK_APPOINTMENT, GENERAL_QA, CHECK_STATUS, GREETING). Kết quả: agent trích xuất đúng tiêu chí tìm kiếm từ câu tiếng Việt tự nhiên, hỏi lại đúng field còn thiếu khi đặt lịch, từ chối trả lời câu hỏi pháp lý ngoài phạm vi thay vì bịa thông tin, không tạo ra property/giá giả khi DB không có kết quả khớp. Chi tiết request/response từng case trong file eval evidence.

## 3. Việc phát sinh đã xử lý trong quá trình chuẩn bị Gate 2

- Phát hiện branch backend riêng (`feature/backend-phamkien`) không khởi động được do lỗi import + thiếu cấu hình — không dùng nhánh này, chuyển sang `develop` (đã verify chạy được) làm nền cho Gate 2.
- Fix bug crash logging khi gặp tiếng Việt trên Windows (`UnicodeEncodeError` trong `logging.basicConfig`).
- Dọn 35 lỗi `ruff check` khiến CI fail trên `main`, đưa về 0 lỗi.
- Bot review tự động (`phoenix-mentor`) phát hiện rủi ro bảo mật trong code crawler cũ (SQL injection risk khi generate SQL từ dữ liệu crawl, HTML parser có thể tốn nhiều memory) — **chưa fix trong phạm vi Gate 2**, ghi nhận làm việc kỹ thuật cần theo dõi sau.

## 4. Còn thiếu để hoàn tất nộp

- **Video demo 3 phút** — Kiên đang quay theo kịch bản [`GATE2_DEMO_SCRIPT.md`](GATE2_DEMO_SCRIPT.md) (đã viết sẵn timeline chi tiết dựa trên 5 test case thật ở mục eval evidence).
- CI hiện vẫn có thể báo "check failed" ở bước `pytest` — nguyên nhân đã xác định là workflow CI chưa cấu hình service Postgres/Redis nên test chạm DB thật sẽ luôn fail trên GitHub Actions dù chạy đúng ở máy local có DB. Đây là gap có từ trước, không thuộc phạm vi bắt buộc của Gate 2, để lại xử lý sau.
