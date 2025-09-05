"""
This module contains the lead scoring logic for the CQSE.
"""
from src.cqse.models import Lead, IdealClientProfile


def score_lead(lead: Lead, icp: IdealClientProfile) -> int:
    """
    Scores a lead based on its alignment with an Ideal Client Profile.

    This initial version calculates a score based on the number of
    pain point keywords found in the lead's self-reported need.

    Args:
        lead: The incoming lead to score.
        icp: The Ideal Client Profile to score against.

    Returns:
        An integer score representing the lead's qualification.
    """
    score = 0
    # Normalize the need to lowercase for case-insensitive matching
    normalized_need = lead.self_reported_need.lower()

    for keyword in icp.pain_points_keywords:
        if keyword.lower() in normalized_need:
            score += 1

    return score
