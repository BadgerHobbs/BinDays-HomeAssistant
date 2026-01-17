"""
API Client Error.
"""

from typing import Optional


class BinDaysApiClientError(Exception):
    """
    Exception to indicate a general API error.
    """

    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        data: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.data = data
