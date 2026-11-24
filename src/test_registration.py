from datetime import date
from registration import (
    register_host,
    register_guest,
    register_vehicle
)


def test_register_host():
    hosts = []

    host = register_host(hosts, "H001", "Rahul")

    assert host is not None
    assert len(hosts) == 1


def test_register_guest():
    guests = []

    guest = register_guest(
        guests, "G001", "Arun", 22,
        date(2027, 12, 31), 85
    )

    assert guest is not None
    assert len(guests) == 1


def test_register_vehicle():
    vehicles = []

    vehicle = register_vehicle(
        vehicles, "V001", "H001", "CAR",
        "HATCHBACK", 100, 1500, "Bangalore"
    )

    assert vehicle is not None
    assert len(vehicles) == 1
