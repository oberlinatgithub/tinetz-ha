from .const import DOMAIN
from .api import TinetzApi
from .coordinator import TinetzCoordinator

async def async_setup_entry(hass, entry):
    api = TinetzApi(
        entry.data["username"],
        entry.data["password"]
    )
    await hass.async_add_executor_job(api.login)

    coordinator = TinetzCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    return True
