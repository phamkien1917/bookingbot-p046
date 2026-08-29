-- 009_geocode_coordinates_enrichment.sql
-- Bổ sung tọa độ chuẩn Hà Nội cho các BĐS chưa có hoặc sai lệch tọa độ
-- để hỗ trợ Goong Maps Geocoding & Distance Matrix hoạt động chính xác.

BEGIN;

-- Cầu Giấy (Khu vực ĐHQG, Duy Tân, Nghĩa Đô)
UPDATE properties
SET latitude = 21.0333, longitude = 105.7933
WHERE district ILIKE '%Cầu Giấy%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Đống Đa (Khu vực Ngã Tư Sở, Chùa Bộc, Láng)
UPDATE properties
SET latitude = 21.0180, longitude = 105.8280
WHERE district ILIKE '%Đống Đa%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Ba Đình (Khu vực Liễu Giai, Hoàng Hoa Thám, Đội Cấn)
UPDATE properties
SET latitude = 21.0340, longitude = 105.8250
WHERE district ILIKE '%Ba Đình%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Hai Bà Trưng (Khu vực Bạch Mai, Phố Huế, Minh Khai)
UPDATE properties
SET latitude = 21.0080, longitude = 105.8520
WHERE district ILIKE '%Hai Bà Trưng%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Thanh Xuân (Khu vực Nguyễn Trãi, Lê Văn Lương, Khuất Duy Tiến)
UPDATE properties
SET latitude = 20.9980, longitude = 105.8080
WHERE district ILIKE '%Thanh Xuân%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Tây Hồ (Khu vực Lạc Long Quân, Võ Chí Công, Quảng An)
UPDATE properties
SET latitude = 21.0720, longitude = 105.8220
WHERE district ILIKE '%Tây Hồ%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Nam Từ Liêm (Khu vực Mỹ Đình, Mễ Trì, Keangnam Landmark 72)
UPDATE properties
SET latitude = 21.0180, longitude = 105.7760
WHERE district ILIKE '%Nam Từ Liêm%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

-- Mặc định cho các BĐS thuộc Hà Nội chưa có tọa độ
UPDATE properties
SET latitude = 21.0285, longitude = 105.8542
WHERE province ILIKE '%Hà Nội%' AND (latitude IS NULL OR longitude IS NULL OR latitude < 20.50 OR latitude > 21.40);

COMMIT;
