import unittest
from src.cqse.models import IdealClientProfile, Lead
from src.cqse.scorer import score_lead

class TestLeadScorer(unittest.TestCase):

    def setUp(self):
        """Set up a sample ICP for all tests."""
        self.construction_icp = IdealClientProfile(
            vertical_name="High-Value Construction",
            pain_points_keywords=["theft", "vandalism", "project delays", "liability"],
            decision_maker_titles=[],
            value_proposition_key="",
            strategic_narrative="",
        )

    def test_good_match(self):
        """Test a lead that is a good match for the ICP."""
        lead = Lead(
            company_name="SiteSecure",
            industry="Construction",
            self_reported_need="We are experiencing significant theft of materials, which is causing project delays."
        )
        # Expects to match "theft" and "project delays"
        self.assertEqual(score_lead(lead, self.construction_icp), 2)

    def test_partial_match(self):
        """Test a lead that is a partial match for the ICP."""
        lead = Lead(
            company_name="BuildItFast",
            industry="Construction",
            self_reported_need="Our main concern is liability on the job site."
        )
        # Expects to match "liability"
        self.assertEqual(score_lead(lead, self.construction_icp), 1)

    def test_no_match(self):
        """Test a lead that is a poor match for the ICP."""
        lead = Lead(
            company_name="CoffeeShop",
            industry="Food & Beverage",
            self_reported_need="I need a new point-of-sale system."
        )
        self.assertEqual(score_lead(lead, self.construction_icp), 0)

    def test_case_insensitivity(self):
        """Test that keyword matching is case-insensitive."""
        lead = Lead(
            company_name="UpperCase Inc.",
            industry="Construction",
            self_reported_need="THEFT and VANDALISM are our biggest problems."
        )
        # Expects to match "THEFT" and "VANDALISM"
        self.assertEqual(score_lead(lead, self.construction_icp), 2)

    def test_empty_need(self):
        """Test a lead with an empty self-reported need."""
        lead = Lead(
            company_name="Silent Builders",
            industry="Construction",
            self_reported_need=""
        )
        self.assertEqual(score_lead(lead, self.construction_icp), 0)

if __name__ == '__main__':
    unittest.main()
