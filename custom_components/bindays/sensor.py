"""
Platform for sensor integration.
"""

# External Packages
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Internal Packages
from .const import DOMAIN
from .next_collection_sensor import NextCollectionSensor
from .collection_schedule_sensor import CollectionScheduleSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up the sensor platform.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        NextCollectionSensor(coordinator, entry.entry_id),
        CollectionScheduleSensor(coordinator, entry.entry_id),
    ]

    async_add_entities(entities)
