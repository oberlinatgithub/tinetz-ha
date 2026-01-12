import aiohttp
import ssl
import logging

_LOGGER = logging.getLogger(__name__)


class TinetzApi:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def login(self, username: str, password: str) -> None:
        """Login into TINETZ customer portal"""

        url = "https://kundenportal.tinetz.at/powercommerce/tinetz/fo/portal/loginWidget.json"

        payload = {
            "username": username,
            "password": password,
        }

        # SSL workaround for broken certificate chain
        sslcontext = ssl.create_default_context()
        sslcontext.check_hostname = False
        sslcontext.verify_mode = ssl.CERT_NONE

        try:
            async with self._session.post(
                url,
                json=payload,
                ssl=sslcontext,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                text = await response.text()

                _LOGGER.debug("Login response status: %s", response.status)
                _LOGGER.debug("Login response body: %s", text)

                if response.status != 200:
                    raise Exception(f"Login failed with status {response.status}")

        except aiohttp.ClientError as err:
            _LOGGER.error("HTTP error during login: %s", err)
            raise
