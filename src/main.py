import sys
from src.tax_engine.flow_through_calc import FlowThroughCalculator
from src.tax_engine.capital_gains import CapitalGainsCalculator2025
from src.geology.drill_parser import DrillParser

def run_cap_gains_calc():
    print("\n--- 2025 Capital Gains Tax Estimator ---")
    try:
        gain = float(input("Enter Total Capital Gain ($): ") or "0")
        tax_rate = float(input("Enter Marginal Tax Rate (0.00-1.00): ") or "0.50")
        entity = input("Entity Type (Individual/Corporation) [Individual]: ") or "Individual"

        calc = CapitalGainsCalculator2025(marginal_tax_rate=tax_rate, entity_type=entity)
        res = calc.calculate_tax(gain)

        print("\n--- Results ---")
        print(f"Total Gain: ${res['total_gain']:,.2f}")
        print(f"Taxable Capital Gain: ${res['taxable_capital_gain']:,.2f}")
        print(f"Tax Payable: ${res['tax_payable']:,.2f}")
        print(f"Effective Tax Rate: {res['effective_tax_rate']:.2%}")
        print(f"Details: {res['details']}")

    except ValueError:
        print("Invalid input.")

def run_tax_calc():
    print("\n--- Flow-Through Share Calculator ---")
    try:
        price = float(input("Enter Share Price ($): ") or "1.00")
        investment = float(input("Enter Investment Amount ($): ") or "10000")
        tax_rate = float(input("Enter Marginal Tax Rate (0.00-1.00): ") or "0.50")
        province = input("Enter Province (ON, BC, QC, AB): ") or "ON"

        calc = FlowThroughCalculator(marginal_tax_rate=tax_rate, province=province)
        result = calc.calculate_breakeven(share_price=price, investment_amount=investment)

        print("\n--- Results ---")
        print(f"Original Share Price: ${result['original_share_price']:.2f}")
        print(f"Net Out-of-Pocket Cost: ${result['net_out_of_pocket']:.2f} (Savings: ${result['deduction_savings'] + result['credit_savings']:.2f})")
        print(f"Effective Cost Base: ${result['effective_cost_per_share']:.2f}")
        print(f"True Breakeven Price (Exit Tax Included): ${result['breakeven_price']:.2f}")

    except ValueError:
        print("Invalid input. Please enter numbers.")

def run_drill_parser():
    print("\n--- Drill Result Interpreter (Prototype) ---")
    print("Paste a simulated press release snippet.")

    text = input("\nEnter text: ")
    if not text:
        text = "Company X intersects 15.5m @ 12.5 g/t Au and 5.0 g/t Au over 10m"
        print(f"Using default: {text}")

    parser = DrillParser()
    results = parser.parse_text(text)

    if not results:
        print("No drill results found.")
    else:
        print("\n--- Extracted Data ---")
        for i, res in enumerate(results):
            print(f"Intercept {i+1}: {res['formatted']}")

    gram_meters = parser.calculate_metal_content(results, target_element="Au")
    print(f"\nTotal Gram-Meters (Au only): {gram_meters}")

def main():
    while True:
        print("\nSelect Tool:")
        print("1. Flow-Through Tax Calculator")
        print("2. Drill Result Parser")
        print("3. 2025 Capital Gains Estimator")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1': run_tax_calc()
        elif choice == '2': run_drill_parser()
        elif choice == '3': run_cap_gains_calc()
        elif choice == '4': sys.exit(0)

if __name__ == "__main__":
    main()
