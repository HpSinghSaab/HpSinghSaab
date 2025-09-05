"""
Example usage script for the AI-Powered Operational Intelligence Suite.

This script demonstrates the end-to-end workflow of:
1. Qualifying a lead using the Client Qualification & Scoping Engine (CQSE).
2. Designing a solution for the qualified lead using the Integrated Solution
   Architect (ISA).
"""
from src.cqse.models import IdealClientProfile, Lead
from src.cqse.scorer import score_lead
from src.isa.architect import design_solution

def main():
    """Main function to run the demonstration."""
    print("--- AI-Powered Operational Intelligence Suite Demo ---")

    # --- Define ICP and Leads ---
    construction_icp = IdealClientProfile(
        vertical_name="High-Value Construction",
        pain_points_keywords=[
            "theft", "vandalism", "project delays",
            "budget overruns", "liability", "trespassing"
        ],
        decision_maker_titles=["Project Manager", "Site Superintendent"],
        value_proposition_key="Project Continuity Insurance",
        strategic_narrative="Shift conversation from cost of security to cost of insecurity.",
    )

    construction_lead = Lead(
        company_name="SecureBuild Construction",
        industry="Construction",
        self_reported_need="We are having major issues with equipment theft and "
                           "vandalism at our new site, leading to costly project delays."
    )

    retail_lead = Lead(
        company_name="Corner Bodega",
        industry="Retail",
        self_reported_need="I need a simple alarm system for my small shop."
    )

    leads_to_process = [construction_lead, retail_lead]

    for i, lead in enumerate(leads_to_process):
        print(f"\n----- Processing Lead {i+1}: {lead.company_name} -----")

        # --- Stage 1: Client Qualification (CQSE) ---
        print("\n[Stage 1: CQSE] Qualifying lead...")
        score = score_lead(lead, construction_icp)
        print(f"Qualification Score: {score}")

        # Define a qualification threshold
        qualification_threshold = 2

        if score >= qualification_threshold:
            print("Assessment: Lead is QUALIFIED.")

            # --- Stage 2: Solution Design (ISA) ---
            print("\n[Stage 2: ISA] Designing solution...")
            solution = design_solution(lead)
            print(f"Recommended Solution: '{solution.name}'")
            print(f"Description: {solution.description}")
            print("\nItemized Proposal:")
            print("-" * 30)
            for component in solution.components:
                print(f"  - {component.service.name} (x{component.quantity})")
                print(f"    '{component.service.description}'")
                print(f"    Price: ${component.service.price:.2f} / {component.service.unit}")
            print("-" * 30)
            # A real proposal would distinguish recurring vs one-time costs
            print(f"Estimated Total: ${solution.total_price:.2f}")

        else:
            print("Assessment: Lead is NOT QUALIFIED. Halting process.")

    print("\n--- End of Demo ---")


if __name__ == "__main__":
    main()
