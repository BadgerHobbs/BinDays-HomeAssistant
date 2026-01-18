"""
Platform for sensor integration.
"""

# External Packages
from __future__ import annotations
from typing import Any, List, Optional
from datetime import date

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

# Internal Packages
from .const import DOMAIN
from .models.bin_day import BinDay


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up the sensor platform.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [NextCollectionSensor(coordinator, entry.entry_id)]

    async_add_entities(entities)


class NextCollectionSensor(CoordinatorEntity, SensorEntity):
    """
    Sensor showing the next bin collection date.
    """

    _attr_has_entity_name = True
    _attr_name = "Next Collection"
    _attr_device_class = SensorDeviceClass.DATE
    _attr_icon = "mdi:delete"

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str) -> None:
        """
        Initialize the sensor.
        """
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_next_collection"

    @property
    def native_value(self) -> Optional[date]:
        """
        Return the state of the sensor.
        """
        next_collection: Optional[BinDay] = self._get_next_collection()
        if next_collection:
            return next_collection.parsed_date
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """
        Return the state attributes.
        """
        next_collection: Optional[BinDay] = self._get_next_collection()
        if not next_collection:
            return {}

        bins = next_collection.bins
        bin_names = [b.name for b in bins]
        bin_colours = [b.colour for b in bins]

        # We can also return raw dictionary structure for template flexibility
        raw_bins = [
            {"name": b.name, "colour": b.colour, "type": b.type, "keys": b.keys}
            for b in bins
        ]

        return {
            "bins": bin_names,
            "colours": bin_colours,
            "raw_bins": raw_bins,
        }

    def _get_next_collection(self) -> Optional[BinDay]:
        """
        Get the next collection from the coordinator data.
        """
        bin_days: List[BinDay] = self.coordinator.data
        if not bin_days:
            return None

        today = date.today()
        upcoming = []

        for d in bin_days:
            d_date = d.parsed_date
            if d_date >= today:
                upcoming.append((d_date, d))

        # Sort by date
        upcoming.sort(key=lambda x: x[0])

        if upcoming:
            return upcoming[0][1]

        return None