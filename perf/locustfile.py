from locust import HttpUser, task, between
from src.utils.data import make_booking_payload

class BookingUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_read_delete(self):
        r = self.client.post("/booking", json=make_booking_payload())
        if r.status_code != 200:
            return
        booking_id = r.json().get("bookingid")
        self.client.get(f"/booking/{booking_id}")
        self.client.delete(f"/booking/{booking_id}")
