-- 010_province_normalization.sql
-- Hai crawler ghi tên tỉnh theo đúng chuỗi của nguồn, nên cùng một tỉnh xuất hiện
-- dưới hai tên: Nhà Tốt trả "Tp Hồ Chí Minh", Batdongsan trả "Hồ Chí Minh".
-- Hệ quả là mọi phép GROUP BY province đếm thành hai tỉnh, và bộ lọc tìm kiếm chỉ
-- gom được cả hai nhờ ký tự đại diện của ILIKE — một sự may mắn, không phải thiết kế.
--
-- File này chạy sau 004 và 005, an toàn khi chạy lại nhiều lần.

BEGIN;

UPDATE properties
SET province = 'Tp Hồ Chí Minh', updated_at = now()
WHERE province IN ('Hồ Chí Minh', 'TP Hồ Chí Minh', 'TP. Hồ Chí Minh', 'TPHCM', 'Sài Gòn');

UPDATE properties
SET province = 'Hà Nội', updated_at = now()
WHERE province IN ('TP Hà Nội', 'TP. Hà Nội', 'Thành phố Hà Nội');

COMMIT;
