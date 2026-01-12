from datetime import date, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, DEFAULT_DELAY_DAYS
import logging

_LOGGER = logging.getLogger(__name__)

class TinetzCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
        )
        self.api = api

    async def _async_update_data(self):
        today = date.today()
        end = today - timedelta(days=DEFAULT_DELAY_DAYS)
        start = end.replace(day=1)

        return await self.hass.async_add_executor_job(
            self.api.get_consumption, start, end
        )
