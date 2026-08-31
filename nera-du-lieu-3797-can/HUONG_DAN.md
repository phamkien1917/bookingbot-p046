# Nạp kho bất động sản mới lên production

Gói này đưa database production từ 168 căn lên 3.797 căn, phủ 27 tỉnh/thành.
Toàn bộ lệnh đều là upsert nên **không mất** user, booking, lịch hẹn hay hold đang có.

## Vì sao phải nạp tay

`auto_seed_if_empty()` trong `src/main.py` chỉ chạy khi `app_env == "development"`,
mà Render đặt `APP_ENV=production`. Kể cả nếu chạy thì hàm cũng thoát ngay vì bảng
`properties` đã có dữ liệu. Nói cách khác, deploy lại backend sẽ không tự nạp gì thêm —
file SQL trong repo chỉ được `docker-compose` dùng ở máy local.

## Nội dung gói

| File | Nội dung |
|---|---|
| `004_crawled_data.sql` | 3.662 căn hộ Nhà Tốt, 1.745 người đăng, 25.027 ảnh (36 MB) |
| `010_province_normalization.sql` | Gộp `"Hồ Chí Minh"` và `"Tp Hồ Chí Minh"` thành một tên |

## Các bước

### 1. Thêm cột `last_verified_at`

Cột này theo dõi lần cuối một tin được xác nhận còn sống, tách khỏi `updated_at`
vì `updated_at` bị đụng bởi mọi thao tác sửa. Backend đã có runtime migration tạo cột
này lúc khởi động, nhưng chạy trước cũng không sao — lệnh idempotent.

```bash
psql "$DATABASE_URL" -c "ALTER TABLE properties ADD COLUMN IF NOT EXISTS last_verified_at TIMESTAMPTZ;"
psql "$DATABASE_URL" -c "UPDATE properties SET last_verified_at = published_at WHERE last_verified_at IS NULL AND published_at IS NOT NULL;"
```

### 2. Nạp dữ liệu

```bash
psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -f 004_crawled_data.sql
psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -f 010_province_normalization.sql
```

`$DATABASE_URL` là **External Connection String** của Postgres trên Render
(dashboard → service Postgres → Connect → External). Đẩy 36 MB qua mạng mất khoảng
5–15 phút.

Nếu máy không có `psql`, dùng client trong container Postgres của repo:

```bash
docker compose up -d db
docker compose cp 004_crawled_data.sql db:/tmp/004.sql
docker compose cp 010_province_normalization.sql db:/tmp/010.sql
docker compose exec -T db psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -f /tmp/004.sql
docker compose exec -T db psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -f /tmp/010.sql
```

### 3. Kiểm tra

```sql
SELECT count(*) AS can_ho, count(DISTINCT province) AS tinh_thanh FROM properties;
-- mong đợi: 3797 | 27

SELECT count(*) FILTER (WHERE last_verified_at >= now() - interval '30 days') AS con_tuoi,
       count(*) FILTER (WHERE last_verified_at <  now() - interval '30 days') AS can_xac_minh_lai
FROM properties;
-- mong đợi: 3712 | 85

SELECT count(*) FROM properties p
WHERE NOT EXISTS (SELECT 1 FROM property_media m WHERE m.property_id = p.id);
-- mong đợi: 0
```

Xong là web đọc được ngay, không cần redeploy backend.

## Vài điểm cần biết

**Dung lượng.** Database local sau khi nạp là 28 MB. Gói Postgres free của Render cho
1 GB nên thoải mái, nhưng gói free hết hạn 30 ngày kể từ ngày tạo — kiểm tra hạn trước
khi nạp, tránh nạp xong thì mất.

**85 tin hiện "cần xác minh lại".** Đây là tin cũ crawl từ 05/08 mà lần crawl này không
tìm lại được trên nguồn. Badge màu hổ phách đang nói đúng sự thật, không phải lỗi. Sau
05/09 con số này thành 135 (3,6% kho) khi nhóm tin cũ còn lại vượt ngưỡng 30 ngày.
3.662 tin mới có mốc xác minh 31/08, xanh đến 30/09.

**Batdongsan.com.vn đang chặn.** Mọi request tự động nhận HTTP 403, kể cả `robots.txt`.
Crawler dừng sạch thay vì lách, nên 60 tin nhà/đất/biệt thự từ nguồn đó giữ nguyên batch
cũ và sẽ dần chuyển sang trạng thái cần xác minh.

**Muốn crawl lại về sau:** xem `database/README.md` trong repo, phần "Crawl dữ liệu căn
bán thật". Lệnh chính là `crawler_chotot.py --region-id 0` (toàn quốc), rồi
`merge_crawls.py` và `generate_sql_from_json.py`.
