"""
Pydantic data model for a ClientSideResponse.
"""

# External Packages
from typing import Dict, Any
from pydantic import BaseModel, Field

# Internal Packages
from .client_side_options import ClientSideOptions


class ClientSideResponse(BaseModel):
    """
    Pydantic data model for a ClientSideResponse.
    """

    request_id: int = Field(alias="requestId", description="ID of the original request")
    """ID of the original request."""

    status_code: int = Field(alias="statusCode", description="HTTP status code received")
    """HTTP status code received."""

    headers: Dict[str, str] = Field(default_factory=dict, description="Headers received (values flattened)")
    """Headers received (values flattened)."""

    content: str = Field(description="Response body content")
    """Response body content."""

    reason_phrase: str = Field("", alias="reasonPhrase", description="HTTP reason phrase")
    """HTTP reason phrase."""

    options: ClientSideOptions = Field(description="Original options used")
    """Original options used."""

    def to_api_payload(self) -> Dict[str, Any]:
        """
        Convert to the dictionary format expected by the API.
        """
        return self.model_dump(by_alias=True)