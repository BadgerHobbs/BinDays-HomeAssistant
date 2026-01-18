"""
Sensor showing all upcoming bin collections.
"""

from __future__ import annotations
from typing import Any, List
from datetime import date

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .models.bin_day import BinDay


class CollectionScheduleSensor(CoordinatorEntity, SensorEntity):
    """
    Sensor showing all upcoming bin collections.
    """

    _attr_has_entity_name = True
    _attr_name = "Collection Schedule"
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str) -> None:
        """
        Initialize the sensor.
        """
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_collection_schedule"

    @property
    def native_value(self) -> int:
        """
        Return the state of the sensor (count of upcoming collections).
        """
        upcoming = self._get_upcoming_collections()
        return len(upcoming)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """
        Return the state attributes.
        """
        upcoming = self._get_upcoming_collections()
        schedule = []
        for date_obj, bin_day in upcoming:
            schedule.append({
                "date": date_obj.isoformat(),
                "bins": [
                    {
                        "name": b.name,
                        "colour": b.colour,
                        "type": b.type,
                        "keys": b.keys
                    } for b in bin_day.bins
                ]
            })

        return {
            "upcoming_collections": schedule
        }

    def _get_upcoming_collections(self) -> List[tuple[date, BinDay]]:
        """
        Get all upcoming collections from the coordinator data.
        """
        bin_days: List[BinDay] = self.coordinator.data
        if not bin_days:
            return []

        today = date.today()
        upcoming = []

        for d in bin_days:
            d_date = d.parsed_date
            if d_date >= today:
                upcoming.append((d_date, d))

        # Sort by date
        upcoming.sort(key=lambda x: x[0])
        return upcoming
