"""
Pydantic data model for a Bin.
"""

# External Packages
from pydantic import BaseModel, Field


class Bin(BaseModel):
    """
    Pydantic data model for a Bin.
    """

    name: str = Field(description="Name/Type of the bin (e.g., General Waste)")
    """Name/Type of the bin (e.g., General Waste)."""

    colour: str = Field(description="Colour of the bin")
    """Colour of the bin."""