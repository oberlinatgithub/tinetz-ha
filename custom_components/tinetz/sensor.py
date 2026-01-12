from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TinetzConsumptionSensor(coordinator)])

class TinetzConsumptionSensor(SensorEntity):
    _attr_name = "TINETZ Verbrauch (Monat bis vorgestern)"
    _attr_unit_of_measurement = "kWh"
    _attr_device_class = "energy"
    _attr_state_class = "total_increasing"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def state(self):
        return self.coordinator.data
