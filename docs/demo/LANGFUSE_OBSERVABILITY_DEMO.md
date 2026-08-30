# Demo — Đo độ trễ với Langfuse (happy path)

Mục tiêu: trả lời đúng câu mentor hỏi ở buổi review — *"không đo thì không biết chậm ở đâu"*.
Kịch bản này chạy một lượt hội thoại sạch, rồi chỉ ra thời gian của từng chặng
ở ba mức: tổng lượt, từng node trong graph, và từng lời gọi LLM.

## Chuẩn bị (2 phút)

1. `.env` đã có ba dòng Langfuse (đã thêm sẵn):
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
2. Chỉ bật một tracer. Trong `.env` đặt `LANGCHAIN_TRACING_V2=false` để LangSmith
   không chạy song song làm nhiễu số liệu.
3. Chạy backend, để log ở mức INFO:
   ```powershell
   .\venv\Scripts\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000
   ```
4. Mở https://cloud.langfuse.com → project → tab **Tracing**, để sẵn ở đó.
5. Kiểm tra kết nối Langfuse trước khi quay:
   ```powershell
   .\venv\Scripts\python.exe -c "from langfuse import get_client; print(get_client().auth_check())"
   ```
   Phải in `True`.

> Backend cần "warm" trước. Gọi thử một lượt bỏ đi, rồi mới bắt đầu đo — lượt đầu
> luôn chậm hơn vì nạp model client và mở kết nối DB.

## Kịch bản (happy path — 3 lượt)

Dùng chung một `session_id` để nối ngữ cảnh. Bắt buộc là UUID hợp lệ (nếu không,
API trả 422). Sinh một cái rồi giữ nguyên cho cả ba lượt.

### Lượt 1 — chào hỏi (đường ngắn nhất: chỉ supervisor + respond)

```powershell
$SID = [guid]::NewGuid().ToString()
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/chat -Method Post -ContentType "application/json" -Body (@{
  message = "chào Nera"
  session_id = $SID
} | ConvertTo-Json) | Select-Object ai_mode, stage_timings
```

### Lượt 2 — tìm nhà (đường đầy đủ: supervisor + inventory + respond)

```powershell
Measure-Command {
  $r = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/chat -Method Post -ContentType "application/json" -Body (@{
    message = "tìm căn hộ 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ"
    session_id = $SID
  } | ConvertTo-Json)
}
$r | Select-Object ai_mode, stage_timings
```

### Lượt 3 — thu hẹp tiêu chí + lọc khoảng cách (thêm vòng gọi Goong)

```powershell
$r = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/chat -Method Post -ContentType "application/json" -Body (@{
  message = "chỉ lấy căn cách Đại học Quốc gia Hà Nội dưới 20 phút đi xe"
  session_id = $SID
} | ConvertTo-Json)
$r | Select-Object ai_mode, stage_timings
```

Biến thể bash/curl:

```bash
SID=$(python -c "import uuid; print(uuid.uuid4())")
curl -s http://127.0.0.1:8000/api/v1/chat -H 'content-type: application/json' \
  -d "{\"message\":\"tìm căn hộ 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ\",\"session_id\":\"$SID\"}" \
  | python -m json.tool
```

## Đọc số liệu ở ba mức

### Mức 1 — từng node (trong response API)

```json
{
  "ai_mode": "llm_grounded",
  "ai_latency_ms": 900,
  "stage_timings": { "supervisor": 900, "inventory": 3100, "respond": 1200 }
}
```

- `stage_timings`: thời gian mỗi node trong graph. Cộng lại là xấp xỉ tổng lượt
  (ở ví dụ trên ≈ 5200 ms). Đây là thứ thêm mới sau buổi review.
- `ai_latency_ms`: **chỉ** là thời gian gọi LLM ở node supervisor, không phải
  tổng lượt. Giữ tên cũ để không phá client. Muốn tổng lượt thì cộng
  `stage_timings`, hoặc đo wall-clock quanh request (ví dụ
  `Measure-Command { ... }` trong PowerShell).

### Mức 2 — vòng gọi Goong (trong log backend)

Ở lượt 3, tìm dòng:

```
INFO ... geo.enrich_and_filter took 1840 ms
```

`stage_timings["inventory"]` gộp cả LLM lẫn Goong. Dòng log này tách riêng phần
Goong ra, nên biết trong 3100 ms của node inventory có bao nhiêu là gọi bản đồ.

### Mức 3 — từng lời gọi LLM (trong Langfuse)

Mở trace mới nhất trên dashboard. Cây trace hiện:

```
run_agent
├── supervisor      → 1 generation (intent, structured output)   ~900 ms   320 tokens
├── inventory       → 1 generation (soạn câu trả lời)            ~1200 ms  1800 tokens
└── respond         → 1 generation (chốt phản hồi)               ~1100 ms   950 tokens
```

Mỗi generation có: thời gian, số token vào/ra, chi phí ước tính, và prompt +
response đầy đủ. Đây là mức `stage_timings` không với tới được.

## Lời thuyết minh (≈90 giây)

> Ở buổi review, mentor nói một câu đúng: *không đo thì không biết chậm ở đâu*.
> Nhóm đã dựng phép đo ở ba mức.
>
> Mức một, ngay trong response API: `stage_timings` chia thời gian ra ba node —
> supervisor, inventory, respond. Cộng lại là tổng một lượt. Nhìn vào đây thấy
> ngay node inventory chiếm phần lớn thời gian.
>
> Mức hai, node inventory vừa gọi LLM vừa gọi Goong Maps để lọc khoảng cách.
> Nhóm bọc lời gọi Goong bằng một lớp đo riêng, log ra `geo.enrich_and_filter
> took ... ms`, nên tách được phần bản đồ khỏi phần LLM.
>
> Mức ba là Langfuse. Mỗi lượt sinh một trace, trong đó từng lời gọi LLM là một
> span riêng, kèm thời gian, số token và chi phí. Ở đây thấy rõ một lượt tìm nhà
> gọi LLM ba lần tuần tự — đó là lý do gốc của độ trễ, và là chỗ để tối ưu tiếp:
> gộp bớt lời gọi, hoặc chạy song song những phần không phụ thuộc nhau.
>
> Với bên thứ ba như Goong thì chấp nhận có độ trễ, nhưng giờ nhóm biết chính xác
> nó tốn bao nhiêu thay vì đoán.

## Câu lệnh mẫu để copy

```text
chào Nera
tìm căn hộ 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ
chỉ lấy căn cách Đại học Quốc gia Hà Nội dưới 20 phút đi xe
```

## Nếu Langfuse không hiện trace

- `auth_check()` trả `False` → sai key, tạo lại ở Langfuse Settings → API Keys.
- Trace chậm vài giây mới lên dashboard — Langfuse gửi theo batch. Đợi hoặc F5.
- `_trace_callbacks()` trả `()` → thiếu key trong `.env`, hoặc chưa restart backend
  sau khi sửa `.env`.

---

# Phụ lục — Kịch bản chat với Nera qua giao diện

Chạy bằng giao diện `/chat` thật. Kịch bản có hai mục đích: (1) đo độ trễ ở từng
chặng, (2) khoanh vùng chỗ "đơ" khi mới gửi tin. Mỗi lượt sinh một trace Langfuse.

## Chuẩn bị

1. Backend + frontend chạy. `.env` có key Langfuse, `LANGCHAIN_TRACING_V2=false`.
2. Backend để log mức INFO — cần thấy dòng `Chat stage timings session=...` và
   `geo.enrich_and_filter took ... ms`.
3. Đăng nhập tài khoản khách: `customer.demo@example.com` / `Demo@123`.
4. Mở `/chat`, bấm **Cuộc trò chuyện mới** (bắt đầu phiên sạch, tránh tiêu chí cũ
   trong long-term memory trộn vào).
5. Mở sẵn tab Langfuse **Tracing**. Mở DevTools → Network để đọc thời gian thực
   của request `POST /api/v1/chat`.
6. Bật sẵn tab **Sale** (`kien.sale@example.com` / `Demo@123`) cho phần đặt lịch.

## Phần A — Đo cold start (2 lượt greeting)

`chào Nera` **không gọi LLM lần nào** (fast path regex ở supervisor, respond trả
thẳng `direct_response`). Nên lượt này đo đúng phần hạ tầng, không lẫn LLM.

| # | Gõ vào chat | Xem gì | Kết luận |
|---|---|---|---|
| 1 | `chào Nera` | Network: thời gian request. Log: `Chat stage timings` (supervisor + respond, phải < 50 ms tổng) | Nếu request mất 20–60 s mà stage timings < 50 ms → chậm nằm **ngoài graph**: Render cold start hoặc Redis/Postgres/captcha trước graph |
| 2 | `chào Nera` (gửi lại ngay) | So thời gian request với lượt 1 | Lượt 2 nhanh hẳn → **cold start** (container Render ngủ, request đầu đánh thức). Lượt 2 vẫn chậm → Redis/DB/captcha, đào tiếp |

Trên Langfuse: lượt 1 và 2 mỗi cái một trace, span `run_agent` rất ngắn, **0
generation**. Nếu span `run_agent` cũng mất vài giây → bất thường trong graph.

## Phần B — Đo pipeline tìm nhà (đường đầy đủ)

Gõ từng dòng, chờ trả lời xong mới gõ tiếp.

| # | Gõ vào chat | Nera làm gì | Chặng gọi |
|---|---|---|---|
| 3 | `tìm chung cư 2 phòng ngủ ở Cầu Giấy dưới 6 tỷ` | Bóc tách tiêu chí, trả danh sách căn kèm lý do | supervisor (LLM) + inventory (LLM) + respond (LLM) = 3 lời gọi tuần tự |
| 4 | `còn căn nào tầm 5 tỷ đổ lại không` | Giữ quận + số phòng, hạ trần giá | supervisor + inventory + respond |
| 5 | `lấy căn cách Đại học Quốc gia Hà Nội dưới 25 phút đi xe` | Gọi Goong lọc theo thời gian đi, gắn badge khoảng cách | inventory + **vòng `enrich_and_filter`** → log `geo.enrich_and_filter took ... ms` |
| 6 | `so sánh 2 căn đầu giúp mình` | Bảng so sánh + nhận xét | supervisor + inventory (nhánh so sánh, 1 LLM) + respond |
| 7 | `căn số 1 có điểm gì nổi bật` | Review sâu một căn | supervisor + inventory (nhánh review) + respond |

Sau mỗi lượt, đọc log `Chat stage timings session=... {'supervisor': .., 'inventory': .., 'respond': ..}`.
Cộng ba số ≈ tổng thời gian lượt. Node `inventory` thường lớn nhất.

## Phần C — Tài chính + đặt lịch

| # | Gõ vào chat | Nera làm gì | Chặng gọi |
|---|---|---|---|
| 8 | `mình có sẵn 1 tỷ, thu nhập 40 triệu mỗi tháng, tư vấn giúp mình tầm giá mua nhà` | `_extract_finance` bắt thu nhập 40tr + vốn 1 tỷ; `affordability.py` tính tầm giá, LLM chỉ diễn đạt | supervisor + respond (không hỏi lại "40 tỷ hay thuê") |
| 9 | `đặt lịch xem căn số 1 vào 14h ngày mai` | Kiểm tra căn + slot Sale, tạo yêu cầu `TR-xxxx` trạng thái chờ duyệt | supervisor (intent BOOKING) + booking + respond |
| 10 | *(tab Sale)* bấm **Xác nhận** yêu cầu `TR-xxxx` | Tạo `PropertyHold` + `Appointment` | REST thuần, không qua graph |
| 11 | *(tab khách)* `lịch của mình sao rồi` | Báo đã xác nhận + mã booking + tên/SĐT Sale | supervisor + respond |
| 12 | `cảm ơn Nera nhé` | Chào tạm biệt (fast path, không LLM) | supervisor + respond |

## Đọc kết quả trên Langfuse

1. Tab **Tracing** → lọc theo khoảng thời gian vừa chat → ~10 trace, mỗi lượt một cái.
2. Mở trace **lượt 3**: cây span `run_agent → supervisor → inventory → respond`,
   mỗi node một generation kèm thời gian, token vào/ra, chi phí ước tính.
3. Mở trace **lượt 5**: node inventory dài hơn lượt 3 rõ rệt — phần chênh là vòng
   Goong. Đối chiếu dòng log `geo.enrich_and_filter took ... ms`.
4. Tab **Sessions** → chọn `session_id` của phiên → xem cả 12 lượt trên một dòng
   thời gian, tổng token và tổng chi phí. `run_agent` gắn sẵn `langfuse_session_id`
   và `langfuse_user_id`.
5. Sắp generation theo **Latency** giảm dần → loại lời gọi nào chậm nhất (thường
   là inventory vì prompt dài, nhồi nhiều dữ liệu căn hộ).

## Chốt cho mentor

- Greeting: 0 LLM. Nếu vẫn "đơ" → hạ tầng (cold start / Redis / captcha), không
  phải agent. Phần A chứng minh điều này bằng số.
- Tìm nhà: 3 lời gọi LLM tuần tự, cộng 1 vòng Goong khi lọc khoảng cách. Đây là
  nguồn độ trễ chính và là chỗ tối ưu tiếp.
- Đã đo được từng chặng thay vì đoán: `stage_timings` (mức node) + log Goong
  (tách bên thứ ba) + Langfuse (mức từng lời gọi LLM).
- Hướng tối ưu: gộp lời gọi supervisor và inventory, hoặc rút ngắn prompt
  inventory; giữ container Render ấm bằng cron ping `/health`.
