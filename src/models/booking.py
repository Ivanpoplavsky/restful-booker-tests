from typing import Optional
from pydantic import BaseModel, Field, constr

class BookingDates(BaseModel):
    checkin: constr(strip_whitespace=True)
    checkout: constr(strip_whitespace=True)

class Booking(BaseModel):
    firstname: constr(strip_whitespace=True)
    lastname: constr(strip_whitespace=True)
    totalprice: int = Field(ge=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

class CreateBookingResponse(BaseModel):
    bookingid: int
    booking: Booking
