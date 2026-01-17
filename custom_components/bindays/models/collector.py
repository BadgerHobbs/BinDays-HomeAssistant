"""
Pydantic data model for a Collector.
"""

# External Packages
from typing import Optional
from pydantic import BaseModel, Field


class Collector(BaseModel):
    """
    Pydantic data model for a Collector.
    """

    gov_uk_id: str = Field(alias="govUkId", description="Government UK ID for the council")
    """Government UK ID for the council."""

    name: str = Field(description="Name of the council")
    """Name of the council."""

    key: Optional[str] = Field(default=None, description="Internal key")
    """Internal key."""

    url: Optional[str] = Field(default=None, description="Website URL")
    """Website URL."""