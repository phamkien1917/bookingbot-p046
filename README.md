# Nera — Trợ Lý AI Bất Động Sản & Đặt Lịch Xem Nhà O2O

<div align="center">

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-brightgreen?style=flat-square&logo=githubactions)](.github/workflows/ci.yml)
[![Tests Passing](https://img.shields.io/badge/Tests-844%20Passed-success?style=flat-square&logo=pytest)](docs/evaluation.md)
[![Live Production](https://img.shields.io/badge/Live-nerahome.space-blue?style=flat-square&logo=vercel)](https://www.nerahome.space/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14%20App%20Router-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18%20Tables-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6F00?style=flat-square)](https://langchain-ai.github.io/langgraph/)

**Nera** là nền tảng AI Agent đàm thoại thông minh cho bất động sản O2O (Online-to-Offline), giải quyết bài toán đứt gãy giao dịch giữa tìm kiếm trên mạng và dẫn khách thực địa của chuyên viên Sale.

🌐 **Trải nghiệm trực tiếp:** [https://www.nerahome.space/](https://www.nerahome.space/) · 📚 **API Docs:** `http://localhost:8000/docs`

</div>

---

## 📸 Giao diện Ứng dụng (Screenshots)

<div align="center">

| Trò chuyện tìm nhà & Tính khoảng cách Goong Maps | Khám phá kho BĐS & Đặt lịch xem nhà |
|:---:|:---:|
| ![Nera Chat](docs/demo/assets/nera-needs-clean.png) | ![Nera Properties](docs/demo/assets/nera-properties-top-clean.png) |

| Trí nhớ duy trì tiêu chí đa lượt | Phân hệ Sale duyệt lịch xem nhà (HITL) |
|:---:|:---:|
| ![Nera Memory Journey](docs/demo/assets/nera-home-memory-clean.png) | ![Nera Trust & HITL](docs/demo/assets/nera-trust-clean.png) |

</div>

---

## 📑 Danh mục 10 Deliverables theo chuẩn Ban Tổ Chức AI20K

| # | Deliverable | Vị trí tài liệu trong Repository | Mô tả & Trạng thái |
|:---:|:---|:---|:---|
| **1** | **Source Code** | `src/`, `frontend/`, `database/` | Mã nguồn phân tầng rõ ràng, 844 tests pass |
| **2** | **README.md** | [`README.md`](README.md) | Tài liệu hướng dẫn đầy đủ, có ảnh giao diện, bảng biến, bảng API |
| **3** | **Architecture Diagram** | [`docs/architecture.md`](docs/architecture.md) | Sơ đồ Mermaid 4 tầng, luồng dữ liệu và quyết định thiết kế |
| **4** | **AI Logs & Tracing** | [`docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md`](docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md) | Tích hợp Langfuse Tracing, đo lường token và ms từng node |
| **5** | **Live URL** | [https://www.nerahome.space/](https://www.nerahome.space/) | Hoạt động trên Internet (Frontend Vercel + Backend Render) |
| **6** | **Video Demo** | [`docs/video-demo.md`](docs/video-demo.md) | Video 5 phút 50 giây, link Google Drive và cấu trúc từng phân đoạn |
| **7** | **Pitch Deck** | [`docs/pitch-deck.pdf`](docs/pitch-deck.pdf) | Slide Demo Day; kịch bản nói ở [`docs/SLIDE_THUYET_TRINH_NERA_DEMO_DAY.md`](docs/SLIDE_THUYET_TRINH_NERA_DEMO_DAY.md) |
| **8** | **Development Journal** | [`docs/journal.md`](docs/journal.md) | Nhật ký phát triển 4 tuần, bài học kinh nghiệm và giải pháp |
| **9** | **Worklog** | [`docs/worklog.md`](docs/worklog.md) | Lịch sử công việc chi tiết theo ngày của các thành viên |
| **10**| **Evaluation Evidence**| [`docs/evaluation.md`](docs/evaluation.md) | 844 tests pass, coverage, bảng Grounding RAG, Cost/Job 5k |

---

## 👥 Đội ngũ Phát triển (Team P-046 / 046LTD)

| Họ và tên | Vai trò chính | Trách nhiệm đảm nhiệm |
|:---|:---|:---|
| **Vũ Thế Lực** | **Product Manager & AI Product Lead** | Định vị sản phẩm O2O, Multi-Agent LangGraph, Data Pipeline (3.796 căn), Eval Suite (844 tests), Token/Cost Tracker, Monetization. 📄 [Xem Portfolio PM & AI Lead](docs/PM_AI_PRODUCT_PORTFOLIO.md) |
| **Phạm Trung Kiên** | **Tech Lead & AI Core Engineer** | Lõi AI Multi-Agent LangGraph, Reasoning đa lượt, Tích hợp Goong Maps & Batch Matrix, CSDL PostgreSQL 18 bảng, Redis Fallback, Backend FastAPI & Frontend Next.js. 📄 [Xem Portfolio Tech Lead](docs/TECH_LEAD_AI_CORE_PORTFOLIO.md) |
| **Nguyễn Thế Anh** | **QA & Memory Engineer** | Test API và routing, đánh giá RAGAS, tích hợp Mem0 service (`src/services/mem0_service.py`). 📄 [Xem Portfolio QA & Memory](docs/QA_MEMORY_PORTFOLIO.md) |
| **Lê Tiến Đạt** | **Prototype & Docs Engineer** | MOCKUI prototype, tài liệu PRD/brief, cấu hình Redis, thiết lập AI logs hooks. 📄 [Xem Portfolio Prototype & Docs](docs/PROTOTYPE_DOCS_PORTFOLIO.md) |

---

## 🏛️ Kiến trúc Hệ thống

GitHub render Mermaid ngay trong README. Sơ đồ đầy đủ bốn tầng, luồng dữ liệu và
các quyết định thiết kế nằm ở [`docs/architecture.md`](docs/architecture.md);
riêng đồ thị tác tử ở [`docs/guide/architecture_diagram.md`](docs/guide/architecture_diagram.md).

```mermaid
graph LR
    subgraph Client["Frontend · Next.js / Vercel"]
        UI["/chat · /sale · /admin · /my-bookings"]
    end

    subgraph API["Backend · FastAPI / Render"]
        Router["Router /api/v1"]
        Auth["Auth & RBAC<br/>JWT + HttpOnly cookie"]
        Hold["Hold Engine<br/>giữ chỗ 15 phút"]
    end

    subgraph Agent["Multi-Agent · LangGraph"]
        SUP["supervisor"]
        INV["inventory"]
        BOK["booking"]
        ASG["assignment"]
        HIT["hitl"]
        RSP["respond"]
    end

    subgraph Data["Dữ liệu"]
        PG[("PostgreSQL<br/>18 bảng · 3.796 BĐS")]
        RD[("Redis<br/>fallback bộ nhớ")]
    end

    subgraph Ext["Dịch vụ ngoài"]
        LLM["OpenRouter"]
        GOONG["Goong Maps"]
        LF["Langfuse"]
    end

    UI -->|REST + SSE| Router
    Router --> Auth --> PG
    Router --> Hold --> PG
    Router --> SUP

    SUP --> INV --> RSP
    SUP --> BOK
    SUP --> ASG
    BOK -->|chờ duyệt| HIT
    ASG -->|chờ duyệt| HIT
    HIT --> RSP

    INV --> PG
    INV --> GOONG
    SUP --> LLM
    RSP --> LLM
    SUP -.-> RD
    Agent -.->|trace| LF
```

Ba điểm đáng chú ý trong sơ đồ:

- **Không có vector store.** Kết quả tìm kiếm đến từ câu lệnh SQL trên bảng
  `properties` sau khi bộ trích xuất chốt ràng buộc cứng, nên mọi con số trong
  câu trả lời đều truy ngược được về một bản ghi có thật.
- **`hitl` là cổng chặn bắt buộc.** Một lịch hẹn chỉ chuyển sang `CONFIRMED` sau
  khi nhân viên sale bấm duyệt; AI không tự chốt lịch.
- **Redis có đường lui.** Redis chết thì trạng thái hội thoại rơi về bộ nhớ tiến
  trình, phiên chat không đứt.

## ⚡ Hướng dẫn Cài đặt & Chạy ứng dụng

### Cách 1: Chạy trực tiếp trên máy cục bộ (Windows / macOS / Linux)

#### 1. Yêu cầu môi trường
- Python 3.11+
- Node.js 20+ & npm
- PostgreSQL 15+ & Redis (tùy chọn — có sẵn In-Memory Fallback)

#### 2. Cài đặt Backend
```powershell
# Tại thư mục gốc dự án
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

#### 3. Khởi tạo Cơ sở dữ liệu PostgreSQL
Cập nhật `DATABASE_URL` trong `.env`, sau đó chạy lần lượt các script khởi tạo CSDL:
```powershell
psql -U visitops -d visitops -f database/001_schema.sql
psql -U visitops -d visitops -f database/002_seed.sql
psql -U visitops -d visitops -f database/004_crawled_data.sql
psql -U visitops -d visitops -f database/005_batdongsan_data.sql
psql -U visitops -d visitops -f database/006_saved_properties.sql
psql -U visitops -d visitops -f database/007_customer_memory.sql
```

#### 4. Chạy Backend Server
```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```
> Swagger API Documentation có sẵn tại: `http://localhost:8000/docs`

#### 5. Cài đặt & Chạy Frontend
Mở Terminal thứ hai:
```powershell
cd frontend
npm install
npm run dev
```
> Giao diện người dùng sẽ chạy tại: `http://localhost:3005` (hoặc `http://localhost:3000`)

---

### Cách 2: Chạy toàn bộ hệ thống bằng Docker Compose

```powershell
docker compose up --build
```
Hệ thống sẽ tự động khởi tạo 4 containers: PostgreSQL, Redis, Backend FastAPI (cổng 8000) và Frontend Next.js (cổng 3000).

---

## 🔑 Tài khoản Demo (Test Credentials)

Các tài khoản dưới đây được thiết lập sẵn trên môi trường demo (Mật khẩu: `Demo@123` hoặc `123456`):

| Vai trò (Role) | Email đăng nhập | Quyền hạn & Giao diện tương ứng |
|:---|:---|:---|
| **Khách hàng (Customer)** | `customer.demo@example.com` | Chat tìm nhà, so sánh, đặt lịch xem tại `/`, `/chat`, `/my-bookings` |
| **Chuyên viên Sale** | `kien.sale@example.com` | Quản lý và phê duyệt lịch hẹn xem nhà, xem lộ trình tại `/sale` |
| **Quản trị viên (Admin)** | `admin.demo@example.com` | Theo dõi tổng thể hệ thống, KPIs, quản lý BĐS và user tại `/admin` |

---

## 🛠️ Danh mục Biến Môi trường (.env Variables)

| Tên biến | Mô tả | Mẫu giá trị (Không ghi secret thật) |
|:---|:---|:---|
| `APP_ENV` | Môi trường chạy | `development` / `production` / `test` |
| `DATABASE_URL` | Kết nối PostgreSQL | `postgresql+asyncpg://user:pass@localhost:5432/db` |
| `JWT_SECRET_KEY` | Khóa ký phiên JWT | `random-secret-key-at-least-32-chars` |
| `OPENAI_API_KEY` | API Key cho LLM | `sk-...` |
| `OPENROUTER_API_KEY` | API Key cho OpenRouter | `sk-or-v1-...` |
| `GOONG_API_KEY` | API Key dịch vụ bản đồ Goong | `your-goong-api-key` |
| `LANGFUSE_PUBLIC_KEY` | Key công khai cho Tracing | `pk-lf-...` |
| `LANGFUSE_SECRET_KEY` | Key bảo mật cho Tracing | `sk-lf-...` |

---

## 📡 Danh mục API Endpoints Chính

| Phương thức | Đường dẫn Endpoint | Vai trò | Chức năng |
|:---|:---|:---:|:---|
| `GET` | `/health` | Public | Kiểm tra trạng thái hoạt động backend, DB & Redis |
| `POST` | `/api/v1/auth/login` | Public | Đăng nhập tài khoản, thiết lập HttpOnly Cookie |
| `POST` | `/api/v1/chat` | Customer | Gửi tin nhắn và nhận phản hồi từ AI Multi-Agent |
| `POST` | `/api/v1/chat/stream` | Customer | Streaming phản hồi AI qua Server-Sent Events (SSE) |
| `GET` | `/api/v1/properties` | Public | Lấy danh sách BĐS từ kho 3.796 căn thật |
| `POST` | `/api/v1/bookings/hold` | Customer | Tạo bản ghi giữ chỗ 15 phút (`PropertyHold`) |
| `GET` | `/api/v1/sale/appointments` | Sale | Danh sách lịch hẹn cần xử lý của Sale |
| `POST` | `/api/v1/sale/appointments/{id}/accept` | Sale | Sale phê duyệt lịch hẹn (Human-In-The-Loop) |
| `GET` | `/api/v1/admin/analytics/kpi` | Admin | Thống kê tỷ lệ chuyển đổi, no-show rate, số booking |

---

## 🏗️ Cấu trúc Thư mục Dự án (Directory Tree)

```text
P-046/
├── README.md                      # Deliverable #2 — Giới thiệu tổng quan dự án
├── ARCHITECTURE.md                # Con trỏ sang docs/architecture.md
├── JOURNAL.md                     # Con trỏ sang docs/journal.md
├── WORKLOG.md                     # Con trỏ sang docs/worklog.md
├── Dockerfile                     # Docker build cho Backend FastAPI
├── docker-compose.yml             # Khởi chạy Postgres, Redis, Backend, Frontend
├── requirements.txt               # Danh sách thư viện Python
├── docs/                          # Thư mục Deliverables chính thức
│   ├── architecture.md            # Deliverable #3 — Kiến trúc hệ thống
│   ├── video-demo.md              # Deliverable #6 — Kịch bản & Link Video Demo
│   ├── pitch-deck.pdf             # Deliverable #7 — Slide thuyết trình Demo Day
│   ├── journal.md                 # Deliverable #8 — Development Journal
│   ├── worklog.md                 # Deliverable #9 — Nhật ký công việc
│   ├── evaluation.md              # Deliverable #10 — Bằng chứng đánh giá
│   ├── evaluation/                # Báo cáo audit đánh giá chuyên sâu
│   └── demo/                      # Scripts demo, hình ảnh và brand assets
├── src/                           # Deliverable #1 — Mã nguồn Backend
│   ├── main.py                    # Entry point FastAPI app & Exception handler
│   ├── config.py                  # Cấu hình Pydantic settings
│   ├── agents/                    # LangGraph Multi-Agent Engine
│   │   ├── graph.py               # StateGraph định tuyến chính
│   │   ├── state.py               # Agent State definition
│   │   └── nodes/                 # Supervisor, Inventory, Booking, HITL, Respond
│   ├── api/                       # API Routers (Auth, Chat, Sale, Admin, Bookings)
│   ├── database/                  # Kết nối Async SQLAlchemy & Models ORM
│   ├── services/                  # Business Logic (Hold, Geo, Affordability, Token)
│   └── utils/                     # Tiện ích chuẩn hóa tên, thời gian, text
├── frontend/                      # Ứng dụng Next.js 14 App Router
│   ├── src/app/                   # App routes (chat, properties, sale, admin, bookings)
│   ├── src/components/            # UI components (PropertyCard, MapIframe, Typewriter)
│   └── public/                    # Logo, Favicon, OG Image
├── tests/                         # Bộ 844 Automated Tests
│   ├── test_golden_set.py         # Replay 222 kịch bản Golden Scenarios
│   ├── test_geo_tool_failure.py   # Kiểm thử khi Goong Maps lỗi (SEV-0)
│   ├── test_hitl_no_false_conf.py # Kiểm thử chống xác nhận giả HITL (SEV-0)
│   ├── test_property_hold_conc.py # Kiểm thử khóa đồng thời chống Double-booking (SEV-0)
│   └── test_token_usage.py        # Đo lường token và chi phí runtime
└── .github/workflows/             # CI/CD Pipeline
    └── ci.yml                     # Tự động hóa Lint (ruff), Pytest, Build Frontend
```

---

## 🧪 Chạy Bộ Kiểm Thử Tự Động (844 Tests)

```powershell
# Chạy toàn bộ 844 tests
.\.venv\Scripts\python.exe -m pytest tests/ -v

# Chạy kiểm thử kèm đo lường Code Coverage
.\.venv\Scripts\python.exe -m pytest tests/ --cov=src --cov-report=term-missing
```

---

<div align="center">
  <sub>Xây dựng bởi Team <b>046LTD</b> · AI20K Build Phase Cohort 3 · 2026</sub>
</div>
