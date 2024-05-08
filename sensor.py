"""Platform for sensor integration."""

from __future__ import annotations

from functools import partial

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import ATTRIBUTE_OPTIONS


async def async_trigger_update_callback(
    entity: IOSSleepSensor, call: ServiceCall, state: str
) -> None:
    """Handle incoming data."""

    if state not in ATTRIBUTE_OPTIONS:
        return

    if entity:
        await entity.async_trigger_update(state)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> bool:
    """Set up the sensor platform."""
    # platform.async_register_entity_service(
    #     "set_relaxation", {"state": "relaxation"}, "async_trigger_update"
    # )
    # platform.async_register_entity_service(
    #     "set_sleep", {"state": "sleep"}, "async_trigger_update"
    # )
    # add_entities([IOSSleepSensor(entry, hass)])

    entity = IOSSleepSensor(entry, hass)
    add_entities([entity])

    platform = async_get_current_platform()

    platform.async_register_entity_service(
        "set_awake",
        {},
        partial(async_trigger_update_callback, state="awake"),
    )

    platform.async_register_entity_service(
        "set_relaxation",
        {},
        partial(async_trigger_update_callback, state="relaxation"),
    )

    platform.async_register_entity_service(
        "set_sleep",
        {},
        partial(async_trigger_update_callback, state="sleep"),
    )

    return True


class IOSSleepSensor(SensorEntity):
    """iOS sleep sensor."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:sleep"
    _attr_should_poll = False
    _attr_options = ATTRIBUTE_OPTIONS

    def __init__(self, config_entry: ConfigEntry, hass: HomeAssistant) -> None:
        """Initialize the sensor."""

        super().__init__()
        self._attr_native_value = "awake"
        self._attr_name, self.ios_device_name = self._compute_name(config_entry, hass)
        self._attr_unique_id = str(config_entry.data["ios_device_id"]).lower()

        self.incoming_value = "awake"

    def _compute_name(self, config_entry: ConfigEntry, hass: HomeAssistant) -> str:
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(config_entry.data["ios_device_id"])

        return device.name + " iOS Sleep Schedule", device.name

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.incoming_value

    async def async_trigger_update(self, state) -> None:
        """Handle incoming data."""

        self.incoming_value = state
        await self.async_update()
        self.async_schedule_update_ha_state()
