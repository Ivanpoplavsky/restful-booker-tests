from faker import Faker
from datetime import date, timedelta

fake = Faker()

def make_booking_payload(firstname=None, lastname=None, totalprice=None, depositpaid=None, additionalneeds=None):
    firstname = firstname or fake.first_name()
    lastname = lastname or fake.last_name()
    totalprice = totalprice if totalprice is not None else fake.random_int(min=50, max=5000)
    depositpaid = bool(depositpaid) if depositpaid is not None else fake.boolean()
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=fake.random_int(min=1, max=14))

    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": start.isoformat(),
            "checkout": end.isoformat(),
        },
    }
    if additionalneeds is not None:
        payload["additionalneeds"] = additionalneeds
    return payload
