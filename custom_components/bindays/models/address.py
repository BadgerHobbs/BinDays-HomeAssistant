"""
Pydantic data model for an Address.
"""

# External Packages
from typing import Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    """
    Pydantic data model for an Address.
    """

    uid: str = Field(description="Unique identifier for the address")
    """Unique identifier for the address."""

    postcode: str = Field(description="Postal code of the address")
    """Postal code of the address."""

    property: Optional[str] = Field(default=None, description="Property number or name")
    """Property number or name."""

    street: Optional[str] = Field(default=None, description="Street name")
    """Street name."""

    town: Optional[str] = Field(default=None, description="Town or city name")
    """Town or city name."""

    def __str__(self) -> str:
        """
        Return a formatted string representation of the address.
        """
        parts = [
            self.property,
            self.street,
            self.town,
            self.postcode,
            self.uid,
        ]
        return ", ".join([part for part in parts if part and part.strip()])