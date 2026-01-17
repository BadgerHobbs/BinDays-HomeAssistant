"""
Pydantic data model for a ClientSideRequest.
"""

# External Packages
from typing import Dict, Optional
from pydantic import BaseModel, Field

# Internal Packages
from .client_side_options import ClientSideOptions


class ClientSideRequest(BaseModel):
    """
    Pydantic data model for a ClientSideRequest.
    """

    request_id: str = Field(alias="requestId", description="Unique ID for this request")
    """Unique ID for this request."""

    url: str = Field(description="The URL to request")
    """The URL to request."""

    method: str = Field("GET", description="HTTP method (GET, POST, etc.)")
    """HTTP method (GET, POST, etc.)."""

    headers: Dict[str, str] = Field(default_factory=dict, description="HTTP headers to include")
    """HTTP headers to include."""

    body: Optional[str] = Field(default=None, description="Request body")
    """Request body."""

    options: ClientSideOptions = Field(default_factory=ClientSideOptions, description="Request options")
    """Request options."""