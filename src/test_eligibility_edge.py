
from datetime import date, datetime
from models import Guest, Vehicle
from eligibility import check_eligibility


def create_vehicle():
    return Vehicle(
        "V001", "H001", "CAR",
        "LUXURY", 500, 5000, "Bangalore"
    )


start = datetime(2026, 11, 5, 10)
end = datetime(2026, 11, 5, 15)


def test_guest_below_minimum_age():
    guest = Guest("G001", "Arun", 20, date(2027, 12, 31), 85)
    result, message = check_eligibility(
        guest, create_vehicle(), start, end
    )
    assert result is False


def test_luxury_vehicle_low_trust_score():
    guest = Guest("G002", "Ravi", 25, date(2027, 12, 31), 30)
    result, message = check_eligibility(
        guest, create_vehicle(), start, end
    )
    assert result is False


def test_expired_licence():
    guest = Guest("G003", "Sam", 25, date(2026, 11, 5), 85)
    result, message = check_eligibility(
        guest, create_vehicle(), start, end
    )
    assert result is False

