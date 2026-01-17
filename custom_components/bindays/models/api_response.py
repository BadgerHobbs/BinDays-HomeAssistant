"""
Pydantic data model for API response.
"""

# External Packages
from typing import Any, Optional
from pydantic import BaseModel

# Internal Packages
from .client_side_request import ClientSideRequest


class ApiResponse(BaseModel):
    """
    Pydantic data model for API response.
    """

    data: Any
    """The data returned by the API."""

    next_client_side_request: Optional[ClientSideRequest] = None
    """The next client-side request to perform."""
