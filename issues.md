# issues 1
Dọn dẹp: schema cũ mâu thuẫn, MOCKUI chết, README chỉ có đường dẫn Windows

Nhóm việc dọn dẹp, không gấp, nhưng ảnh hưởng tới người nhận bàn giao.

1. database/mvp/ là bản sao cũ, mâu thuẫn với schema thật
database/mvp/001_schema.sql mô tả 16 bảng. Schema đang dùng có 18.

Người đọc không biết file nào là nguồn đúng. Đề xuất: xoá, hoặc đổi tên thành database/_archive/ kèm một dòng README nói rõ đây là bản cũ.

2. MOCKUI/ không được tham chiếu ở đâu
Không file nào trong repo trỏ tới thư mục này. Nếu còn dùng để đối chiếu thiết kế thì thêm một dòng trong README nói rõ; nếu không thì xoá.

3. README chỉ có đường dẫn Windows, hardcode máy cá nhân
README.md:11,33,40,92 dùng đường dẫn kiểu C:\buildAI\P-046.

Người dùng macOS hoặc Linux không làm theo được, và ngay cả người dùng Windows cũng phải sửa vì đường dẫn là của máy một thành viên cụ thể.

Đề xuất: dùng đường dẫn tương đối, và bổ sung lệnh cho cả hai hệ.

4. README_boilerplate.md chưa điền
File template gốc còn nguyên trong repo. Xoá hoặc điền.

5. Rủi ro SQL injection trong crawler mà chính đội đã ghi nhận
database/generate_sql_from_json.py:402 — đội tự ghi nhận trong docs/demo/GATE2_REPORT.md nhưng chưa sửa.

Hiện có escape tự viết. Script chỉ chạy tay với dữ liệu tự thu thập nên rủi ro thấp, nhưng escape tự viết là thứ nên thay bằng tham số hoá chuẩn khi có thời gian.


# issues 2
Thiếu test: hai service lớn nhất không có test, không có ca từ chối quyền 403

Hai module lớn nhất không có test nào
Module	Số dòng	Test
src/services/redis_service.py	1315	không có
src/services/booking_service.py	874	không có
Bộ test hiện tại 120 ca, chạy sạch và cách ly tốt — không phụ thuộc key, DB hay mạng. Đó là điểm mạnh thật. Nhưng hai file dài nhất trong services/ lại nằm ngoài phạm vi.

Không có test cho từ chối quyền
require_roles (src/api/routes/auth.py:134-140) được dùng nhất quán khắp admin.py và sale.py, và code đọc thì đúng.

Nhưng không có test nào kiểm ca từ chối — người dùng sai vai trò gọi endpoint quản trị phải nhận 403.

Đây là loại test đáng giá nhất cho phân quyền: nó bắt được lỗi khi ai đó vô tình gỡ decorator hoặc thêm route mới mà quên.

Một test hiện đang lấy lệ
tests/test_mem0_service.py:183-199 chỉ assert hasattr(...) và kiểm chữ ký hàm. Nó xanh kể cả khi thân hàm rỗng.

Đối chiếu với test tốt trong cùng repo: tests/test_search_criteria_service.py:261-284 là regression thật, docstring giải thích bug thật; tests/test_google_oauth.py:12 kiểm giả mạo chữ ký thật.

Đề xuất
Thêm test cho đường đi chính của booking_service — đặt lịch, huỷ, trùng lịch.
Thêm test 403 cho mỗi nhóm vai trò.
Viết lại test_mem0_service.py:183-199 thành test hành vi, hoặc bỏ.

# issues 3
Rò rỉ thông tin: token Calendar lưu plaintext, str(e) trả ra client, /docs mở ở production

Ba vấn đề nhỏ hơn nhưng cùng nhóm: thông tin không nên ra khỏi máy chủ.

1. Token Google Calendar lưu plaintext
src/api/routes/google_oauth.py:223-225 gán thẳng calendar_access_token và calendar_refresh_token vào cột DB, không mã hoá.

Refresh token của Google không tự hết hạn. Ai đọc được bảng users là truy cập được lịch của người dùng, kể cả sau khi họ đăng xuất khỏi ứng dụng.

Đề xuất: mã hoá at rest, hoặc lưu ở kho bí mật riêng.

2. Rò nội dung lỗi ra client
src/api/routes/auth.py:60 — detail=f"Registration error: {str(e)}" trong except Exception
src/api/routes/sale.py:129-130 — detail=str(e) khi trả 500
Lỗi SQLAlchemy nhúng cả câu SQL và tham số vào thông điệp. Nên đây không phải thông báo vô hại — nó lộ cấu trúc bảng và giá trị đang xử lý.

Đề xuất: trả thông điệp chung cho client, ghi chi tiết vào log máy chủ. Thêm exception handler toàn cục — hiện chưa có.

3. /docs, /redoc, /openapi.json mở ở mọi môi trường
src/main.py:135-140 gọi FastAPI(...) mà không set docs_url=None, redoc_url=None, openapi_url=None.

Toàn bộ bề mặt API công khai cho bất kỳ ai truy cập được máy chủ.

Đề xuất: tắt ở production, hoặc đặt sau xác thực.

# issues 4
ruff đỏ trên main: thiếu import Path làm auto_seed_if_empty() ném NameError

Vấn đề
ruff check src/ tests/ — đúng lệnh CI đang cấu hình — đỏ trên main:

F821 Undefined name 'Path'   src/main.py:46
src/main.py:46 dùng Path(__file__).parent.parent nhưng phần import ở đầu file không có pathlib.

Đây không chỉ là lỗi lint
Dòng 46 nằm trong auto_seed_if_empty(). Khi hàm này chạy, nó ném NameError chứ không phải cảnh báo. Auto-seed hỏng hoàn toàn ở lần khởi động đầu tiên.

Nghĩa là người mới clone repo về, chạy lần đầu, sẽ gặp lỗi ở đúng bước làm cho ứng dụng có dữ liệu để dùng.

Vì sao không ai phát hiện
CI của repo chưa từng chạy thành công — 100/100 lượt gần nhất đều hỏng. Nguyên nhân nằm ở billing của tổ chức, không phải lỗi của đội, nhưng hệ quả là không có ai báo lỗi lint này suốt thời gian qua.

Đề xuất sửa
Thêm from pathlib import Path vào đầu src/main.py.
Chạy ruff check src/ tests/ tại chỗ và dọn hết lỗi còn lại trước khi CI được bật lại.
Hai nhánh pr/fix-ruff-lint-errors và pr/fix-remaining-ruff-errors đang treo chưa merge — xử lý hoặc đóng.
Cân nhắc thêm pre-commit hook chạy ruff check, để không phụ thuộc hoàn toàn vào CI.

#issues 5
Bảo mật nghiêm trọng: verify_password chấp nhận mật khẩu demo ở mọi môi trường, phủ cả tài khoản ADMIN

Vấn đề
src/services/auth_service.py:24-26:

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password == DEMO_PASSWORD_HASH:
        return plain_password in {DEMO_PASSWORD, LEGACY_DEMO_PASSWORD}
DEMO_PASSWORD_HASH là chuỗi placeholder "DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH" (dòng 19). Bất kỳ user nào trong DB mang đúng chuỗi đó ở cột password_hash đều đăng nhập được bằng Demo@123 hoặc 123456.

Không có kiểm APP_ENV ở bất kỳ đâu trong hàm này. Nhánh demo chạy y hệt ở mọi môi trường.

database/002_seed.sql gán đúng chuỗi placeholder đó cho 10 tài khoản, trong đó có:

admin.demo@example.com — vai trò ADMIN (dòng 58)
nhiều tài khoản SALE và COORDINATOR
Nghĩa là nếu seed này từng được nạp vào một môi trường thật, tài khoản quản trị mở bằng mật khẩu Demo@123.

Tài liệu đang mô tả một chốt bảo mật không tồn tại
ARCHITECTURE.md:118 viết:

Password hash bcrypt; tài khoản demo password chỉ được chấp nhận khi APP_ENV=development.

Điều này không đúng với code. auth_service.py không tham chiếu APP_ENV ở đâu cả.

Đây là phần đáng lo hơn cả bản thân lỗi: người đọc tài liệu sẽ tin rằng đã có chốt chặn và không đi kiểm lại.

Ghi nhận
Auto-seed chỉ chạy ở môi trường dev (src/main.py:95). Nên rủi ro thực tế phụ thuộc vào việc seed có từng được nạp tay vào production hay không. Điều này chưa xác minh được từ bên ngoài — đội tự kiểm nhanh hơn.

Đề xuất sửa
Bỏ hẳn nhánh demo trong verify_password. Nếu cần tài khoản demo, hãy hash mật khẩu thật bằng bcrypt như mọi tài khoản khác.
Nếu vẫn muốn giữ, tối thiểu phải bọc trong kiểm settings.app_env == "development".
Kiểm production: có bản ghi nào mang password_hash = 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH' không. Nếu có, đổi ngay.
Sửa ARCHITECTURE.md:118 cho khớp code, hoặc sửa code cho khớp tài liệu.
Thêm test: tài khoản có hash placeholder không đăng nhập được khi APP_ENV != development.

#issues 6
Bảo mật nghiêm trọng: tài khoản Google OAuth có mật khẩu suy ra từ email, đăng nhập được qua form thường

Vấn đề
Tài khoản tạo qua Google OAuth có mật khẩu suy ra được từ chính email, và đăng nhập bằng form mật khẩu thường vẫn chấp nhận nó.

src/api/routes/google_oauth.py:166 — khi người dùng đăng nhập Google lần đầu và chưa có tài khoản:

password_hash=get_password_hash(f"gauth_{email}")
Email đã được chuẩn hoá .lower().strip() ở dòng 151, nên giá trị hoàn toàn đoán được.

src/services/auth_service.py:28 — verify_password chỉ gọi bcrypt.checkpw. Không có cờ nào đánh dấu tài khoản là OAuth-only, và model User cũng không có trường như vậy.

Kết quả: ai biết email của một người đã đăng nhập bằng Google đều đăng nhập được vào tài khoản đó qua POST /auth/login với mật khẩu gauth_<email>.

Không cần điều kiện gì thêm. Đây là đường đi bình thường của ứng dụng, không phải nhánh dev hay fallback.

Đề xuất sửa
Không đặt mật khẩu suy ra được. Với tài khoản tạo qua OAuth, để password_hash là NULL, hoặc sinh chuỗi ngẫu nhiên không ai biết.
Thêm trường phân biệt nguồn xác thực trên User (ví dụ auth_provider). Đăng nhập bằng mật khẩu phải từ chối tài khoản OAuth-only.
Kiểm tra dữ liệu hiện có. Mọi tài khoản đã tạo qua đường này đang mang mật khẩu đoán được — cần reset.
Thêm test hồi quy: tài khoản tạo qua Google không đăng nhập được bằng gauth_<email>.