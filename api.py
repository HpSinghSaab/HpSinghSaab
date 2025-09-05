"""
API Server for the Client Qualification & Scoping Engine (CQSE).

This server provides an endpoint to score leads based on their alignment
with an Ideal Client Profile (ICP).
"""
from fastapi import FastAPI
from src.cqse.models import IdealClientProfile, Lead
from src.cqse.scorer import score_lead

# Initialize the FastAPI app
app = FastAPI(
    title="Client Qualification & Scoping Engine API",
    description="An API to score business leads against an Ideal Client Profile.",
    version="1.0.0",
)

# Define the Ideal Client Profile (ICP) for High-Value Construction
# In a real application, this would be loaded from a database or config file.
CONSTRUCTION_ICP = IdealClientProfile(
    vertical_name="High-Value Construction",
    pain_points_keywords=[
        "theft", "vandalism", "project delays",
        "budget overruns", "liability", "trespassing"
    ],
    decision_maker_titles=["Project Manager", "Site Superintendent", "Head of Security"],
    value_proposition_key="Project Continuity Insurance",
    strategic_narrative="Shift conversation from cost of security to cost of insecurity.",
)


@app.post("/score")
def score_lead_endpoint(lead: Lead):
    """
    Scores a single lead against the default Ideal Client Profile.

    This endpoint receives lead information, scores it using the CQSE's
    scoring logic, and returns the qualification score.

    - **lead**: A JSON object containing the lead's details.

    Returns:
    - A JSON response with the lead's qualification score.
    """
    score = score_lead(lead, CONSTRUCTION_ICP)
    return {"company_name": lead.company_name, "qualification_score": score}
