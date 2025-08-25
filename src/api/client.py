import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv
from src.api import endpoints

load_dotenv()
DEFAULT_BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")

class RestfulBookerClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def create_token(self, username: str, password: str) -> str:
        url = self.base_url + endpoints.AUTH
        resp = self.session.post(url, json={"username": username, "password": password})
        resp.raise_for_status()
        token = resp.json().get("token")
        self.session.cookies.set("token", token)
        return token

    def create_booking(self, payload: Dict[str, Any]) -> requests.Response:
        return self.session.post(self.base_url + endpoints.BOOKING, json=payload)

    def get_booking(self, booking_id: int) -> requests.Response:
        url = self.base_url + endpoints.BOOKING_ID.format(booking_id=booking_id)
        return self.session.get(url)

    def update_booking(self, booking_id: int, payload: Dict[str, Any]) -> requests.Response:
        url = self.base_url + endpoints.BOOKING_ID.format(booking_id=booking_id)
        return self.session.put(url, json=payload, headers={"Content-Type": "application/json"})

    def partial_update_booking(self, booking_id: int, payload: Dict[str, Any]) -> requests.Response:
        url = self.base_url + endpoints.BOOKING_ID.format(booking_id=booking_id)
        return self.session.patch(url, json=payload, headers={"Content-Type": "application/json"})

    def delete_booking(self, booking_id: int) -> requests.Response:
        url = self.base_url + endpoints.BOOKING_ID.format(booking_id=booking_id)
        return self.session.delete(url)
