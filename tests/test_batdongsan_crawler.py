import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory


DATABASE_DIR = Path(__file__).resolve().parents[1] / "database"
sys.path.insert(0, str(DATABASE_DIR))

import crawler_batdongsan as crawler  # noqa: E402


SAMPLE_URL = (
    "https://batdongsan.com.vn/ban-dat-phuong-hung-thang-1/"
    "ban-o-goc-canh-nha-o-xa-hoi-bim-bai-chay-ha-long-gia-au-tu-pr46093955"
)


def complete_land_html() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta property="og:title" content="Bán ô góc cạnh nhà ở xã hội BIM Bãi Cháy, Hạ Long. Giá đầu tư.">
  <meta property="og:image" content="https://file4.batdongsan.com.vn/2026/07/25/cover_wm.jpg">
  <script type="application/ld+json">
    {"@context":"https://schema.org/","@type":"RealEstateListing",
     "@name":"Bán ô góc","@datePublished":"2026-07-25T10:50:59.0980000+07:00",
     "@dateModified":"2026-07-31T08:30:25.7650000+07:00"}
  </script>
  <script>
    window.pageTrackingData = { ...JSON.parse('{"products":[{"productId":46093955,
      "createByUser":4577230,"verified":true,"expired":false,"vipType":5,
      "productType":38}]}') };
  </script>
</head>
<body>
  <div class="re__pr-info js__product-detail-web" uid="4577230" prid="46093955">
    <h1 class="re__pr-title js__pr-title">Bán ô góc cạnh nhà ở xã hội BIM Bãi Cháy, Hạ Long. Giá đầu tư.</h1>
    <span class="re__address-line-1">Phường Hùng Thắng, Thành phố Hạ Long, Quảng Ninh</span>
    <span class="re__address-line-2">(Phường Bãi Cháy, Quảng Ninh mới)</span>
    <div class="re__pr-short-info-item js__pr-short-info-item">
      <span class="title">Khoảng giá</span><span class="value">4,8 tỷ</span>
      <span class="ext">~69 triệu/m²</span>
    </div>
    <div class="re__pr-short-info-item js__pr-short-info-item">
      <span class="title">Diện tích</span><span class="value">69,5 m²</span>
      <span class="ext">Mặt tiền 5 m</span>
    </div>
    <div class="re__section-body js__pr-description">
      Gia đình cần bán đất ô góc thuộc tái định cư Biên phòng Hùng Thắng.<br>
      Ngay cạnh khu nhà ở xã hội, thuận tiện kinh doanh và sang tên ngay.<br>
      Liên hệ trực tiếp: <span class="hidden-phone">0888 538 ***</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Khoảng giá</span>
      <span class="re__pr-specs-content-item-value">69 triệu/m²</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Diện tích</span>
      <span class="re__pr-specs-content-item-value">69,5 m²</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Hướng nhà</span>
      <span class="re__pr-specs-content-item-value">Tây - Nam</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Mặt tiền</span>
      <span class="re__pr-specs-content-item-value">5 m</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Đường vào</span>
      <span class="re__pr-specs-content-item-value">7,5 m</span>
    </div>
    <div class="re__pr-specs-content-item">
      <span class="re__pr-specs-content-item-title">Pháp lý</span>
      <span class="re__pr-specs-content-item-value">Sổ đỏ/ Sổ hồng</span>
    </div>
    <div class="re__contact-name" title="Nguyễn Hải Ninh">
      <a href="https://guru.batdongsan.com.vn/pa/nguyenhaininh">Nguyễn Hải Ninh</a>
    </div>
    <img class="re__contact-avatar" src="https://file4.batdongsan.com.vn/2026/01/09/avatar.jpg">
    <div>Môi giới chuyên nghiệp</div>
    <div class="agent-deail-infor"><span>Tham gia Batdongsan.com.vn</span><i>1 năm</i></div>
    <div class="agent-deail-infor"><span>Tin đăng đang có</span><i>8 tin</i></div>
    <div>Chat qua Zalo</div>
    <div><span class="title">Ngày đăng</span><span class="value">25/07/2026</span></div>
    <div><span class="title">Ngày hết hạn</span><span class="value">08/08/2026</span></div>
    <div><span class="title">Loại tin</span><span class="value">Tin thường</span></div>
    <div><span class="title">Mã tin</span><span class="value">46093955</span></div>
    <div class="js__pricing-history">26,6% Giá tại khu vực này đã tăng trong vòng 1 năm qua</div>
    <input class="js__pricing-history-count-of-years" value="1">
    <input class="js__encrypted-params" value="public-page-token">
  </div>
  <script>
    const mapConfig = { latitude: 20.963150536175743, longitude: 106.99359219639597 };
    const gallery = {"url":"https://file4.batdongsan.com.vn/2026/07/25/1_wm.jpg#~https://file4.batdongsan.com.vn/2026/07/25/2_wm.jpg#~https://file4.batdongsan.com.vn/2026/07/25/3_wm.jpg#~",
      "videos":[{"src":"https://vn1-cdn.pgimgs.com/listing/890788499/tour.mp4"}],"prid":46093955};
  </script>
</body>
</html>
"""


class ParsingTests(unittest.TestCase):
    def test_localized_numbers(self):
        self.assertEqual(4_800_000_000, crawler.parse_vnd("4,8 tỷ"))
        self.assertEqual(69_000_000, crawler.parse_vnd("69 triệu/m²"))
        self.assertEqual(69.5, crawler.parse_measurement("69,5 m²"))
        self.assertEqual(7.5, crawler.parse_measurement("7,5 m"))

    def test_combined_bathroom_label_is_recognized(self):
        self.assertEqual(
            "bathrooms",
            crawler.attribute_key("Số phòng tắm, vệ sinh"),
        )

    def test_tracking_query_is_removed(self):
        canonical = crawler.canonical_listing_url(SAMPLE_URL + "?gidzl=tracking")
        self.assertEqual(SAMPLE_URL, canonical)
        self.assertEqual("46093955", crawler.listing_id_from_url(canonical))

    def test_complete_land_page_is_normalized(self):
        record, issues = crawler.parse_listing_html(
            complete_land_html(),
            SAMPLE_URL + "?gidzl=tracking",
            crawled_at="2026-08-06T10:00:00Z",
        )

        self.assertEqual([], issues)
        self.assertIsNotNone(record)
        self.assertEqual("BDS_PR46093955", record["property_id"])
        self.assertEqual("LAND", record["property_kind"])
        self.assertEqual(4_800_000_000, record["price"])
        self.assertEqual(69.5, record["area_sqm"])
        self.assertEqual(5.0, record["frontage_m"])
        self.assertEqual(7.5, record["road_width_m"])
        self.assertEqual("Tây Nam", record["orientation"])
        self.assertEqual("Sổ đỏ/ Sổ hồng", record["legal_status"])
        self.assertEqual("Nguyễn Hải Ninh", record["seller"]["display_name"])
        self.assertEqual("0888 538 ***", record["seller"]["public_phone_masked"])
        self.assertEqual(8, record["seller"]["active_listing_count"])
        self.assertEqual(3, len(record["media"]))
        self.assertEqual(1, len(record["source_videos"]))
        self.assertEqual(26.6, record["market_insights"]["annual_change_percent"])
        self.assertFalse(record["market_insights"]["pricing_history_fetched"])
        self.assertEqual(
            "08/08/2026",
            record["source_listing_metadata"]["expires_text"],
        )
        self.assertEqual(
            "Tin thường",
            record["source_listing_metadata"]["listing_tier"],
        )
        self.assertEqual("2026-07-25T10:50:59.098000+07:00", record["published_at"])

    def test_page_id_must_match_url(self):
        html = complete_land_html().replace(
            '"productId":46093955', '"productId":99999999'
        ).replace('prid="46093955"', 'prid="99999999"')
        record, issues = crawler.parse_listing_html(
            html,
            SAMPLE_URL,
            crawled_at="2026-08-06T10:00:00Z",
        )
        self.assertIsNone(record)
        self.assertIn("source_listing_id_mismatch:99999999", issues)

    def test_explicit_villa_label_wins_over_combined_category_path(self):
        specs = crawler.blocks_by_label(
            [{"label": "Loại hình", "value": "Biệt thự", "extension": ""}]
        )
        self.assertEqual(
            "VILLA",
            crawler.extract_property_kind(
                "https://batdongsan.com.vn/ban-nha-biet-thu-lien-ke/"
                "biet-thu-hoan-chinh-pr12345678",
                specs,
            ),
        )

    def test_free_form_contact_is_redacted(self):
        html = complete_land_html().replace(
            "Liên hệ trực tiếp:", "Liên hệ 0912 345 678 hoặc owner@example.com:"
        )
        record, issues = crawler.parse_listing_html(
            html,
            SAMPLE_URL,
            crawled_at="2026-08-06T10:00:00Z",
        )
        self.assertEqual([], issues)
        self.assertNotIn("0912 345 678", record["description"])
        self.assertNotIn("owner@example.com", record["description"])
        self.assertEqual(2, record["privacy"]["free_text_contact_redactions"])

    def test_missing_land_road_width_is_rejected(self):
        html = complete_land_html().replace(
            '<span class="re__pr-specs-content-item-title">Đường vào</span>',
            '<span class="re__pr-specs-content-item-title">Chiều dài</span>',
        )
        record, issues = crawler.parse_listing_html(
            html,
            SAMPLE_URL,
            crawled_at="2026-08-06T10:00:00Z",
        )
        self.assertIsNone(record)
        self.assertIn("missing_land_road_width_m", issues)

    def test_cloudflare_challenge_is_not_parsed(self):
        with self.assertRaises(crawler.AccessBlocked):
            crawler.parse_listing_html(
                "<html><title>Just a moment...</title>Enable JavaScript and cookies to continue</html>",
                SAMPLE_URL,
                crawled_at="2026-08-06T10:00:00Z",
            )

    def test_category_links_are_deduplicated(self):
        category = "https://batdongsan.com.vn/ban-dat-ha-noi"
        html = (
            f'<a href="{SAMPLE_URL}">one</a>'
            f'<a href="{SAMPLE_URL}?tracking=x">duplicate</a>'
        )
        self.assertEqual([SAMPLE_URL], crawler.discover_listing_urls(html, category))


class SqlTests(unittest.TestCase):
    def setUp(self):
        self.record, issues = crawler.parse_listing_html(
            complete_land_html(),
            SAMPLE_URL,
            crawled_at="2026-08-06T10:00:00Z",
        )
        self.assertEqual([], issues)

    def test_sql_is_deterministic_and_safe_for_pgadmin(self):
        first = crawler.generate_sql([self.record])
        second = crawler.generate_sql([self.record])

        self.assertEqual(first, second)
        self.assertIn("BEGIN;", first)
        self.assertIn("COMMIT;", first)
        self.assertNotIn("\\set", first)
        self.assertIn("ON CONFLICT (code) DO UPDATE", first)
        self.assertIn("DELETE FROM property_media", first)
        self.assertIn("frontage_m", first)
        self.assertIn("road_width_m", first)
        self.assertIn("status = CASE WHEN properties.status", first)
        self.assertIn("INSERT INTO external_sellers", first)
        self.assertIn("INSERT INTO property_external_sellers", first)
        self.assertIn("INSERT INTO property_sale_assignments", first)
        self.assertIn("'LISTING_POSTER'", first)
        self.assertIn("AND source = 'BATDONGSAN_COM_VN'", first)
        self.assertNotIn(
            "WHERE property_id = (SELECT id FROM properties WHERE code = "
            "'BDS_PR46093955');",
            first,
        )
        self.assertNotIn("INSERT INTO users", first)
        self.assertNotIn("INSERT INTO sale_profiles", first)
        self.assertNotIn("INSERT INTO appointments", first)

    def test_exactly_one_cover_is_generated(self):
        sql = crawler.generate_sql([self.record])
        self.assertEqual(
            1,
            sql.count("NOT EXISTS (SELECT 1 FROM property_media existing_media"),
        )
        self.assertEqual(2, sql.count(", FALSE) ON CONFLICT (id)"))

    def test_database_bounds_are_validated_before_sql(self):
        self.record["frontage_m"] = 0
        with self.assertRaisesRegex(ValueError, "invalid_frontage_m"):
            crawler.generate_sql([self.record])

    def test_apartment_public_card_minimum_is_accepted(self):
        apartment = deepcopy(self.record)
        apartment["property_kind"] = "APARTMENT"
        apartment["bedrooms"] = 2
        apartment["bathrooms"] = 2
        apartment["floor_number"] = None
        apartment["furniture_status"] = None
        apartment["orientation"] = None
        apartment["balcony_orientation"] = None
        apartment["frontage_m"] = None
        apartment["road_width_m"] = None
        self.assertEqual([], crawler.listing_issues(apartment))

    def test_masked_seller_phone_is_required(self):
        self.record["seller"]["public_phone_masked"] = None
        self.assertIn(
            "missing_seller_public_phone_masked",
            crawler.listing_issues(self.record),
        )

        self.record["seller"]["public_phone_masked"] = "0901234567"
        self.assertIn(
            "seller_public_phone_not_masked",
            crawler.listing_issues(self.record),
        )

    def test_validated_checkpoint_can_be_resumed(self):
        with TemporaryDirectory() as temporary_dir:
            checkpoint = Path(temporary_dir) / "records.json"
            crawler.write_record_checkpoint(checkpoint, [self.record])
            loaded = crawler.load_record_checkpoint(checkpoint)
        self.assertEqual([self.record], loaded)

        resumed, rejected, removed = crawler.crawl(
            [],
            target=1,
            max_pages=1,
            timeout_seconds=1,
            retries=0,
            delay_seconds=2,
            jitter_seconds=0,
            initial_records=loaded,
        )
        self.assertEqual([self.record], resumed)
        self.assertFalse(rejected)
        self.assertEqual([], removed)

    def test_profile_fallback_seller_key_ignores_query_and_fragment(self):
        first = deepcopy(self.record)
        second = deepcopy(self.record)
        first["seller"]["source_account_id"] = None
        second["seller"]["source_account_id"] = None
        first["seller"]["profile_url"] = (
            "https://guru.batdongsan.com.vn/pa/nguyenhaininh?from=listing-a"
        )
        second["seller"]["profile_url"] = (
            "https://guru.batdongsan.com.vn/pa/nguyenhaininh?from=listing-b#contact"
        )

        first_key = crawler.external_seller_key(first)
        self.assertTrue(first_key.startswith("profile_sha256:"))
        self.assertEqual(first_key, crawler.external_seller_key(second))


if __name__ == "__main__":
    unittest.main()
