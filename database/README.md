# PostgreSQL cho XHome VisitOps

Đây là schema cân bằng để nhóm có thể làm web trước, sau đó triển khai các tính
năng nâng cao mà không phải thiết kế lại database.

## Cấu trúc

- `001_schema.sql`: 24 bảng, constraint, index, trigger, view và hàm hết hạn.
- `002_seed.sql`: tài khoản demo, sale, xe, dự án, căn hộ, đất và dữ liệu bản đồ.
- `003_smoke_test.sql`: kiểm tra HITL và chống đặt trùng lịch.

## Khởi chạy

Từ thư mục `P-046`:

```bash
copy .env.example .env
docker compose up -d db
docker compose logs -f db
```

PostgreSQL tự chạy `001_schema.sql` và `002_seed.sql` khi volume được tạo lần đầu.

Chạy smoke test:

```bash
docker compose exec -T db \
  psql -U visitops -d visitops < database/003_smoke_test.sql
```

Kết quả mong đợi:

```text
PASS: overlapping sale/property/vehicle booking was rejected
PASS: appointment details cannot differ from sale approval
```

## Crawl dữ liệu căn bán thật

Pipeline crawl chỉ ghi dữ liệu bất động sản và ảnh. Người đăng trên Nhà Tốt
không được biến thành tài khoản sale nội bộ; crawler cũng không sinh customer,
lịch hẹn hoặc dữ liệu Faker.

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
toàn khối. Có thể nhập bằng:

```bash
docker compose exec -T db \
  psql -v ON_ERROR_STOP=1 -U visitops -d visitops \
  < database/004_crawled_data.sql
```

## 17 bảng dùng cho web cơ bản

1. `users`
2. `customer_profiles`
3. `sale_profiles`
4. `vehicles`
5. `projects`
6. `properties`
7. `property_media`
8. `property_sale_assignments`
9. `sale_unavailability`
10. `conversations`
11. `messages`
12. `tour_requests`
13. `tour_slot_options`
14. `approval_requests`
15. `appointments`
16. `property_holds`
17. `notifications`

## 7 bảng dùng cho nâng cao và vận hành

1. `customer_preferences`: memory khung giờ và nhu cầu khách.
2. `route_plans`: kết quả tối ưu lịch trình theo ngày.
3. `route_stops`: thứ tự điểm đón, căn và showroom.
4. `reschedule_proposals`: phương án tự động dời lịch.
5. `nearby_places`: cache tiện ích từ Google Maps/Mapbox.
6. `analytics_events`: dữ liệu tính booking success, no-show và latency.
7. `audit_logs`: truy vết thao tác quan trọng.

Các bảng nâng cao có thể để trống trong giai đoạn MVP, không ảnh hưởng hoạt động
của các bảng cơ bản.

## Quy tắc backend bắt buộc

1. LLM chỉ gọi domain tool; không được chạy SQL trực tiếp.
2. Chỉ tạo `appointments` sau khi `approval_requests.status = 'APPROVED'`.
3. Chi tiết appointment phải trùng với giờ, sale và xe mà sale đã duyệt.
4. Constraint PostgreSQL tự chặn trùng sale, căn và xe.
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
