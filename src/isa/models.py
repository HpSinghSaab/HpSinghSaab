"""
Data models for the Integrated Solution Architect (ISA) module.

This module defines the Pydantic models that structure the data for:
- ServiceComponent: An individual item in the service catalog.
- SolutionComponent: A service item with a quantity for a proposal.
- SolutionBundle: A complete collection of services for a client proposal.
"""
from pydantic import BaseModel
from typing import List


class ServiceComponent(BaseModel):
    """Represents a single, available service or product in the catalog."""
    id: str
    name: str
    description: str
    price: float
    unit: str  # e.g., "per_hour", "per_month", "one_time"


class SolutionComponent(BaseModel):
    """Represents a service component included in a solution, with a specific quantity."""
    service: ServiceComponent
    quantity: int


class SolutionBundle(BaseModel):
    """Represents a complete solution proposal for a client."""
    name: str
    description: str
    components: List[SolutionComponent]

    @property
    def total_price(self) -> float:
        """
        Calculates the total price of the solution bundle.

        Note: This is a simplification. A real-world calculation would need to
        differentiate between recurring (e.g., monthly) and one-time costs.
        """
        total = 0.0
        for component in self.components:
            total += component.service.price * component.quantity
        return total
