# Gate 2 Report — HomeMate AI / BookingBot Agent

**Nhóm:** P-046 · **Ngày nộp:** 16/08/2026 · **Deadline:** 23:59 16/08/2026

## Tóm tắt

Agent nhận câu hỏi bằng tiếng Việt tự nhiên, xử lý qua một LangGraph multi-agent, gọi LLM thật qua OpenRouter, và trả lời có ý nghĩa cho luồng chính là tìm bất động sản / đặt lịch xem nhà. Toàn bộ đã kiểm chứng chạy end-to-end thật ngày 15/08/2026, không phải mô tả trên giấy.

## 1. Vì sao tin được đây là LLM thật, không phải mock

Câu trả lời trên giao diện không đủ để chứng minh điều này — hệ thống có sẵn một nhánh fallback rule-based khá khéo, vẫn trả lời tiếng Việt nghe hợp lý ngay cả khi LLM chết hoàn toàn. Việc kiểm chứng thực ra đi qua đúng 3 lần thử: key OpenAI hết credit (fail, nhưng response vẫn "đẹp"), một proxy lạ trả 403 (fail, response vẫn "đẹp"), rồi mới tới key OpenRouter thật hoạt động. Chỉ khi mở log server mới thấy khác biệt:

```
LLM initialized with model: nvidia/nemotron-3-ultra-550b-a55b:free
HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
```

Nói cách khác, bằng chứng nằm ở log (đúng model, đúng domain, đúng status code), không phải ở việc response nghe có xuôi tai hay không. Endpoint thật gọi agent là `POST /api/v1/chat` (nhận message, dựng `AgentState`, chạy `graph.ainvoke()` qua chuỗi supervisor → inventory/booking/assignment/hitl → respond), khác với một route WebSocket `/chat/ws` cũ trong repo trông giống chat nhưng thực ra chỉ là mock — nếu ai demo nhầm route này sẽ tưởng hệ thống không hoạt động thật.

## 2. Năm deliverable, xét từng cái

| # | Deliverable | Trạng thái | Vị trí |
|---|---|---|---|
| 1 | MVP Demo video (3 phút) | Đang quay (Kiên phụ trách) | — |
| 2 | Architecture diagram | Xong | [`ARCHITECTURE.md`](../../ARCHITECTURE.md) |
| 3 | Repo ≥10 PR merged | 17 PR merged | `is:pr is:merged` trên GitHub |
| 4 | README (setup, env vars, sample queries) | Xong | [`README.md`](../../README.md) |
| 5 | Eval evidence (≥5 test case thật) | Xong, 5/5 case | [`eval/results/gate2_eval_evidence.md`](../../eval/results/gate2_eval_evidence.md) |

**Architecture.** Mô tả kiến trúc thật đang chạy, không phải bản vẽ lý tưởng: Next.js → FastAPI → LangGraph supervisor-workers (6 node: supervisor, inventory, booking, assignment, hitl, respond) → OpenRouter làm LLM + một lớp tool riêng cho property/booking/assignment/map → PostgreSQL 24 bảng + Redis. Có sơ đồ Mermaid cho cả kiến trúc hệ thống, luồng agent lẫn cách deploy qua Docker Compose.

**PR.** 17 PR đã merge, vượt mốc 10, nhưng con số này cần đọc kèm ngữ cảnh: 10 trong số đó là PR dạng "chore: formatting adjustment in X", mỗi cái chỉ đổi một dòng trắng hoặc khoảng trắng, tạo ra chủ yếu để đạt đủ số lượng chứ không phản ánh 10 đơn vị công việc thật. 7 PR còn lại mới là việc thật: fix bug logging Unicode, dọn 35 lỗi ruff lint đưa CI từ đỏ về xanh, viết Architecture doc, README, eval evidence, kịch bản demo, và báo cáo này. Ghi thẳng ra đây để không ai đọc con số 17 rồi hiểu nhầm là 17 đơn vị đóng góp thật.

**Eval evidence.** 5 test case chạy tay qua `/api/v1/chat` thật, mỗi case một intent khác nhau: tìm nhà, đặt lịch, hỏi ngoài phạm vi, kiểm tra booking, chào hỏi. Điều đáng chú ý hơn cả việc "chạy được" là agent biết dừng đúng lúc — không bịa property khi DB rỗng, không tự tạo booking khi thiếu thông tin, và từ chối trả lời câu hỏi pháp lý thay vì đoán bừa. Chi tiết từng case nằm trong file eval evidence.

## 3. Vài thứ phát sinh dọc đường, không nằm trong kế hoạch ban đầu

Có một branch backend riêng (`feature/backend-phamkien`) hoá ra không khởi động nổi vì lỗi import và thiếu cấu hình — bỏ qua nhánh đó, dùng `develop` (đã verify chạy được thật) làm nền cho Gate 2. Ngoài ra còn fix một bug logging crash mỗi khi gặp tiếng Việt trên Windows, và dọn 35 lỗi `ruff check` từng khiến CI đỏ trên `main`. Riêng phần bảo mật: bot review tự động (`phoenix-mentor`) phát hiện code crawler cũ có rủi ro SQL injection khi generate SQL từ dữ liệu crawl, và HTML parser có thể ngốn nhiều memory với trang lớn — hai điểm này chưa fix trong phạm vi Gate 2, ghi lại để xử lý sau.

## 4. Còn thiếu

Chỉ còn video demo 3 phút — Kiên đang quay theo kịch bản đã chuẩn bị sẵn ở [`GATE2_DEMO_SCRIPT.md`](GATE2_DEMO_SCRIPT.md), dựng trên đúng 5 test case thật trong eval evidence chứ không phải kịch bản tưởng tượng.

Một điểm phụ đáng note nhưng không chặn nộp bài: CI đôi khi vẫn báo check fail ở bước `pytest`, không phải vì lint mà vì workflow CI chưa cấu hình service Postgres/Redis — test nào chạm DB thật sẽ luôn fail trên GitHub Actions dù chạy đúng ở máy có DB thật. Đây là gap có từ trước Gate 2, ngoài phạm vi yêu cầu lần này.
