from homeassistant import config_entries
import voluptuous as vol
from .api import TinetzApi
from .const import DOMAIN

class TinetzConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            api = TinetzApi(
                user_input["username"],
                user_input["password"]
            )
            await self.hass.async_add_executor_job(api.login)

            return self.async_create_entry(
                title="TINETZ",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str
            })
        )
