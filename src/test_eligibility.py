
from datetime import date, datetime
from models import Guest, Vehicle
from eligibility import check_eligibility


def create_guest():
    return Guest(
        "G001", "Arun", 22,
        date(2027, 12, 31), 85
    )


def create_vehicle():
    return Vehicle(
        "V001", "H001", "CAR",
        "HATCHBACK", 100, 1500, "Bangalore"
    )


def test_eligible_guest():
    result, message = check_eligibility(
        create_guest(),
        create_vehicle(),
        datetime(2026, 11, 5, 10),
        datetime(2026, 11, 5, 15)
    )

    assert result is True


def test_underage_guest():
    guest = create_guest()
    guest.age = 18

    result, message = check_eligibility(
        guest,
        create_vehicle(),
        datetime(2026, 11, 5, 10),
        datetime(2026, 11, 5, 15)
    )

    assert result is False

