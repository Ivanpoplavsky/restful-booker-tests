import pytest
from src.models.booking import Booking, CreateBookingResponse

@pytest.mark.crud
def test_create_read_booking(client, booking_payload):
    r = client.create_booking(booking_payload)
    assert r.status_code == 200
    body = CreateBookingResponse.model_validate(r.json())
    gr = client.get_booking(body.bookingid)
    assert gr.status_code == 200
    got = Booking.model_validate(gr.json())
    assert got.firstname == booking_payload["firstname"]

@pytest.mark.crud
def test_update_booking_put(client, token, created_booking, booking_payload):
    booking_payload["firstname"] = "UpdatedName"
    r = client.update_booking(created_booking, booking_payload)
    assert r.status_code == 200
    updated = Booking.model_validate(r.json())
    assert updated.firstname == "UpdatedName"

@pytest.mark.crud
def test_partial_update_booking_patch(client, token, created_booking):
    r = client.partial_update_booking(created_booking, {"firstname": "Patchy"})
    assert r.status_code == 200
    assert r.json()["firstname"] == "Patchy"

@pytest.mark.crud
def test_delete_booking(client, token, created_booking):
    r = client.delete_booking(created_booking)
    assert r.status_code == 201, f"Unexpected status: {r.status_code}, body: {r.text}"
    gr = client.get_booking(created_booking)
    assert gr.status_code == 404
