"""
Pydantic data model for a Bin.
"""

# External Packages
from typing import List, Optional
from pydantic import BaseModel, Field


class Bin(BaseModel):
    """
    Pydantic data model for a Bin.
    """

    name: str = Field(description="Name/Type of the bin (e.g., General Waste)")
    """Name/Type of the bin (e.g., General Waste)."""

    colour: str = Field(description="Colour of the bin")
    """Colour of the bin."""

    type: Optional[str] = Field(default=None, description="Type of the bin")
    """Type of the bin."""

    keys: List[str] = Field(default_factory=list, description="Identifiers for the bin")
    """Identifiers for the bin."""