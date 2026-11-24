from datetime import date, datetime
from models import Host, Guest, Vehicle, Booking


def test_create_host():
    host = Host("H001", "Rahul")

    assert host.host_id == "H001"
    assert host.name == "Rahul"


def test_create_guest():
    guest = Guest("G001", "Arun", 22, date(2027, 12, 31), 85)

    assert guest.guest_id == "G001"
    assert guest.name == "Arun"
    assert guest.age == 22
    assert guest.trust_score == 85


def test_create_vehicle():
    vehicle = Vehicle(
        "V001", "H001", "CAR", "HATCHBACK",
        100, 1500, "Bangalore"
    )

    assert vehicle.vehicle_id == "V001"
    assert vehicle.host_id == "H001"
    assert vehicle.segment == "HATCHBACK"


def test_create_booking():
    booking = Booking(
        "B001", "G001", "V001",
        datetime(2026, 11, 5, 10, 0),
        datetime(2026, 11, 5, 15, 0)
    )

    assert booking.booking_id == "B001"
    assert booking.guest_id == "G001"
    assert booking.vehicle_id == "V001"