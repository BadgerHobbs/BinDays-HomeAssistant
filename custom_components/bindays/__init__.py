"""
The BinDays integration.
"""

# External Packages
from __future__ import annotations
import logging
from datetime import timedelta
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

# Internal Packages
from .api import BinDaysApiClient, BinDaysApiClientError
from .models.collector import Collector
from .models.address import Address
from .models.bin_day import BinDay
from .const import (
    DOMAIN,
    CONF_POSTCODE,
    CONF_ADDRESS_ID,
    CONF_COLLECTOR_ID,
    DEFAULT_API_URL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: List[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up BinDays from a config entry.
    """

    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)
    client = BinDaysApiClient(session, DEFAULT_API_URL)

    postcode = entry.data[CONF_POSTCODE]
    collector_id = entry.data[CONF_COLLECTOR_ID]
    address_id = entry.data[CONF_ADDRESS_ID]

    async def async_update_data() -> List[BinDay]:
        """
        Fetch data from API endpoint.
        """
        try:
            # Reconstruct minimal objects required by the API client
            # The API client expects typed Collector and Address objects
            collector = Collector(
                govUkId=collector_id,
                name="Stored Collector",
                websiteUrl=None,
                govUkUrl=None,
            )
            address = Address(
                uid=address_id,
                postcode=postcode,
                property=None,
                street=None,
                town=None,
            )

            bin_days = await client.get_bin_days(collector, address)
            return bin_days
        except BinDaysApiClientError as err:
            _LOGGER.error("Error communicating with API for %s: %s", address_id, err)
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(hours=12),  # Update twice a day
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload a config entry.
    """
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok