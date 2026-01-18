"""
Pydantic data model for a BinDay.
"""

# External Packages
import datetime
from typing import List
from pydantic import BaseModel, Field

# Internal Packages
from .bin import Bin
from .address import Address


class BinDay(BaseModel):
    """
    Pydantic data model for a BinDay.
    """

    date_str: str = Field(alias="date", description="The date of collection as a string")
    """The date of collection as a string."""

    address: Address = Field(description="Address for the bin day")
    """Address for the bin day."""

    bins: List[Bin] = Field(default_factory=list, description="List of bins being collected")
    """List of bins being collected."""

    @property
    def parsed_date(self) -> datetime.date:
        """
        Return the parsed date object from the date string.
        """
        try:
            return datetime.datetime.fromisoformat(self.date_str.replace("Z", "+00:00")).date()
        except ValueError:
            return datetime.datetime.strptime(self.date_str, "%Y-%m-%d").date()