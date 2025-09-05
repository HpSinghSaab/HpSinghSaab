"""
This module contains the core logic for the Integrated Solution Architect (ISA).
It defines the service catalog and the rule-based engine for designing
solutions.
"""
from typing import List
from src.cqse.models import Lead
from src.isa.models import ServiceComponent, SolutionComponent, SolutionBundle

# 1. The Service Catalog
# A list of all available services the company can offer.
SERVICE_CATALOG = [
    ServiceComponent(
        id="guard_static_1",
        name="Static Guard",
        description="A trained security guard stationed at a fixed post.",
        price=75.0,
        unit="per_hour"
    ),
    ServiceComponent(
        id="patrol_mobile_1",
        name="Mobile Patrol",
        description="A security patrol that visits the site at random intervals.",
        price=50.0,
        unit="per_visit"
    ),
    ServiceComponent(
        id="camera_mobile_1",
        name="Mobile Security Unit",
        description="A trailer-mounted camera with remote monitoring.",
        price=2500.0,
        unit="per_month"
    ),
    ServiceComponent(
        id="access_biometric_1",
        name="Biometric Access Control",
        description="Multi-factor biometric access control for sensitive entry points.",
        price=150.0,
        unit="per_door_per_month"
    ),
]

# Helper to find a service by its ID
def _get_service(service_id: str) -> ServiceComponent:
    for service in SERVICE_CATALOG:
        if service.id == service_id:
            return service
    raise ValueError(f"Service with ID '{service_id}' not found in catalog.")


# 2. The Rule-Based Engine
def design_solution(lead: Lead) -> SolutionBundle:
    """
    Designs a security solution based on the lead's vertical and needs.

    This function acts as a rule-based engine, matching lead characteristics
    to a predefined solution bundle.

    Args:
        lead: The qualified lead object from the CQSE module.

    Returns:
        A SolutionBundle containing the recommended services.
    """
    # Normalize needs for keyword searching
    needs = lead.self_reported_need.lower()
    industry = lead.industry.lower()

    # Rule for High-Value Construction (as per blueprint example)
    if "construction" in industry and ("theft" in needs or "vandalism" in needs):
        return SolutionBundle(
            name="Construction Site Security Package",
            description="A comprehensive solution to protect against theft and vandalism, ensuring project continuity.",
            components=[
                SolutionComponent(service=_get_service("guard_static_1"), quantity=1),
                SolutionComponent(service=_get_service("patrol_mobile_1"), quantity=2),
                SolutionComponent(service=_get_service("camera_mobile_1"), quantity=4),
            ]
        )

    # Rule for Data Centers (as per blueprint example)
    if "data center" in industry and ("compliance" in needs or "access" in needs):
        return SolutionBundle(
            name="Data Center Compliance & Access Control",
            description="A high-compliance solution for physical access control and auditable logging.",
            components=[
                SolutionComponent(service=_get_service("access_biometric_1"), quantity=8),
                SolutionComponent(service=_get_service("guard_static_1"), quantity=1),
            ]
        )

    # Default/Fallback Solution for other qualified leads
    return SolutionBundle(
        name="Basic Security Patrol Package",
        description="A standard package for general deterrence and presence.",
        components=[
            SolutionComponent(service=_get_service("patrol_mobile_1"), quantity=4)
        ]
    )
