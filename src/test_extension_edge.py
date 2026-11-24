
from datetime import datetime, timedelta
from extension import check_extension


def test_extension_with_two_hour_gap():
    new_end = datetime(2026, 11, 5, 15, 0)

    next_booking = type("BookingRecord", (), {
        "booking_id": "B002",
        "vehicle_id": "V001",
        "start_time": new_end + timedelta(hours=2),
        "end_time": new_end + timedelta(hours=5),
        "status": "BOOKED"
    })()

    allowed, message = check_extension(
        "V001", "B001", new_end, [next_booking]
    )

    assert allowed is True


def test_extension_with_less_than_two_hour_gap():
    new_end = datetime(2026, 11, 5, 15, 0)

    next_booking = type("BookingRecord", (), {
        "booking_id": "B002",
        "vehicle_id": "V001",
        "start_time": new_end + timedelta(hours=1),
        "end_time": new_end + timedelta(hours=5),
        "status": "BOOKED"
    })()

    allowed, message = check_extension(
        "V001", "B001", new_end, [next_booking]
    )

    assert allowed is False
