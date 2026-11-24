from datetime import datetime, timedelta
from trip_manager import calculate_late_fee


def test_two_hours_late():
    expected = datetime(2026, 11, 5, 10, 0)
    actual = expected + timedelta(hours=2)

    fee, extra = calculate_late_fee(actual, expected, 100)

    assert fee == 300
    assert extra == 0


def test_one_hour_late():
    expected = datetime(2026, 11, 5, 10, 0)
    actual = expected + timedelta(hours=1)

    fee, extra = calculate_late_fee(actual, expected, 100)

    assert fee == 150
    assert extra == 0


def test_no_late_fee():
    expected = datetime(2026, 11, 5, 10, 0)

    fee, extra = calculate_late_fee(expected, expected, 100)

    assert fee == 0
    assert extra == 0
