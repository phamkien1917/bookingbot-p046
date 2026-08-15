import sys
import unittest
from copy import deepcopy
from pathlib import Path


DATABASE_DIR = Path(__file__).resolve().parents[1] / "database"
sys.path.insert(0, str(DATABASE_DIR))

import crawler_chotot  # noqa: E402
import generate_sql_from_json  # noqa: E402


def complete_detail_payload() -> dict:
    ad = {
        "list_id": 123456789,
        "subject": "Bán căn hộ 70 m² đầy đủ nội thất",
        "body": "Căn hộ chính chủ có đầy đủ thông tin để kiểm thử pipeline dữ liệu.",
        "type": "s",
        "price": 5_500_000_000,
        "size": 70,
        "street_name": "Phố Nguyễn Chánh",
        "ward_name": "Phường Yên Hoà",
        "area_name": "Quận Cầu Giấy",
        "region_name": "Hà Nội",
        "latitude": 21.021805,
        "longitude": 105.790870,
        "rooms": 2,
        "toilets": 2,
        "floornumber": 12,
        "direction": 3,
        "property_legal_document": 6,
        "furnishing_sell": 1,
        "apartment_type": 1,
        "account_id": 987654,
        "account_name": "Người đăng nguồn",
        "state": "accepted",
        "status": "active",
        "orig_list_time": 1_785_811_812_000,
        "images": [
            "https://cdn.example.com/1.jpg",
            "https://cdn.example.com/2.jpg",
            "https://cdn.example.com/3.jpg",
        ],
        "company_ad": False,
    }
    labels = {
        "address": "Phố Nguyễn Chánh, Phường Yên Hoà, Quận Cầu Giấy, Hà Nội",
        "apartment_type": "Chung cư",
        "property_legal_document": "Sổ hồng riêng",
        "direction": "Đông Nam",
        "furnishing_sell": "Nội thất đầy đủ",
        "balconydirection": "Đông Bắc",
    }
    return {
        "ad": ad,
        "ad_params": {
            key: {"id": key, "value": value} for key, value in labels.items()
        },
    }


class CrawlNormalizationTests(unittest.TestCase):
    def test_numeric_area_is_not_corrupted_by_m2_unit(self):
        normalized, issues = crawler_chotot.normalize_detail(
            complete_detail_payload(),
            crawled_at="2026-08-05T10:00:00Z",
        )

        self.assertEqual([], issues)
        self.assertIsNotNone(normalized)
        self.assertEqual(70.0, normalized["area_sqm"])
        self.assertNotEqual(702.0, normalized["area_sqm"])
        self.assertEqual(5_500_000_000, normalized["price"])
        self.assertEqual("SALE", normalized["listing_type"])
        self.assertEqual("TOTAL", normalized["price_period"])

    def test_missing_floor_is_rejected_in_strict_mode(self):
        payload = complete_detail_payload()
        payload["ad"]["floornumber"] = None
        normalized, issues = crawler_chotot.normalize_detail(
            payload,
            crawled_at="2026-08-05T10:00:00Z",
        )

        self.assertIsNone(normalized)
        self.assertIn("missing_floornumber", issues)
        self.assertIn("invalid_floor_number", issues)

    def test_source_enum_labels_are_used_instead_of_stale_maps(self):
        normalized, _ = crawler_chotot.normalize_detail(
            complete_detail_payload(),
            crawled_at="2026-08-05T10:00:00Z",
        )

        self.assertEqual("Sổ hồng riêng", normalized["legal_status"])
        self.assertEqual("Nội thất đầy đủ", normalized["furniture_status"])
        self.assertEqual("Đông Nam", normalized["orientation"])

    def test_zero_seller_rating_is_not_replaced_by_fallback(self):
        payload = complete_detail_payload()
        payload["ad"]["average_rating_for_seller"] = 0.0
        payload["ad"]["average_rating"] = 4.5

        normalized, issues = crawler_chotot.normalize_detail(
            payload,
            crawled_at="2026-08-05T10:00:00Z",
        )

        self.assertEqual([], issues)
        self.assertEqual(0.0, normalized["seller_rating"])

    def test_semantic_repost_keeps_newest_record(self):
        older, _ = crawler_chotot.normalize_detail(
            complete_detail_payload(),
            crawled_at="2026-08-05T10:00:00Z",
        )
        newer = deepcopy(older)
        older["property_id"] = "P_OLD"
        older["source_listing_id"] = 100
        older["published_at"] = "2026-08-01T10:00:00Z"
        newer["property_id"] = "P_NEW"
        newer["source_listing_id"] = 101
        newer["published_at"] = "2026-08-02T10:00:00Z"

        unique, removed = crawler_chotot.deduplicate_properties([older, newer])

        self.assertEqual(["P_NEW"], [item["property_id"] for item in unique])
        self.assertEqual(["P_OLD"], removed)


class SqlGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.property, issues = crawler_chotot.normalize_detail(
            complete_detail_payload(),
            crawled_at="2026-08-05T10:00:00Z",
        )
        self.assertEqual([], issues)

    def test_sql_is_deterministic_and_normalizes_seller_and_sale_assignment(self):
        first = generate_sql_from_json.generate_sql([self.property])
        second = generate_sql_from_json.generate_sql([self.property])

        self.assertEqual(first, second)
        self.assertIn("BEGIN;", first)
        self.assertIn("COMMIT;", first)
        self.assertNotIn("\\set", first)
        self.assertIn("ON CONFLICT (code) DO UPDATE", first)
        self.assertIn("70.00", first)
        self.assertIn("INSERT INTO external_sellers", first)
        self.assertIn("INSERT INTO property_external_sellers", first)
        self.assertIn("INSERT INTO property_sale_assignments", first)
        self.assertIn("'LISTING_POSTER'", first)
        self.assertIn("AND source = 'NHATOT'", first)
        self.assertIn("status = CASE WHEN properties.status", first)
        self.assertNotIn("INSERT INTO users", first)
        self.assertNotIn("INSERT INTO appointments", first)
        self.assertNotIn("@example.com", first)

    def test_each_property_has_exactly_one_generated_cover(self):
        sql = generate_sql_from_json.generate_sql([self.property])

        self.assertEqual(
            1,
            sql.count("NOT EXISTS (SELECT 1 FROM property_media existing_media"),
        )
        self.assertEqual(2, sql.count(", FALSE) ON CONFLICT (id)"))

    def test_seller_uuid_is_stable_for_same_source_account(self):
        repost = deepcopy(self.property)
        repost["source_listing_id"] = 222222222
        repost["property_id"] = "P_222222222"

        self.assertEqual(
            generate_sql_from_json.deterministic_external_seller_uuid(self.property),
            generate_sql_from_json.deterministic_external_seller_uuid(repost),
        )


if __name__ == "__main__":
    unittest.main()
