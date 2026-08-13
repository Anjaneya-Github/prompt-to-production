"""
Unit and Integration Tests for UC-0A Complaint Classifier
"""
import os
import csv
import unittest
from classifier import classify_complaint, batch_classify, ALLOWED_CATEGORIES, SEVERITY_KEYWORDS


class TestComplaintClassifier(unittest.TestCase):

    def test_severity_keyword_triggers_urgent(self):
        sample_row = {
            "complaint_id": "TEST-01",
            "description": "Deep pothole near bus stop. School children at risk."
        }
        res = classify_complaint(sample_row)
        self.assertEqual(res["category"], "Pothole")
        self.assertEqual(res["priority"], "Urgent")
        self.assertIn("school", res["reason"].lower())
        self.assertIn("child", res["reason"].lower())

    def test_allowed_categories_only(self):
        descriptions = [
            "Tarmac surface melting at 44°C. Footwear sticking.",
            "Water leakage in main stormwater drain blocked.",
            "Wedding venue playing music past midnight on weeknights.",
            "Old city road subsidence near ancient step well.",
            "Overflowing garbage bins near market."
        ]
        for desc in descriptions:
            res = classify_complaint({"description": desc})
            self.assertIn(res["category"], ALLOWED_CATEGORIES, f"Category '{res['category']}' not in allowed list!")

    def test_empty_description_flags_needs_review(self):
        res = classify_complaint({"description": ""})
        self.assertEqual(res["category"], "Other")
        self.assertEqual(res["priority"], "Low")
        self.assertEqual(res["flag"], "NEEDS_REVIEW")

    def test_batch_classify_integration(self):
        input_csv = "../data/city-test-files/test_pune.csv"
        output_csv = "results_pune.csv"
        batch_classify(input_csv, output_csv)
        self.assertTrue(os.path.exists(output_csv))

        with open(output_csv, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 15, "Expected 15 rows in test_pune.csv")
            for row in reader:
                self.assertIn(row["category"], ALLOWED_CATEGORIES)
                self.assertIn(row["priority"], ["Urgent", "Standard", "Low"])
                self.assertTrue(len(row["reason"]) > 0, "Reason must not be empty")


if __name__ == "__main__":
    unittest.main()
