from typing import Dict, Optional

class FlowThroughCalculator:
    """
    Calculates the effective breakeven price for Flow-Through Shares (FTS)
    based on the investor's marginal tax rate and applicable tax credits.
    """

    def __init__(self, marginal_tax_rate: float, province: str = "ON"):
        """
        Initialize the calculator.

        :param marginal_tax_rate: The investor's marginal tax rate (e.g., 0.53 for 53%).
        :param province: The province for specific tax credits (default: Ontario).
        """
        self.marginal_tax_rate = marginal_tax_rate
        self.province = province.upper().strip()

        # Simplified map of provincial Mineral Exploration Tax Credits (METC)
        self.provincial_credits = {
            "ON": 0.05,  # Ontario Focused Flow-Through Share Tax Credit
            "BC": 0.20,  # BC Mining Flow-Through Share Tax Credit
            "QC": 0.0,   # Quebec has a complex deduction system, treating as 0 for simple prototype
            "AB": 0.0    # Alberta
        }

        self.federal_metc = 0.15 # 15% Federal Mineral Exploration Tax Credit

    def calculate_breakeven(self, share_price: float, investment_amount: float = 10000.0,
                            eligible_for_metc: bool = True) -> Dict[str, float]:
        """
        Calculate the effective cost and breakeven price.

        :param share_price: The price per share of the flow-through offering.
        :param investment_amount: Total amount invested.
        :param eligible_for_metc: Whether the financing qualifies for the 15% Federal METC.
        :return: Dictionary containing breakdown of savings and breakeven price.
        """
        deduction_savings = investment_amount * self.marginal_tax_rate

        credits = 0.0
        if eligible_for_metc:
            credits += self.federal_metc

        credits += self.provincial_credits.get(self.province, 0.0)

        credit_savings = investment_amount * credits

        total_tax_savings = deduction_savings + credit_savings
        net_cost = investment_amount - total_tax_savings

        effective_cost_per_share = (net_cost / investment_amount) * share_price

        cap_gains_inclusion = 0.5
        cap_gains_tax_rate = self.marginal_tax_rate * cap_gains_inclusion

        breakeven_price = effective_cost_per_share / (1 - cap_gains_tax_rate)

        return {
            "original_share_price": share_price,
            "investment_amount": investment_amount,
            "deduction_savings": deduction_savings,
            "credit_savings": credit_savings,
            "net_out_of_pocket": net_cost,
            "effective_cost_per_share": effective_cost_per_share,
            "breakeven_price": breakeven_price,
            "hard_breakeven_price_no_exit_tax": effective_cost_per_share
        }
