import os, pytest
from dotenv import load_dotenv
from src.api.client import RestfulBookerClient
from src.utils.data import make_booking_payload
from src.models.booking import Booking, CreateBookingResponse

load_dotenv()

@pytest.fixture(scope="session")
def client():
    return RestfulBookerClient()

@pytest.fixture(scope="session")
def creds():
    return (os.getenv("RB_USERNAME", "admin"), os.getenv("RB_PASSWORD", "password123"))

@pytest.fixture(scope="session")
def token(client, creds):
    return client.create_token(*creds)

@pytest.fixture
def booking_payload():
    return make_booking_payload(additionalneeds="Breakfast")

@pytest.fixture
def created_booking(client, booking_payload):
    r = client.create_booking(booking_payload)
    obj = CreateBookingResponse.model_validate(r.json())
    yield obj.bookingid
    try:
        client.delete_booking(obj.bookingid)
    except Exception:
        pass
