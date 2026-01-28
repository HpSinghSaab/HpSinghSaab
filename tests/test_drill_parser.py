import unittest
from src.geology.drill_parser import DrillParser

class TestDrillParser(unittest.TestCase):

    def setUp(self):
        self.parser = DrillParser()

    def test_extract_pattern1(self):
        text = "10.5m @ 5.0 g/t Au"
        results = self.parser.parse_text(text)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['raw_grade'], 5.0)

    def test_extract_pattern2(self):
        text = "5.0 g/t Au over 10.5m"
        results = self.parser.parse_text(text)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['raw_grade'], 5.0)
        self.assertEqual(results[0]['raw_interval'], 10.5)

    def test_decimal_without_leading_zero(self):
        text = ".5m @ .9 g/t Au"
        results = self.parser.parse_text(text)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['raw_interval'], 0.5)
        self.assertEqual(results[0]['raw_grade'], 0.9)

    def test_metal_content_filtering(self):
        results = [
            {'element': 'Au', 'grade_unit': 'g/t', 'normalized_interval_m': 10.0, 'raw_grade': 2.0},
            {'element': 'Ag', 'grade_unit': 'g/t', 'normalized_interval_m': 5.0, 'raw_grade': 10.0}
        ]
        score_au = self.parser.calculate_metal_content(results, target_element="Au")
        score_ag = self.parser.calculate_metal_content(results, target_element="Ag")

        self.assertEqual(score_au, 20.0)
        self.assertEqual(score_ag, 50.0)

if __name__ == '__main__':
    unittest.main()
