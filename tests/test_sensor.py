import sys
from unittest.mock import MagicMock

# Mock homeassistant modules
mock_ha = MagicMock()
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.const"] = MagicMock()
sys.modules["homeassistant.components"] = MagicMock()
sys.modules["homeassistant.components.sensor"] = MagicMock()
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.entity_platform"] = MagicMock()
sys.modules["homeassistant.helpers.update_coordinator"] = MagicMock()
sys.modules["homeassistant.helpers.aiohttp_client"] = MagicMock()

# Define Mock classes for inheritance
class MockEntity:
    _attr_has_entity_name = False
    _attr_name = None
    _attr_device_class = None
    _attr_icon = None
    _attr_unique_id = None
    
    def __init__(self, *args, **kwargs):
        pass
    
    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id
        
    @property
    def icon(self):
        return self._attr_icon

class MockCoordinatorEntity(MockEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        super().__init__()

# Assign mocks to modules
sys.modules["homeassistant.components.sensor"].SensorEntity = MockEntity
sys.modules["homeassistant.helpers.update_coordinator"].CoordinatorEntity = MockCoordinatorEntity
sys.modules["homeassistant.helpers.update_coordinator"].DataUpdateCoordinator = MagicMock
sys.modules["homeassistant.components.sensor"].SensorDeviceClass = MagicMock()

import pytest
from datetime import date, timedelta
# Import AFTER mocking
from custom_components.bindays.collection_schedule_sensor import CollectionScheduleSensor
from custom_components.bindays.next_collection_sensor import NextCollectionSensor
from custom_components.bindays.models.bin_day import BinDay
from custom_components.bindays.models.bin import Bin
from custom_components.bindays.models.address import Address

@pytest.fixture
def mock_coordinator():
    coordinator = MagicMock()
    coordinator.data = []
    return coordinator

@pytest.fixture
def mock_entry():
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    return entry

def test_next_collection_sensor_initialization(mock_coordinator, mock_entry):
    sensor = NextCollectionSensor(mock_coordinator, mock_entry.entry_id)
    assert sensor.name == "Next Collection"
    assert sensor.unique_id == "test_entry_id_next_collection"

def test_collection_schedule_sensor_initialization(mock_coordinator, mock_entry):
    sensor = CollectionScheduleSensor(mock_coordinator, mock_entry.entry_id)
    assert sensor.name == "Collection Schedule"
    assert sensor.unique_id == "test_entry_id_collection_schedule"
    assert sensor.icon == "mdi:calendar-clock"

def test_collection_schedule_sensor_state_empty(mock_coordinator, mock_entry):
    sensor = CollectionScheduleSensor(mock_coordinator, mock_entry.entry_id)
    assert sensor.native_value == 0
    assert sensor.extra_state_attributes == {"upcoming_collections": []}

def test_collection_schedule_sensor_state_with_data(mock_coordinator, mock_entry):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    
    address = Address(uprn="123", line1="Test St", postcode="TE1 1ST", uid="123")
    
    bin1 = Bin(name="General", colour="Black")
    bin2 = Bin(name="Recycling", colour="Green")
    
    # Yesterday (should be ignored)
    bd1 = BinDay(date=yesterday.isoformat(), address=address, bins=[bin1])
    # Today (should be included)
    bd2 = BinDay(date=today.isoformat(), address=address, bins=[bin2])
    # Tomorrow (should be included)
    bd3 = BinDay(date=tomorrow.isoformat(), address=address, bins=[bin1, bin2])
    
    mock_coordinator.data = [bd3, bd1, bd2] # Unsorted input
    
    sensor = CollectionScheduleSensor(mock_coordinator, mock_entry.entry_id)
    
    assert sensor.native_value == 2
    
    attributes = sensor.extra_state_attributes
    upcoming = attributes["upcoming_collections"]
    assert len(upcoming) == 2
    
    # check sorting
    assert upcoming[0]["date"] == today.isoformat()
    assert upcoming[1]["date"] == tomorrow.isoformat()
    
    # check content
    assert upcoming[0]["bins"][0]["name"] == "Recycling"
    assert len(upcoming[1]["bins"]) == 2