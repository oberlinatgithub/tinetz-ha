from datetime import date
import requests

BASE_URL = "https://kundenportal.tinetz.at"

class TinetzApi:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def login(self):
        url = f"{BASE_URL}/powercommerce/tinetz/fo/portal/loginWidget.json"
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        r = self.session.post(url, data=payload, headers=headers)
        r.raise_for_status()

    def get_consumption(self, start_date: date, end_date: date):
        url = f"{BASE_URL}/powercommerce/tinetz/fo/portal/analysis/valueRequest"
        payload = {
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
            "granularity": "P1D"
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
        r = self.session.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return self._parse(r.json())

    def _parse(self, data):
        for indicator in data.get("indicatorValueResponses", []):
            values = indicator.get("values", [])
            if values:
                return values[-1]["value"]
        return None
