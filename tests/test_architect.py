import unittest
from src.cqse.models import Lead
from src.isa.architect import design_solution

class TestSolutionArchitect(unittest.TestCase):

    def test_construction_rule(self):
        """
        Test that a construction lead with 'theft' gets the correct package.
        """
        lead = Lead(
            company_name="Test Construction Co.",
            industry="Construction",
            self_reported_need="We have a big problem with theft on our site."
        )
        solution = design_solution(lead)
        self.assertEqual(solution.name, "Construction Site Security Package")
        self.assertEqual(len(solution.components), 3)
        # Check for a specific component to be extra sure
        self.assertTrue(any(c.service.id == 'camera_mobile_1' for c in solution.components))

    def test_data_center_rule(self):
        """
        Test that a data center lead with 'compliance' gets the correct package.
        """
        lead = Lead(
            company_name="Test Data Center Inc.",
            industry="Data Center",
            self_reported_need="We need to ensure PIPEDA compliance for physical access."
        )
        solution = design_solution(lead)
        self.assertEqual(solution.name, "Data Center Compliance & Access Control")
        self.assertEqual(len(solution.components), 2)
        self.assertTrue(any(c.service.id == 'access_biometric_1' for c in solution.components))

    def test_default_rule(self):
        """
        Test that a lead with no matching rules gets the default package.
        """
        lead = Lead(
            company_name="Test Logistics",
            industry="Logistics",
            self_reported_need="We need general security for our warehouse."
        )
        solution = design_solution(lead)
        self.assertEqual(solution.name, "Basic Security Patrol Package")
        self.assertEqual(len(solution.components), 1)
        self.assertEqual(solution.components[0].service.id, 'patrol_mobile_1')

    def test_construction_no_matching_keywords(self):
        """
        Test that a construction lead without matching keywords gets the default package.
        """
        lead = Lead(
            company_name="Test Construction Co.",
            industry="Construction",
            self_reported_need="We need to manage site access for our workers."
        )
        solution = design_solution(lead)
        self.assertEqual(solution.name, "Basic Security Patrol Package")

if __name__ == '__main__':
    unittest.main()
