"""
Integration tests against the real BinDays API.
"""

# External Packages
import pytest
import aiohttp
import sys
from unittest.mock import MagicMock
from types import ModuleType

# Mock Home Assistant structure to allow importing the package
mock_ha = ModuleType("homeassistant")
mock_ha_core = ModuleType("homeassistant.core")
mock_ha_config = ModuleType("homeassistant.config_entries")
mock_ha_flow = ModuleType("homeassistant.data_entry_flow")
mock_ha_exc = ModuleType("homeassistant.exceptions")
mock_ha_helpers = ModuleType("homeassistant.helpers")
mock_ha_http = ModuleType("homeassistant.helpers.aiohttp_client")
mock_ha_const = ModuleType("homeassistant.const")
mock_ha_update = ModuleType("homeassistant.helpers.update_coordinator")
mock_ha_entity = ModuleType("homeassistant.helpers.entity_platform")
mock_ha_sensor = ModuleType("homeassistant.components.sensor")
mock_ha_components = ModuleType("homeassistant.components")

# Populate attributes to satisfy imports
mock_ha_config.ConfigEntry = MagicMock()
mock_ha_core.HomeAssistant = MagicMock()
mock_ha_const.Platform = MagicMock()
mock_ha_const.Platform.SENSOR = "sensor"
mock_ha_flow.FlowResult = MagicMock()
mock_ha_update.DataUpdateCoordinator = MagicMock()
mock_ha_update.UpdateFailed = Exception
mock_ha_http.async_get_clientsession = MagicMock()
mock_ha_sensor.SensorEntity = MagicMock()
mock_ha_sensor.SensorDeviceClass = MagicMock()
mock_ha_update.CoordinatorEntity = MagicMock()

sys.modules["homeassistant"] = mock_ha
sys.modules["homeassistant.core"] = mock_ha_core
sys.modules["homeassistant.config_entries"] = mock_ha_config
sys.modules["homeassistant.data_entry_flow"] = mock_ha_flow
sys.modules["homeassistant.exceptions"] = mock_ha_exc
sys.modules["homeassistant.helpers"] = mock_ha_helpers
sys.modules["homeassistant.helpers.aiohttp_client"] = mock_ha_http
sys.modules["homeassistant.const"] = mock_ha_const
sys.modules["homeassistant.helpers.update_coordinator"] = mock_ha_update
sys.modules["homeassistant.helpers.entity_platform"] = mock_ha_entity
sys.modules["homeassistant.components"] = mock_ha_components
sys.modules["homeassistant.components.sensor"] = mock_ha_sensor

# Internal Packages
from custom_components.bindays.api.client import BinDaysApiClient
from custom_components.bindays.const import DEFAULT_API_URL


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "postcode",
    [
        "BN14 9NS", "CH46 8AL", "BA13 3JR", "WN7 2LG", "EX20 1ZF", "OX14 3AJ", "OX14 4FQ", "EX38 8LS", "TF5 0LA", "TQ12 4EL",
        "OX11 7NU", "OX9 7DU", "PL8 2NG", "BS16 7ES", "KA19 7BN", "KA7 4RF", "KA8 8BX", "SO15 5NR", "TA1 3AL", "B92 7EX",
        "SY3 7TB", "CF72 9WR", "PL3 6AG", "SA71 4EL", "OX4 3AT", "NE46 3JR", "SG5 3EU", "BH25 7JS", "EX17 1JZ", "M15 6PN",
        "L15 2HF", "L8 2TG", "BD11 1JY", "EX4 1BG", "CB6 1AD", "BH21 1AL", "PL15 7DU", "HP22 5XA", "HP13 5AW", "HP9 1BG",
        "HP7 0NQ", "NR8 6BQ", "BS6 7SR", "BH6 4DE", "B34 6BS", "BA2 2DL", "BT23 4JG"
    ],
)
async def test_real_api_flow(postcode):
    """
    Test the full flow against the real API for a list of postcodes.
    """
    print(f"[{postcode}] Testing...")

    # Use headers to mimic browser/client and disable Brotli if buggy
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "BinDays-HomeAssistant/1.0",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        client = BinDaysApiClient(session, DEFAULT_API_URL)

        # 1. Get Collector
        try:
            collector = await client.get_collector(postcode)
        except Exception as e:
            pytest.fail(f"[{postcode}] Failed to get collector: {e}")

        assert collector is not None
        print(f"[{postcode}] Collector: {collector.name} ({collector.gov_uk_id})")

        # 2. Get Addresses
        try:
            addresses = await client.get_addresses(collector, postcode)
        except Exception as e:
            pytest.fail(f"[{postcode}] Failed to get addresses: {e}")

        assert addresses is not None
        assert len(addresses) > 0
        print(f"[{postcode}] Addresses found: {len(addresses)}")

        # Pick the first address
        target_address = addresses[0]

        # 3. Get Bin Days
        try:
            bin_days = await client.get_bin_days(collector, target_address)
        except Exception as e:
            pytest.fail(
                f"[{postcode}] Failed to get bin days for {target_address.uid}: {e}"
            )

        assert bin_days is not None
        if len(bin_days) > 0:
            first = bin_days[0]
            print(f"[{postcode}] Next: {first.date_str} ({len(first.bins)} bins)")
        else:
            print(f"[{postcode}] No upcoming bin days found (but request succeeded).")