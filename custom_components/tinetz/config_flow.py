from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import voluptuous as vol
import logging

from .api import TinetzApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class TinetzConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            username = user_input["username"]
            password = user_input["password"]

            session = async_get_clientsession(self.hass)
            api = TinetzApi(session)

            try:
                await api.login(username, password)

                return self.async_create_entry(
                    title="TINETZ",
                    data={
                        "username": username,
                        "password": password,
                    },
                )

            except Exception as err:
                _LOGGER.exception("Unexpected error during TINETZ login")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )
