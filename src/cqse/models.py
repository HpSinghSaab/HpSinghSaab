"""
Data models for the Client Qualification & Scoping Engine (CQSE).

This module defines the Pydantic models that structure the data for:
- Ideal Client Profile (ICP): The criteria for a high-value client.
- Lead: An incoming prospect to be qualified.
"""
from typing import List, Optional

from pydantic import BaseModel


class ContractValueRange(BaseModel):
    """Represents a range for the estimated annual contract value."""
    min: int
    max: int


class IdealClientProfile(BaseModel):
    """
    Defines the structured data for an Ideal Client Profile (ICP).
    This model is derived from the blueprint in section 1.2.1.
    """
    vertical_name: str
    pain_points_keywords: List[str]
    decision_maker_titles: List[str]
    value_proposition_key: str
    est_annual_contract_value: Optional[ContractValueRange] = None
    strategic_narrative: str


class Lead(BaseModel):
    """Represents a new lead captured from a web form or other source."""
    company_name: str
    industry: str
    self_reported_need: str
