"""
Pydantic data model for ClientSideOptions.
"""

# External Packages
from pydantic import BaseModel, Field


class ClientSideOptions(BaseModel):
    """
    Pydantic data model for ClientSideOptions.
    """

    follow_redirects: bool = Field(True, alias="followRedirects", description="Whether to follow HTTP redirects")
    """Whether to follow HTTP redirects."""