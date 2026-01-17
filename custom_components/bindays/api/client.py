"""
BinDays API Client.
"""

# External Packages
import logging
from typing import Any, Dict, List, Optional, TypeVar, Callable
import aiohttp
from pydantic import ValidationError

# Internal Packages
from ..const import DEFAULT_API_URL
from ..models.collector import Collector
from ..models.address import Address
from ..models.bin_day import BinDay
from ..models.client_side_request import ClientSideRequest
from ..models.client_side_response import ClientSideResponse
from .error import BinDaysApiClientError

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


class BinDaysApiClient:
    """
    A client for interacting with the BinDays API.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str = DEFAULT_API_URL,
    ):
        """
        Initialise BinDays API client.
        """
        self._session = session
        self._base_url = base_url.rstrip("/")

    async def get_collectors(self) -> List[Collector]:
        """
        Retrieves a list of all Collectors.
        """
        url = f"{self._base_url}/collectors"

        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return [Collector(**c) for c in data]
        except aiohttp.ClientError as e:
            _LOGGER.error("Failed to fetch collectors: %s", e)
            raise BinDaysApiClientError(f"Network error fetching collectors: {e}") from e
        except ValidationError as e:
            _LOGGER.error("Failed to parse collectors: %s", e)
            raise BinDaysApiClientError(
                f"Data validation error for collectors: {e}"
            ) from e

    async def get_collector(self, postcode: str) -> Collector:
        """
        Retrieves a Collector for a given postcode.
        """
        url = f"{self._base_url}/collector"

        return await self._fetch_data(
            url=url,
            params={"postcode": postcode},
            data_extractor=lambda json: Collector(**json["collector"])
            if json.get("collector")
            else None,
            error_message=f"No collector found for postcode '{postcode}'.",
        )

    async def get_addresses(self, collector: Collector, postcode: str) -> List[Address]:
        """
        Retrieves a list of Address for a given postcode.
        """
        url = f"{self._base_url}/{collector.gov_uk_id}/addresses"

        return await self._fetch_data(
            url=url,
            params={"postcode": postcode},
            data_extractor=lambda json: [Address(**a) for a in json["addresses"]]
            if json.get("addresses")
            else None,
            error_message=f"No addresses found for postcode '{postcode}'.",
        )

    async def get_bin_days(self, collector: Collector, address: Address) -> List[BinDay]:
        """
        Retrieves a list of BinDay for a given Collector and Address.
        """
        url = f"{self._base_url}/{collector.gov_uk_id}/bin-days"

        # For verbose error message
        address_string = str(address)

        return await self._fetch_data(
            url=url,
            params={"postcode": address.postcode, "uid": address.uid},
            data_extractor=lambda json: [BinDay(**b) for b in json["binDays"]]
            if json.get("binDays")
            else None,
            error_message=f"No bin days found for collector '{collector.name}' and address '{address_string}'.",
        )

    async def _fetch_data(
        self,
        url: str,
        params: Dict[str, str],
        data_extractor: Callable[[Dict[str, Any]], Optional[T]],
        error_message: str,
    ) -> T:
        """
        Generic function to fetch data from the API, handling multi-step requests.
        """
        client_side_response: Optional[ClientSideResponse] = None

        while True:
            # Prepare body for the main API request.
            request_body = None
            if client_side_response:
                request_body = client_side_response.to_api_payload()

            try:
                # Make the main POST request to our API endpoint
                async with self._session.post(
                    url,
                    params=params,
                    json=request_body,
                    headers={"Content-Type": "application/json"},
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
            except aiohttp.ClientError as e:
                _LOGGER.error("API request failed: %s", e)
                raise BinDaysApiClientError(f"API request failed: {e}") from e

            # Try to extract the final data
            try:
                extracted_data = data_extractor(data)
                if extracted_data is not None:
                    return extracted_data
            except ValidationError as e:
                _LOGGER.error("Data validation error: %s", e)
                raise BinDaysApiClientError(f"Failed to parse response: {e}") from e

            # If no data, check if there's a next step
            next_request_data = data.get("nextClientSideRequest")
            if next_request_data:
                try:
                    next_request = ClientSideRequest(**next_request_data)
                    # Perform the client-side request required by the API
                    client_side_response = await self._send_client_side_request(
                        next_request
                    )
                    # Continue the loop
                except ValidationError as e:
                    _LOGGER.error("Failed to parse next client side request: %s", e)
                    raise BinDaysApiClientError(
                        f"Invalid client side request received: {e}"
                    ) from e
            else:
                _LOGGER.warning(
                    "API returned neither data nor next instruction. URL: %s", url
                )
                raise BinDaysApiClientError(error_message)

    async def _send_client_side_request(
        self, request: ClientSideRequest
    ) -> ClientSideResponse:
        """
        Sends a client-side request as instructed by the main API.
        """
        _LOGGER.debug(
            "Executing client-side request: %s %s", request.method, request.url
        )

        try:
            async with self._session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.body,
                allow_redirects=request.options.follow_redirects,
            ) as response:

                content = await response.text()

                # Flatten headers
                headers_dict = {}
                for k, v in response.headers.items():
                    if k in headers_dict:
                        headers_dict[k] = f"{headers_dict[k]},{v}"
                    else:
                        headers_dict[k] = v

                return ClientSideResponse(
                    requestId=request.request_id,
                    statusCode=response.status,
                    headers=headers_dict,
                    content=content,
                    reasonPhrase=response.reason if response.reason else "",
                    options=request.options,
                )

        except Exception as e:
            _LOGGER.error("Client side request execution failed: %s", e)
            raise BinDaysApiClientError(f"Client side request failed: {e}") from e