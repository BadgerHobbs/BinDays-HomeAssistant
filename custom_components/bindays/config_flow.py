"""
Config flow for BinDays integration.
"""

# External Packages
from __future__ import annotations
import logging
from typing import Any, List, Optional, Dict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# Internal Packages
from .api import BinDaysApiClient, BinDaysApiClientError
from .models.collector import Collector
from .models.address import Address
from .const import (
    DOMAIN,
    CONF_POSTCODE,
    CONF_ADDRESS_ID,
    CONF_COLLECTOR_ID,
    DEFAULT_API_URL,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_POSTCODE): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Handle a config flow for BinDays.
    """

    VERSION = 1

    def __init__(self) -> None:
        """
        Initialize.
        """
        self.api: Optional[BinDaysApiClient] = None
        self.postcode: Optional[str] = None
        self.collector: Optional[Collector] = None
        self.addresses: Optional[List[Address]] = None

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """
        Handle the initial step.
        """
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.postcode = user_input[CONF_POSTCODE].strip().upper()

            session = async_get_clientsession(self.hass)
            self.api = BinDaysApiClient(session, DEFAULT_API_URL)

            try:
                # 1. Get Collector
                self.collector = await self.api.get_collector(self.postcode)

                # 2. Get Addresses
                self.addresses = await self.api.get_addresses(
                    self.collector, self.postcode
                )

                if not self.addresses:
                    errors["base"] = "no_addresses_found"
                else:
                    return await self.async_step_address()

            except BinDaysApiClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_address(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """
        Handle the address selection step.
        """
        errors: Dict[str, str] = {}

        address_options = {}
        if self.addresses:
            for addr in self.addresses:
                # Use the __str__ method of Address model for label
                address_options[addr.uid] = str(addr)

        if user_input is not None:
            address_uid = user_input[CONF_ADDRESS_ID]
            selected_address_label = address_options.get(address_uid)

            return self.async_create_entry(
                title=f"{selected_address_label}",
                data={
                    CONF_POSTCODE: self.postcode,
                    CONF_COLLECTOR_ID: self.collector.gov_uk_id,
                    CONF_ADDRESS_ID: address_uid,
                },
            )

        return self.async_show_form(
            step_id="address",
            data_schema=vol.Schema(
                {vol.Required(CONF_ADDRESS_ID): vol.In(address_options)}
            ),
            errors=errors,
        )