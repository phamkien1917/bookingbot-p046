# 🤖 Booking Bot AI - Hệ thống Đặt lịch & Tư vấn Bất động sản

Dự án **P-046** là một trợ lý AI thông minh (AI Agent) chuyên hỗ trợ khách hàng tìm kiếm bất động sản, phân tích nhu cầu cá nhân hóa, và đặt lịch xem nhà trực tiếp. Hệ thống bao gồm Backend (FastAPI + LangGraph) và Frontend (Next.js).

---

## 📋 Yêu cầu hệ thống (Prerequisites)
Để chạy dự án trên máy cá nhân, bạn cần cài đặt các công cụ sau:
- **Python 3.10+** (Cho Backend)
- **Node.js 18+** (Cho Frontend)
- **PostgreSQL** (Cơ sở dữ liệu chính)
- **Git**

---

## 🚀 Hướng dẫn cài đặt chi tiết

### Bước 1: Clone dự án
```bash
git clone https://github.com/AI20K-Build-Phase-Cohort-3/P-046.git
cd P-046
git checkout develop
```
*(Lưu ý: Code mới nhất hiện đang nằm ở nhánh `develop`)*

---

### Bước 1.5: Khởi tạo Cơ sở dữ liệu (PostgreSQL)
Dự án yêu cầu bạn phải có sẵn PostgreSQL. Dưới đây là cách tạo và nạp dữ liệu mồi (seed data) bằng công cụ `psql` hoặc các phần mềm quản lý DB (như pgAdmin, DBeaver).

1. Mở Terminal (hoặc pgAdmin) và tạo một database mới tên là `test_db`:
```sql
CREATE DATABASE test_db;
```

2. Nạp dữ liệu mẫu vào Database bằng dòng lệnh `psql` (thay `postgres` bằng username của bạn):
```bash
# Trỏ vào thư mục chứa code
cd P-046

# Chạy lần lượt các file SQL theo thứ tự:
psql -U postgres -d test_db -f database/001_schema.sql
psql -U postgres -d test_db -f database/002_seed.sql
psql -U postgres -d test_db -f database/004_crawled_data.sql
psql -U postgres -d test_db -f database/005_batdongsan_data.sql
```
*(Nếu dùng phần mềm pgAdmin, bạn có thể tạo Database `test_db` bằng giao diện, sau đó mở chức năng Query Tool và copy lần lượt nội dung của 4 file SQL trên để chạy).*

---

### Bước 2: Cài đặt và Chạy Backend (FastAPI + AI)

1. **Tạo môi trường ảo (Virtual Environment)**
```bash
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate
# Kích hoạt trên Mac/Linux:
source venv/bin/activate
```

2. **Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

3. **Cấu hình biến môi trường (`.env`)**
Tạo một file `.env` ở thư mục gốc (ngang hàng với thư mục `src`) và sao chép nội dung sau vào:
```env
# Môi trường chạy
APP_ENV=development
DEBUG=true

# Cấu hình Database (Thay đổi user/password cho phù hợp với máy của bạn)
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/test_db

# Cấu hình LLM - Điền API Key của OpenRouter (hoặc OpenAI)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxx
```
*(Lưu ý: Backend có tính năng In-Memory Fallback nên bạn không bắt buộc phải cài đặt Redis).*

4. **Khởi chạy Backend**
```bash
uvicorn src.main:app --reload
```
Hệ thống sẽ tự động tạo các bảng trong Database.
Backend sẽ chạy tại: `http://localhost:8000`

---

### Bước 3: Cài đặt và Chạy Frontend (Next.js)

Mở một cửa sổ Terminal **mới** (giữ nguyên cửa sổ Backend đang chạy):

1. **Di chuyển vào thư mục frontend**
```bash
cd frontend
```

2. **Cài đặt thư viện Node.js**
```bash
npm install
```

3. **Khởi chạy Frontend**
```bash
npm run dev
```
Giao diện người dùng sẽ chạy tại: `http://localhost:3000`

---

## 💻 Trải nghiệm sản phẩm

1. Mở trình duyệt và truy cập `http://localhost:3000` để vào giao diện chính.
2. Bấm vào icon chat hoặc điều hướng sang trang `/chat`.
3. Bắt đầu nhắn tin với AI (VD: *"Tôi muốn tìm thuê căn hộ 2 phòng ngủ ở Đống Đa, giá dưới 10 triệu"*).
4. Quan sát cách AI thu thập thông tin và tự động hiển thị gợi ý.

Chúc bạn cài đặt thành công! 🎉
