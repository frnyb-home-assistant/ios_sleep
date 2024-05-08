"""The iOS Sleep Schedule integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant  # , ServiceCall, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN

# # TODO List the platforms that you want to support.
# # For your initial PR, limit it to 1 platform.
# # Done
PLATFORMS: list[Platform] = [Platform.SENSOR]


# async def async_setup(hass: HomeAssistant, config: dict) -> bool:
#     """Set up the iOS Sleep Schedule component."""

#     @callback
#     def set_sleep_state_service_callback(call: ServiceCall, state: str) -> None:
#         """Set the sleep state."""

#         if "ios_device_name" not in call.data:
#             return

#         update_callback = None
#         entry_id = None

#         for entr_id, entry_data in hass.data[DOMAIN].items():
#             if entry_data["ios_device_name"] == call.data["ios_device_name"]:
#                 update_callback = entry_data["update_callback"]
#                 entry_id = entr_id
#                 break

#         if entry_id is None:
#             return

#         if update_callback is not None:
#             update_callback(state)

#     hass.services.async_register(
#         DOMAIN,
#         "set_sleep_state",
#         set_sleep_state_service_callback,
#         schema={
#             "type": "object",
#             "properties": {
#                 "ios_device_name": {"type": "string"},
#                 "state": {"type": "string"},
#             },
#             "required": ["ios_device_name", "state"],
#         },
#     )

#     return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up iOS Sleep Schedule from a config entry."""

    # hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    # entry_data = {}

    # device_registry = dr.async_get(hass)
    # device = device_registry.async_get(entry.data["ios_device_id"])

    # entry_data["ios_device_name"] = device.name
    # entry_data["config_entry"] = entry
    # entry_data["update_callback"] = None

    # hass.data[DOMAIN][entry.entry_id] = entry_data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
    #     hass.data[DOMAIN].pop(entry.entry_id)

    # return unload_ok

    return True
