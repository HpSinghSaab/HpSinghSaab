class CapitalGainsCalculator2025:
    """
    Calculates Capital Gains Tax based on Canadian 2025 rules
    (Effective June 25, 2024).
    """

    def __init__(self, marginal_tax_rate: float, entity_type: str = "Individual"):
        """
        :param marginal_tax_rate: The user's marginal tax rate (e.g., 0.53).
        :param entity_type: 'Individual' or 'Corporation'.
        """
        self.marginal_tax_rate = marginal_tax_rate
        self.entity_type = entity_type

    def calculate_tax(self, total_gain: float) -> dict:
        """
        Calculate the tax liability.

        Rules:
        - Individuals: 50% inclusion on first $250k, 66.67% on remainder.
        - Corporations: 66.67% inclusion on ALL gains.
        """
        inclusion_rate_tier1 = 0.50
        inclusion_rate_tier2 = 2/3  # 0.6666...
        tier1_limit = 250000.0

        taxable_capital_gain = 0.0

        if self.entity_type.lower() == "corporation":
            # Corporations do not get the $250k tier
            taxable_capital_gain = total_gain * inclusion_rate_tier2
            details = f"100% of gain @ {inclusion_rate_tier2:.2%} inclusion"
        else:
            # Individual
            if total_gain <= tier1_limit:
                taxable_capital_gain = total_gain * inclusion_rate_tier1
                details = f"100% of gain @ {inclusion_rate_tier1:.0%} inclusion"
            else:
                gain_tier1 = tier1_limit
                gain_tier2 = total_gain - tier1_limit

                taxable_part1 = gain_tier1 * inclusion_rate_tier1
                taxable_part2 = gain_tier2 * inclusion_rate_tier2

                taxable_capital_gain = taxable_part1 + taxable_part2
                details = (f"First ${tier1_limit:,.0f} @ {inclusion_rate_tier1:.0%} inclusion, "
                           f"Remaining ${gain_tier2:,.2f} @ {inclusion_rate_tier2:.2%} inclusion")

        tax_payable = taxable_capital_gain * self.marginal_tax_rate
        effective_rate = tax_payable / total_gain if total_gain > 0 else 0

        return {
            "total_gain": total_gain,
            "taxable_capital_gain": taxable_capital_gain,
            "tax_payable": tax_payable,
            "effective_tax_rate": effective_rate,
            "details": details
        }
