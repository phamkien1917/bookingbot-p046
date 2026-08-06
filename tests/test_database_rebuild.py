import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "database"


class DatabaseRebuildTests(unittest.TestCase):
    def test_main_sql_files_are_pgadmin_compatible(self):
        for name in (
            "001_schema.sql",
            "002_seed.sql",
            "003_smoke_test.sql",
            "004_crawled_data.sql",
            "005_batdongsan_data.sql",
        ):
            text = (DATABASE / name).read_text(encoding="utf-8")
            meta_lines = [
                line for line in text.splitlines() if line.lstrip().startswith("\\")
            ]
            self.assertEqual([], meta_lines, f"{name} contains psql meta commands")
            self.assertIsNone(
                re.search(r"\bCOPY\b.+\bFROM\s+STDIN\b", text, re.IGNORECASE),
                f"{name} requires psql COPY input",
            )

    def test_schema_contains_exact_18_mvp_tables(self):
        schema = (DATABASE / "001_schema.sql").read_text(encoding="utf-8")
        actual_tables = set(
            re.findall(r"(?m)^CREATE TABLE\s+([a-z_]+)\s*\(", schema)
        )
        expected_tables = {
            "users",
            "customer_profiles",
            "sale_profiles",
            "projects",
            "properties",
            "external_sellers",
            "property_external_sellers",
            "property_media",
            "property_sale_assignments",
            "sale_unavailability",
            "conversations",
            "messages",
            "tour_requests",
            "tour_slot_options",
            "approval_requests",
            "appointments",
            "property_holds",
            "notifications",
        }
        self.assertSetEqual(expected_tables, actual_tables)
        self.assertIn("source VARCHAR(40) NOT NULL DEFAULT 'INTERNAL'", schema)
        self.assertIn("uq_property_primary_external_seller", schema)

    def test_seed_has_expected_login_roles_and_profiles(self):
        seed = (DATABASE / "002_seed.sql").read_text(encoding="utf-8")
        self.assertEqual(5, seed.count("'CUSTOMER',"))
        self.assertEqual(3, seed.count("'SALE',"))
        self.assertEqual(1, seed.count("'COORDINATOR',"))
        self.assertEqual(1, seed.count("'ADMIN',"))
        self.assertEqual(5, seed.count("'CUS-DEMO-"))
        self.assertEqual(3, seed.count("'SALE-00"))
        for sale_id in (
            "10000000-0000-0000-0000-000000000002",
            "10000000-0000-0000-0000-000000000008",
            "10000000-0000-0000-0000-000000000009",
        ):
            self.assertIn(sale_id, seed)

    def test_generated_inventory_sql_has_expected_relational_rows(self):
        nhatot_sql = (DATABASE / "004_crawled_data.sql").read_text(encoding="utf-8")
        self.assertEqual(
            (108, 108, 108, 108, 750),
            (
                nhatot_sql.count("INSERT INTO properties"),
                nhatot_sql.count("INSERT INTO external_sellers"),
                nhatot_sql.count("INSERT INTO property_external_sellers"),
                nhatot_sql.count("INSERT INTO property_sale_assignments"),
                nhatot_sql.count("INSERT INTO property_media"),
            ),
        )

        records = json.loads(
            (DATABASE / "batdongsan_records.json").read_text(encoding="utf-8")
        )
        report = json.loads(
            (DATABASE / "batdongsan_crawl_report.json").read_text(encoding="utf-8")
        )
        batdongsan_sql = (DATABASE / "005_batdongsan_data.sql").read_text(
            encoding="utf-8"
        )
        media_count = sum(len(record["media"]) for record in records)
        self.assertEqual(60, len(records))
        self.assertEqual(60, report["accepted_count"])
        self.assertEqual(58, report["unique_seller_count"])
        self.assertEqual(612, media_count)
        self.assertGreaterEqual(report["minimum_images_per_property"], 3)
        self.assertTrue(report["all_have_masked_seller_phone"])
        self.assertTrue(report["all_have_legal_status"])
        self.assertTrue(report["all_have_coordinates"])
        self.assertEqual(
            (60, 60, 60, 60, 612),
            (
                batdongsan_sql.count("INSERT INTO properties"),
                batdongsan_sql.count("INSERT INTO external_sellers"),
                batdongsan_sql.count("INSERT INTO property_external_sellers"),
                batdongsan_sql.count("INSERT INTO property_sale_assignments"),
                batdongsan_sql.count("INSERT INTO property_media"),
            ),
        )
        self.assertNotIn("INSERT INTO users", nhatot_sql)
        self.assertNotIn("INSERT INTO users", batdongsan_sql)

    def test_nha_tot_input_has_98_unique_external_sellers(self):
        rows = json.loads(
            (DATABASE / "properties.json").read_text(encoding="utf-8")
        )
        seller_keys = {
            (str(row["source"]), str(row["seller_account_id"])) for row in rows
        }
        self.assertEqual(108, len(rows))
        self.assertEqual(98, len(seller_keys))


if __name__ == "__main__":
    unittest.main()
