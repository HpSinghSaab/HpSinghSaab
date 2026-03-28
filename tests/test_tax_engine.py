import unittest
from src.tax_engine.flow_through_calc import FlowThroughCalculator

class TestFlowThroughCalculator(unittest.TestCase):

    def test_basic_calculation_ontario(self):
        calc = FlowThroughCalculator(marginal_tax_rate=0.50, province="ON")
        res = calc.calculate_breakeven(share_price=1.00, investment_amount=100.0)
        self.assertAlmostEqual(res['net_out_of_pocket'], 30.0)

    def test_case_insensitive_province(self):
        calc = FlowThroughCalculator(marginal_tax_rate=0.50, province="on")
        res = calc.calculate_breakeven(share_price=1.00, investment_amount=100.0)
        # Should match the ON credit of 5% -> total credit 20% -> savings 70% -> cost 30%
        self.assertAlmostEqual(res['net_out_of_pocket'], 30.0)

if __name__ == '__main__':
    unittest.main()
