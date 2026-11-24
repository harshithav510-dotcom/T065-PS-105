
from datetime import date, datetime
from models import Guest, Vehicle
from booking import create_booking


def test_booking_creation():

    guest = Guest(
        "G001", "Arun", 22,
        date(2027, 12, 31), 85
    )

    vehicle = Vehicle(
        "V001", "H001", "CAR",
        "HATCHBACK", 100, 1500, "Bangalore"
    )

    bookings = []

    booking, message = create_booking(
        guest,
        vehicle,
        datetime(2026, 11, 5, 10, 0),
        datetime(2026, 11, 5, 15, 0),
        bookings
    )

    assert booking is not None
    assert message == "Booking successful."
    assert booking["status"] == "BOOKED"
    assert booking["trip_price"] == 500.0
    assert booking["deposit"] == 1500.0


