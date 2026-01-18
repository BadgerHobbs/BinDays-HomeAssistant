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

    website_url: Optional[str] = Field(default=None, alias="websiteUrl", description="Website URL")
    """Website URL."""

    gov_uk_url: Optional[str] = Field(default=None, alias="govUkUrl", description="Gov.uk URL")
    """Gov.uk URL."""