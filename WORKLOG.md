# Worklog — Team P-046 (Nera)

Worklog được tổng hợp từ `git log` trong giai đoạn 03/08/2026–01/09/2026 trên toàn bộ các nhánh của repository. Mỗi dòng là nhóm đầu ra chính trong ngày, không phải bản sao từng commit riêng lẻ.

**Lưu ý về thời lượng:** repository không ghi time tracking đáng tin cậy, vì vậy cột thời gian để `—`; không suy diễn số giờ từ số commit.

Tên viết tắt: **Lực** — Vũ Thế Lực (*Product Manager & AI Product Lead*); **Kiên** — Phạm Trung Kiên (*Tech Lead & AI Core Engineer*); **Thế Anh** — Nguyễn Thế Anh (*QA & Memory*); **Đạt** — Lê Tiến Đạt (*Prototype & Docs*).

---

## Bảng Tổng hợp Công việc theo Ngày

| Ngày | Thành viên | Công việc/đầu ra chính | Trạng thái | Thời gian |
|:---:|:---|:---|:---:|:---:|
| **03/08** | Đạt | Khởi tạo repository, kiểm thử luồng ghi log AI hooks ban đầu | Done | — |
| **04/08** | Đạt | Bản mẫu giao diện MOCKUI prototype, tài liệu brief và PRD ban đầu | Done | — |
| **05/08** | Kiên, Đạt, Thế Anh | CSDL PostgreSQL schema ban đầu, nạp dữ liệu BĐS crawled, tài liệu Project Brief | Done | — |
| **06/08** | Kiên | Khởi tạo backend FastAPI, APIs xác thực và đặt lịch; hoàn thiện 10 trang UI frontend kết nối API backend | Done | — |
| **07/08** | Lực, Kiên, Đạt | Lực định vị AI Home Companion, nghiên cứu sản phẩm và demo drafts; Kiên hoàn thiện UI responsive, phân trang và dữ liệu thật; Đạt cấu hình Redis | Done | — |
| **08/08** | Lực, Kiên, Đạt | Lực hoàn thiện đặc tả Figma user flows 01-05; Kiên cập nhật kết nối CSDL PostgreSQL và tích hợp Chat UI; Đạt cập nhật text | Done | — |
| **09/08** | Lực | Sao lưu hệ thống, chuẩn hóa môi trường làm việc và công cụ phát triển | Done | — |
| **11/08** | Lực | Đánh giá kỹ thuật AI Elements cho HomeMate V2, điều chỉnh định hướng sản phẩm theo phản hồi mentor | Done | — |
| **12/08** | Kiên | Hoàn thiện luồng nền tảng đặt lịch và cơ chế lưu trữ phiên làm việc | Done | — |
| **13/08** | Kiên | Triển khai Phase 1 & 2: Admin Dashboard, Sale Map, Booking UI, kho ảnh BĐS và luồng khách hàng trang chủ | Done | — |
| **14/08** | Kiên | Nâng cấp booking service, sửa timezone scheduler, hoàn thiện Phase 3 backend & UI | Done | — |
| **15/08** | Lực, Kiên | Lực viết kịch bản video demo Gate 2, sửa crash UTF-8 console logging trên Windows, tài liệu kiến trúc; Kiên triển khai modal hủy booking, thông báo Sale và dọn mock data | Done | — |
| **16/08** | Lực | Hoàn thiện báo cáo nộp Gate 2, rà soát và điều chỉnh các cam kết kỹ thuật | Done | — |
| **18/08** | Lực | Ghi nhận quyết định kiến trúc D-013/R-011 trên nhánh backend | Done | — |
| **19/08** | Kiên, Đạt | Dọn dẹp test files và scripts rác, cập nhật UI và agents | Done | — |
| **20/08** | Thế Anh, Đạt | Thế Anh viết bộ test API, routing, đánh giá RAGAS baseline; Đạt cập nhật text và memory | Done | — |
| **21/08** | Thế Anh, Kiên | Tích hợp Mem0 memory service và bộ test tương ứng | Done | — |
| **22/08** | Lực, Kiên | Lực lọc từ khóa quảng cáo khỏi tiêu đề BĐS; Kiên hoàn thiện multi-turn comparison, bảng markdown so sánh, auto-seed DB, JWT auth, CartoDB maps, seeding 20 sale accounts, floating AI assistant | Done | — |
| **23/08** | Lực, Kiên | Lực chuẩn hóa tiêu đề BĐS, sửa bản sao hero headline, xóa 1.814 dòng code chết trong agents; Kiên tinh chỉnh cổng frontend (3005 / 3000) | Done | — |
| **24/08** | Lực, Kiên | Lực thiết lập Demo Password Guard, Brand Kit Nera, slide Phase 1, bảo vệ session ownership; Kiên lọc phòng ngủ chính xác, chuẩn hóa Unicode word boundaries, lọc địa lý toàn quốc, nút dừng chat | Done | — |
| **25/08** | Lực | Xây dựng logic tư vấn tài chính theo thu nhập và vốn tự có bằng công thức toán thật | Done | — |
| **26/08** | Lực, Kiên | Lực nhận diện từ vựng Cho Thuê, lọc lời chào môi giới, thêm AI tóm tắt trước khi hiển thị; Kiên tích hợp logo/symbol Nera, Typewriter tuần tự, Amortization loan engine, InMemoryFallback khi Redis sập | Done | — |
| **27/08** | Lực, Kiên | Lực sửa import pathlib; Kiên đóng 6 issue mentor review, sửa mất ngữ cảnh và lách guardrail, tăng kích thước logo navbar | Done | — |
| **28/08** | Lực, Kiên | Lực cập nhật tài liệu kiến trúc, security và eval suite; Kiên tích hợp Goong Maps tính khoảng cách, badge và iframe chỉ đường | Done | — |
| **29/08** | Lực | Chuẩn hóa trích xuất lộ trình commute Goong Maps, dọn dẹp script API thủ công, thêm Global Exception Handler chống rò rỉ SQL | Done | — |
| **30/08** | Lực | Tích hợp Langfuse Tracing thật, helper `_trace_callbacks()`, bọc đo ms vòng gọi Goong, `_extract_finance()` trong supervisor, viết hướng dẫn demo Langfuse | Done | — |
| **31/08** | Kiên | Bổ sung trường `last_verified_at` và cập nhật số lượng BĐS | Done | — |
| **01/09** | Lực, Kiên | Lực xây dựng `src/services/token_usage.py`, 3 bộ test SEV-0 (Goong failure, HITL false confirmation, Concurrency lock), tích hợp 222 Golden Scenarios vào pytest (`test_golden_set.py`), viết Monetization One-Pager, audit 10 Deliverables; Kiên cập nhật giao diện, tối ưu truy vấn SQL theo landmark và batch Goong matrix | Done | — |

---

## Tổng hợp theo Trục Trách nhiệm

| Thành viên | Trục đóng góp có bằng chứng trong Git history |
|:---|:---|
| **Vũ Thế Lực** | **Product & AI Lead:** Định vị sản phẩm O2O, Khảo sát thực địa (n=20), Data Pipeline (3.796 căn thật, chuẩn hóa 27 tỉnh thành, lọc nhiễu tiêu đề), AI Multi-Agent logic, Token & Cost Tracker runtime, Eval Suite (720 tests pass, 3 tests SEV-0, 222 Golden Scenarios), Monetization One-Pager (300k/seat, Cost/Job ~5k), Pitch Deck PDF, Video Script và chuẩn hóa 10 Deliverables. Xem chi tiết: [`docs/PM_AI_PRODUCT_PORTFOLIO.md`](docs/PM_AI_PRODUCT_PORTFOLIO.md) |
| **Phạm Trung Kiên** | **Tech Lead & AI Core:** Kiến trúc lõi AI Multi-Agent trên LangGraph (Supervisor, Inventory, Booking, Assignment), Reasoning đa lượt & So sánh BĐS, Động cơ tính khoản vay Amortization, Tích hợp Goong Maps & Batch Distance Matrix, CSDL PostgreSQL 18 bảng, Redis InMemoryFallback, Kiến trúc FastAPI Backend và toàn bộ 25 Routes Frontend Next.js 14 App Router. Xem chi tiết: [`docs/TECH_LEAD_AI_CORE_PORTFOLIO.md`](docs/TECH_LEAD_AI_CORE_PORTFOLIO.md) |
| **Nguyễn Thế Anh** | **QA & Memory:** Viết bộ test API và routing, thử nghiệm đánh giá chất lượng RAGAS ban đầu, tích hợp và kiểm thử Mem0 memory service (`src/services/mem0_service.py`), quản lý tài liệu Project Brief. Xem chi tiết: [`docs/QA_MEMORY_PORTFOLIO.md`](docs/QA_MEMORY_PORTFOLIO.md) |
| **Lê Tiến Đạt** | **Prototype & Docs:** Xây dựng bản mẫu giao diện MOCKUI prototype, soạn thảo BookingBot AI brief và PRD ban đầu, cấu hình Redis ban đầu, thiết lập hệ thống AI logging hooks. Xem chi tiết: [`docs/PROTOTYPE_DOCS_PORTFOLIO.md`](docs/PROTOTYPE_DOCS_PORTFOLIO.md) |

---

## Cách Kiểm chứng (Verification Commands)

```powershell
# Xem toàn bộ commit history từ ngày khởi tạo
git log --since="2026-08-02" --date=short --pretty=format:"%ad %an %ae %s"

# Xem thống kê số lượng commit của từng thành viên
git shortlog -sne HEAD
```
