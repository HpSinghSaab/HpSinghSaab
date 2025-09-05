"""
Example usage script for the Client Qualification & Scoping Engine (CQSE).

This script demonstrates the basic functionality of the lead scoring system
by qualifying a good-fit and a poor-fit lead against a sample
Ideal Client Profile (ICP).
"""
from src.cqse.models import IdealClientProfile, Lead
from src.cqse.scorer import score_lead


def main():
    """Main function to run the demonstration."""
    # 1. Define the Ideal Client Profile (ICP) for High-Value Construction
    # Based on the blueprint document (section 1.2.1)
    construction_icp = IdealClientProfile(
        vertical_name="High-Value Construction",
        pain_points_keywords=[
            "theft", "vandalism", "project delays",
            "budget overruns", "liability", "trespassing"
        ],
        decision_maker_titles=["Project Manager", "Site Superintendent", "Head of Security"],
        value_proposition_key="Project Continuity Insurance",
        strategic_narrative="Shift conversation from cost of security to cost of insecurity.",
    )

    # 2. Simulate incoming leads
    good_lead = Lead(
        company_name="SecureBuild Construction",
        industry="Construction",
        self_reported_need="We are having major issues with equipment theft and "
                           "trespassing at our new site, leading to costly project delays."
    )

    poor_lead = Lead(
        company_name="Corner Bodega",
        industry="Retail",
        self_reported_need="I need a simple alarm system for my small shop."
    )

    # 3. Score the leads against the ICP
    good_lead_score = score_lead(good_lead, construction_icp)
    poor_lead_score = score_lead(poor_lead, construction_icp)

    # 4. Print the results
    print("--- CQSE Lead Qualification Demo ---")
    print(f"\nScoring against ICP: '{construction_icp.vertical_name}'")
    print("-" * 35)

    print(f"\nLead 1: '{good_lead.company_name}'")
    print(f"Need: \"{good_lead.self_reported_need}\"")
    print(f"Qualification Score: {good_lead_score}")
    print("Assessment: Good Fit" if good_lead_score > 1 else "Assessment: Poor Fit")

    print("-" * 35)

    print(f"\nLead 2: '{poor_lead.company_name}'")
    print(f"Need: \"{poor_lead.self_reported_need}\"")
    print(f"Qualification Score: {poor_lead_score}")
    print("Assessment: Good Fit" if poor_lead_score > 1 else "Assessment: Poor Fit")
    print("\n--- End of Demo ---")


if __name__ == "__main__":
    main()
