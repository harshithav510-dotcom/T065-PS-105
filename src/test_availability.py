
from datetime import datetime
from models import Booking
from availability import check_availability


def test_overlapping_booking():
    booking = Booking(
        "B001", "G001", "V001",
        datetime(2026, 11, 5, 10, 0),
        datetime(2026, 11, 5, 15, 0)
    )

    available, message = check_availability(
        "V001",
        datetime(2026, 11, 5, 12, 0),
        datetime(2026, 11, 5, 16, 0),
        [booking]
    )

    assert available is False


def test_non_overlapping_booking():
    booking = Booking(
        "B001", "G001", "V001",
        datetime(2026, 11, 5, 10, 0),
        datetime(2026, 11, 5, 15, 0)
    )

    available, message = check_availability(
        "V001",
        datetime(2026, 11, 5, 16, 0),
        datetime(2026, 11, 5, 18, 0),
        [booking]
    )

    assert available is True

