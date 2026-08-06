# PostgreSQL cho XHome VisitOps

Đây là schema MVP gồm đúng 18 bảng cho luồng tư vấn, chọn căn, sale duyệt,
đặt lịch và giữ căn. Seller lấy từ nguồn công khai được lưu riêng, không trở
thành tài khoản đăng nhập.

## Cấu trúc

- `001_schema.sql`: 18 bảng MVP, constraint, index, trigger, view và hàm hết hạn.
- `002_seed.sql`: 10 user demo, 5 customer, 3 sale, dự án và bất động sản mẫu.
- `003_smoke_test.sql`: kiểm tra số lượng dữ liệu, seller, sale, HITL và chống đặt trùng sale/căn.
- `004_crawled_data.sql`: 108 căn Nhà Tốt, 98 seller nguồn và 750 ảnh.
- `005_batdongsan_data.sql`: 60 tin Batdongsan đạt chuẩn, 58 seller và 612 ảnh.
- `batdongsan_records.json`: checkpoint các bản ghi đã chuẩn hóa để crawl tiếp.
- `batdongsan_crawl_report.json`: thống kê chất lượng và lý do loại tin.

## Khởi chạy

Từ thư mục `P-046`:

```bash
copy .env.example .env
docker compose up -d db
docker compose logs -f db
```

PostgreSQL tự chạy `001`, `002`, `004`, `005` theo thứ tự khi volume được tạo lần đầu.
Các file crawl phụ thuộc sale profile trong `002_seed.sql`, vì vậy không đổi thứ tự này.

Để tạo lại hoàn toàn database local và chấp nhận xóa volume PostgreSQL hiện tại:

```bash
docker compose down -v
docker compose up -d db
docker compose logs -f db
```

Không chạy lệnh xóa volume nếu database đang có dữ liệu cần giữ lại. Password trong seed
chỉ là placeholder, cần thay bằng Argon2id thật trước khi bật đăng nhập.

### Tạo mới bằng pgAdmin

Tạo một database rỗng tên `visitops`, mở Query Tool của đúng database đó và lần lượt
dùng **File → Open** rồi Execute toàn bộ các file:

```text
001_schema.sql
002_seed.sql
004_crawled_data.sql
005_batdongsan_data.sql
003_smoke_test.sql
```

Không thêm `\set ON_ERROR_STOP on` khi chạy bằng Query Tool; đó là lệnh riêng của
`psql`, không phải cú pháp PostgreSQL. Nếu tạo lại từ database cũ, hãy sao lưu trước,
drop database cũ bằng giao diện pgAdmin rồi tạo database rỗng mới.

Chạy smoke test:

```bash
docker compose exec -T db \
  psql -U visitops -d visitops < database/003_smoke_test.sql
```

Kết quả mong đợi:

```text
PASS: exact 18-table database counts and seller/sale links are complete
PASS: appointment cannot be created before HITL approval
PASS: overlapping sale/property booking was rejected
PASS: appointment details cannot differ from sale approval
```

## Crawl dữ liệu căn bán thật

Pipeline chuẩn hóa bất động sản, ảnh, seller nguồn và quan hệ seller–căn. Người đăng trên
Nhà Tốt không bị biến thành tài khoản đăng nhập. Mỗi căn mới chỉ được gán một trong ba
sale demo nội bộ khi căn đó chưa có sale chính; crawler không sinh customer hay lịch hẹn.

```bash
python database/crawler_chotot.py \
  --listing-type SALE \
  --target 200 \
  --output database/properties.json \
  --report database/crawl_report.json

python database/generate_sql_from_json.py \
  --input database/properties.json \
  --output database/004_crawled_data.sql
```

Crawler gọi cả endpoint danh sách và endpoint chi tiết, lấy trực tiếp `price`
theo VND và `size` theo m². Tin chỉ được giữ khi còn active/accepted và có đủ:

- tiêu đề, mô tả, loại giao dịch, giá và diện tích;
- địa chỉ đủ phường/quận/tỉnh, tọa độ;
- phòng ngủ, phòng vệ sinh, tầng, hướng, pháp lý và nội thất;
- loại căn, người đăng nguồn, thời gian đăng;
- ít nhất ba URL ảnh HTTPS duy nhất.

Thiếu bất kỳ trường nào thì tin bị bỏ qua và lý do được thống kê trong
`crawl_report.json`. Mặc định chỉ lấy tin bán vì schema hiện dùng `list_price`
như tổng giá bán; có thể chủ động chọn `RENT` hoặc `ALL`, nhưng ứng dụng phải đọc
`features.listing_type` và `features.price_period` để không trộn giá.

`004_crawled_data.sql` dùng UUID ổn định, upsert có conflict target và transaction
toàn khối. File tạo 98 `external_sellers`, 108 `property_external_sellers`, đồng thời
phân công sale nội bộ cho 108 căn. Có thể nhập bằng:

```bash
docker compose exec -T db \
  psql -v ON_ERROR_STOP=1 -U visitops -d visitops \
  < database/004_crawled_data.sql
```

## Crawl riêng Batdongsan.com.vn

`crawler_batdongsan.py` nhận cả URL tin chi tiết và URL danh sách. Script tự sinh
SQL PostgreSQL riêng, không dùng chung JSON hoặc generator của Nhà Tốt.

Kiểm thử riêng một tin đất mà không ghi đè batch chính:

```bash
python database/crawler_batdongsan.py \
  "https://batdongsan.com.vn/ban-dat-phuong-hung-thang-1/ban-o-goc-canh-nha-o-xa-hoi-bim-bai-chay-ha-long-gia-au-tu-pr46093955" \
  --target 1 \
  --max-pages 1 \
  --records-output database/batdongsan_sample_records.json \
  --report database/batdongsan_sample_report.json \
  --output database/005_batdongsan_sample.sql
```

Crawl từ trang bán toàn quốc, tiếp tục sang `/p2`, `/p3`, ... và ghi checkpoint
sau từng tin đạt chuẩn:

```bash
python database/crawler_batdongsan.py \
  "https://batdongsan.com.vn/nha-dat-ban" \
  --target 0 \
  --max-pages 10 \
  --delay 2.5 \
  --jitter 0.5 \
  --resume \
  --records-output database/batdongsan_records.json \
  --report database/batdongsan_crawl_report.json \
  --output database/005_batdongsan_data.sql
```

Bỏ `--resume` khi muốn tạo checkpoint mới. Khi crawl tiếp, `--resume` bỏ qua các
ID đã có và hợp nhất tin mới vào cùng JSON/SQL. Nếu website yêu cầu CAPTCHA hoặc
từ chối truy cập, crawler dừng mạng và giữ nguyên dữ liệu đã checkpoint.

Crawler giữ toàn bộ bảng `Đặc điểm bất động sản` trong `features.raw_attributes`
và chuẩn hóa các trường phù hợp với từng loại `LAND`, `APARTMENT`, `HOUSE`,
`VILLA`, `TOWNHOUSE`, `COMMERCIAL`. Seller nguồn được upsert vào `external_sellers`
và liên kết qua `property_external_sellers`; seller không được biến thành `users`.
Căn mới nhận sale demo nội bộ nếu chưa có sale chính, nhưng crawler không sinh lịch hẹn.

Ngoài các cột chính (giá, diện tích, địa chỉ, tọa độ, phòng, hướng, pháp lý, mặt
tiền, đường vào), `features` còn giữ thông tin dự án, người đăng công khai, ngày
đăng/hết hạn, loại tin, lịch sử giá khả dụng, giá biến động, thuộc tính gốc và URL
video nguồn. Video chưa xác minh khả năng phát trực tiếp chỉ được giữ làm metadata;
`property_media` chỉ nhận URL ảnh công khai. Số điện thoại đã che được giữ nguyên để
đối chiếu nguồn, còn số/email hiện đầy đủ trong nội dung tự do sẽ được ẩn trước khi
ghi SQL.

Script chỉ đọc dữ liệu công khai, tôn trọng `robots.txt`, chờ tối thiểu 2 giây giữa
hai request, không bấm `Hiện số` và không vượt CAPTCHA. Nếu Cloudflare trả trang
xác minh, tiến trình dừng mạng và giữ checkpoint đã xác minh. Tin thiếu trường bắt
buộc theo loại, thiếu seller, tọa độ, pháp lý hoặc dưới ba ảnh sẽ bị bỏ qua.

Batch hiện tại quét có giới hạn 10 trang bán toàn quốc và giữ 60/201 URL ứng viên:
37 căn hộ, 9 nhà riêng, 6 biệt thự, 5 đất và 3 bất động sản thương mại tại 13
tỉnh/thành. Tất cả 60 tin đều có seller cùng số điện thoại đã che, pháp lý, tọa độ
và ít nhất ba ảnh; tổng cộng 58 seller duy nhất và 612 ảnh.

`005_batdongsan_data.sql` không chứa lệnh meta `\set`, không ghi đè trạng thái
nghiệp vụ như `SOLD`, và chỉ
làm mới media mang nhãn nguồn Batdongsan.com.vn nên có thể chạy trong pgAdmin
Query Tool.

Nhập file bằng pgAdmin Query Tool hoặc `psql`:

```bash
docker compose exec -T db \
  psql -v ON_ERROR_STOP=1 -U visitops -d visitops \
  < database/005_batdongsan_data.sql
```

## 18 bảng canonical của MVP

1. `users`
2. `customer_profiles`
3. `sale_profiles`
4. `projects`
5. `properties`
6. `external_sellers`
7. `property_external_sellers`
8. `property_media`
9. `property_sale_assignments`
10. `sale_unavailability`
11. `conversations`
12. `messages`
13. `tour_requests`
14. `tour_slot_options`
15. `approval_requests`
16. `appointments`
17. `property_holds`
18. `notifications`

Tối ưu lộ trình, quản lý đội xe, bản đồ tiện ích, memory, tự động dời lịch,
analytics và audit được để ngoài schema MVP. Khi nhóm triển khai các phần nâng
cao này, hãy thêm bằng migration riêng thay vì đưa bảng trống vào lần khởi tạo.

## Quy tắc backend bắt buộc

1. LLM chỉ gọi domain tool; không được chạy SQL trực tiếp.
2. Chỉ tạo `appointments` sau khi `approval_requests.status = 'APPROVED'`.
3. Chi tiết appointment phải trùng với giờ và sale đã được duyệt.
4. Constraint PostgreSQL tự chặn trùng sale và căn.
5. Trước khi tạo hold mới, gọi `expire_stale_booking_records()` trong transaction.
6. Khi hủy/dời appointment, trigger tự giải phóng hold.
7. Worker gọi `expire_stale_booking_records()` mỗi phút.
8. OAuth token thật phải nằm trong secret manager; database chỉ giữ secret reference.
9. `messages.content_redacted` không lưu số điện thoại/email chưa che.

## Thay đổi database sau khi web đã chạy

Không chạy lại `001_schema.sql` trên database có dữ liệu. Dùng Alembic:

```bash
alembic revision -m "add new feature"
alembic upgrade head
```

Xem [thiết kế database](../docs/database-design.md) để biết ERD và luồng transaction.
