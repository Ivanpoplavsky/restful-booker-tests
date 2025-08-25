from locust import HttpUser, task, between
from datetime import datetime, timedelta
import os
import random
import json


RB_USERNAME = os.getenv("RB_USERNAME", "admin")
RB_PASSWORD = os.getenv("RB_PASSWORD", "password123")


def make_booking_payload(firstname="John", lastname="Doe"):
    start = (datetime.utcnow() + timedelta(days=1)).date().isoformat()
    end = (datetime.utcnow() + timedelta(days=random.randint(2, 10))).date().isoformat()
    return {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": random.randint(50, 5000),
        "depositpaid": random.choice([True, False]),
        "bookingdates": {"checkin": start, "checkout": end},
        "additionalneeds": random.choice(["Breakfast", "Late checkout", "None"]),
    }


class BookingUser(HttpUser):
    wait_time = between(1, 3)  # паузы между действиями

    def on_start(self):
        """
        Вызывается при старте виртуального пользователя:
        получаем токен через /auth и сохраняем его как Cookie "token".
        """
        with self.client.post(
            "/auth",
            json={"username": RB_USERNAME, "password": RB_PASSWORD},
            name="AUTH /auth",
            catch_response=True,
        ) as r:
            try:
                if r.status_code != 200:
                    r.failure(f"Auth failed: {r.status_code} {r.text}")
                    return
                token = r.json().get("token")
                if not token:
                    r.failure(f"No token in auth response: {r.text}")
                    return
                # В Restful-Booker аутентификация дальше идёт через Cookie "token"
                self.client.cookies.set("token", token)
                r.success()
            except Exception as e:
                r.failure(f"Auth exception: {e}")

    @task(5)
    def crud_flow(self):
        """
        Полный сценарий:
        1) POST /booking  -> 200
        2) GET /booking/{id} -> 200
        3) PUT /booking/{id} -> 200
        4) PATCH /booking/{id} -> 200
        5) DELETE /booking/{id} -> 201
        """
        # 1) CREATE
        payload = make_booking_payload()
        with self.client.post("/booking", json=payload, name="POST /booking", catch_response=True) as r_create:
            if r_create.status_code != 200:
                r_create.failure(f"Create failed: {r_create.status_code} {r_create.text}")
                return
            try:
                booking_id = r_create.json().get("bookingid")
            except Exception:
                r_create.failure(f"Bad create response: {r_create.text}")
                return

        # 2) READ
        with self.client.get(f"/booking/{booking_id}", name="GET /booking/{id}", catch_response=True) as r_get:
            if r_get.status_code != 200:
                r_get.failure(f"Get failed: {r_get.status_code} {r_get.text}")
            else:
                r_get.success()

        # 3) UPDATE (PUT)
        updated_payload = make_booking_payload(firstname="UpdatedName", lastname=payload["lastname"])
        with self.client.put(
            f"/booking/{booking_id}",
            json=updated_payload,
            headers={"Content-Type": "application/json"},
            name="PUT /booking/{id}",
            catch_response=True,
        ) as r_put:
            if r_put.status_code != 200:
                r_put.failure(f"Put failed: {r_put.status_code} {r_put.text}")
            else:
                # простая проверка поля
                try:
                    if r_put.json().get("firstname") != "UpdatedName":
                        r_put.failure(f"Put content mismatch: {r_put.text}")
                    else:
                        r_put.success()
                except Exception:
                    r_put.failure(f"Put non-JSON: {r_put.text}")

        # 4) PARTIAL UPDATE (PATCH)
        patch_body = {"totalprice": 777}
        with self.client.patch(
            f"/booking/{booking_id}",
            json=patch_body,
            headers={"Content-Type": "application/json"},
            name="PATCH /booking/{id}",
            catch_response=True,
        ) as r_patch:
            if r_patch.status_code != 200:
                r_patch.failure(f"Patch failed: {r_patch.status_code} {r_patch.text}")
            else:
                try:
                    if r_patch.json().get("totalprice") != 777:
                        r_patch.failure(f"Patch content mismatch: {r_patch.text}")
                    else:
                        r_patch.success()
                except Exception:
                    r_patch.failure(f"Patch non-JSON: {r_patch.text}")

        # 5) DELETE (ожидается 201 у демо-сервиса)
        with self.client.delete(
            f"/booking/{booking_id}",
            name="DELETE /booking/{id}",
            catch_response=True,
        ) as r_del:
            if r_del.status_code != 201:
                r_del.failure(f"Delete expected 201, got {r_del.status_code}: {r_del.text}")
            else:
                r_del.success()
