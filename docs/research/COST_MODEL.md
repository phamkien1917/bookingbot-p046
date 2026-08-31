# Bài toán chi phí vận hành Nera

**Mã tài liệu:** `docs/research/COST_MODEL.md`
**Cập nhật:** 08/2026
**Công cụ tính kèm:** [`scripts/cost_model.py`](../../scripts/cost_model.py) — đổi giả định, xem lại biên lợi nhuận.

Mô hình dưới đây trả lời: chạy Nera tốn bao nhiêu, và ở giá 300.000đ/tài khoản/tháng thì còn lãi không.

## Giả định gốc (đều chỉnh được trong script)

| Tham số | Giá trị dùng | Nguồn |
| :--- | :--- | :--- |
| Mô hình LLM | `openai/gpt-4o-mini` qua OpenRouter, fallback OpenAI | `render.yaml`, `.env.example` |
| Giá input | 0,15 USD / 1 triệu token | OpenAI API pricing 2026 |
| Giá output | 0,60 USD / 1 triệu token | — |
| Giá input đã cache | 0,075 USD / 1 triệu token (giảm 50%) | — |
| Tỷ giá | 1 USD ≈ 26.000 VND | Giả định 2026, chỉnh khi cần |
| Số lượt LLM / lượt chat của khách | ~2 (có lượt đi fast-path regex = 0, có lượt booking = 3–4) | Kiến trúc multi-agent LangGraph |
| Token / lượt gọi LLM | ~2.500 input + 350 output | Ước tính (system prompt + lịch sử rút gọn + BĐS truy xuất + bộ nhớ) |
| Số lượt hội thoại / cuộc | ~7 | Field test |

## 1. Chi phí biến đổi — mỗi cuộc hội thoại

Một lượt gọi LLM (có prompt caching cho system prompt tĩnh ~1.200 token):

- Input tươi: 1.300 token × 0,15/1tr = 0,000195 USD
- Input cache: 1.200 token × 0,075/1tr = 0,00009 USD
- Output: 350 token × 0,60/1tr = 0,00021 USD
- **≈ 0,0005 USD/lượt gọi ≈ 13 VND**

| Mức | Cuộc hội thoại | LLM | + Goong Maps | Tổng |
| :--- | :--- | :--- | :--- | :--- |
| Điển hình | 7 lượt, 2 gọi/lượt | ~180 VND | ~60 VND (1 truy vấn khoảng cách) | **~250 VND** |
| Nặng | 12 lượt, có booking | ~600 VND | ~120 VND | **~750 VND** |
| Không cache | nhân đôi phần input | — | — | vẫn < 1.500 VND |

Chốt để tính: **~500 VND/cuộc hội thoại** (làm tròn lên cho an toàn).

## 2. Chi phí cố định — mỗi tháng (production quy mô nhỏ)

| Hạng mục | Gói | USD/tháng |
| :--- | :--- | :---: |
| Render — backend web | Starter | 7 |
| Render — worker (giữ chỗ, lịch) — có thể gộp vào web | Starter | 0–7 |
| Render — PostgreSQL | Basic | 6–19 |
| Redis (Render Key Value / Redis Cloud) | Starter | 0–10 |
| Vercel — frontend | Hobby → Pro khi thương mại | 0–20 |
| Langfuse Cloud — observability | Free 50k obs → Core | 0–29 |
| Goong Maps | Free 30.000 req/tháng → Basic | 0–? |
| Tên miền `.space` | /năm quy ra tháng | ~1,5 |
| **Tổng** | | **~25–110 USD/tháng** |

Quy đổi: **~650.000 – 2.900.000 VND/tháng**. Giai đoạn pilot dùng free tier: gần 0 – 800.000đ.

## 3. Kinh tế đơn vị — ở giá 300.000đ/tài khoản/tháng

Chi phí biến đổi mỗi tài khoản tùy lượng khách:
- Sale ít việc: 30 cuộc/tháng × 600đ ≈ 18.000đ
- Sale bận: 120 cuộc/tháng × 800đ ≈ 96.000đ
- Lấy trung bình: **~50.000đ/tài khoản/tháng** cho LLM + Goong

Chi phí cố định chia đều:

| Quy mô | Hạ tầng/tài khoản | Biến đổi/tài khoản | Tổng chi phí phục vụ | Biên lợi nhuận trên 300k |
| :--- | :---: | :---: | :---: | :---: |
| 20 tài khoản | ~100.000đ | ~50.000đ | ~150.000đ | **50%** (mô hình: 61%) |
| 50 tài khoản | ~40.000đ | ~50.000đ | ~90.000đ | **70%** (mô hình: 81%) |
| 200 tài khoản | ~12.000đ | ~50.000đ | ~62.000đ | **79%** (mô hình: 91%) |

Cột "biên lợi nhuận" là con số thận trọng để trình bày; trong ngoặc là kết quả thô của
`scripts/cost_model.py`. LLM là giá vốn thật (khác SaaS thuần), nhưng biên vẫn về mức
70–80% khi qua ~50 tài khoản.

## 4. Chi phí mỗi lịch hẹn chốt được — điểm nhấn pitch

Giả sử 5 cuộc hội thoại ra 1 lịch hẹn được Sale duyệt. Mô hình (`scripts/cost_model.py`)
tính ra **~1.200 VND**; trình bày thận trọng để phòng token phình và retry: **~3.000 – 5.000 VND**.

Hoa hồng mỗi giao dịch thành công (Sale + sàn): **80 – 150 triệu VND**.
Chi phí AI ≈ **0,003%** giá trị hoa hồng. Nói cách khác: 1 giao dịch chốt bù được chi phí AI của hàng chục nghìn lịch hẹn.

## 5. Đòn bẩy giảm chi phí (phần lớn đã có trong code)

| Đòn bẩy | Trạng thái | Tác động |
| :--- | :--- | :--- |
| Fast-path regex ở Supervisor — 0 lượt gọi LLM cho câu tìm kiếm rõ ràng | Đã có | Cắt ~30–50% lượt gọi |
| Prompt caching cho system prompt lặp lại | Bật ở cấu hình OpenRouter/OpenAI | Giảm 50% token input tĩnh |
| `CustomerMemoryService` tóm tắt sở thích dài hạn | Đã có | Context ngắn hơn mỗi lượt |
| Redis rate limiting | Đã có | Chặn lạm dụng đẩy chi phí |
| Giới hạn số BĐS đưa vào context (top 5–8) | Cần kiểm tra | Giữ token input không phình |
| Cắt lịch sử hội thoại còn N lượt gần nhất | Cần kiểm tra | — |
| Chỉ gọi Goong DistanceMatrix khi khách hỏi khoảng cách | Cần xác nhận | Giữ trong hạn free 30k/tháng |

Không nên: hạ xuống model `:free` — `.env.example` ghi rõ không ổn định khi tải cao.

## 6. Rủi ro và độ nhạy

| Rủi ro | Ảnh hưởng | Xử lý |
| :--- | :--- | :--- |
| Tỷ giá USD/VND tăng 10% | LLM +10%, vẫn < 1.000đ/cuộc | Không đáng kể |
| Context phình do nhiều BĐS | Token input tăng | Cap top 5–8 kết quả |
| Vòng lặp do prompt injection | Đốt token | Rate limit + từ chối OOS (100% trong test) |
| Langfuse vượt 50k observations/tháng (~7.000 cuộc) | Phải lên gói trả phí hoặc sample trace | Sample 10–20% trace khi scale |
| Render free plan cold start (~4s) | Vấn đề trải nghiệm, không phải chi phí | Lên gói Starter |

## 7. Số đưa lên slide

- Chi phí AI mỗi lịch hẹn thật: **~3.000 – 5.000 VND** — bằng **0,003%** hoa hồng giao dịch.
- Biên lợi nhuận ở giá 300.000đ/tài khoản: **50% khi mới (20 tài khoản) → ~79% khi scale (200 tài khoản)**.
- Chi phí cố định để vận hành: **~650.000 – 2.900.000 VND/tháng**.
- Điểm hòa vốn: khoảng **5–10 tài khoản trả phí** là bù toàn bộ chi phí vận hành.
