from datetime import datetime, timedelta
from trip_manager import calculate_late_fee


def test_no_fee_within_30_minutes():
    expected = datetime(2026, 11, 5, 10, 0)

    fee, inconvenience = calculate_late_fee(
        expected + timedelta(minutes=30), expected, 100
    )

    assert fee == 0
    assert inconvenience == 0


def test_fee_after_30_minutes():
    expected = datetime(2026, 11, 5, 10, 0)

    fee, inconvenience = calculate_late_fee(
        expected + timedelta(minutes=31), expected, 100
    )

    assert fee == 150
    assert inconvenience == 0


def test_fee_at_6_hours():
    expected = datetime(2026, 11, 5, 10, 0)

    fee, inconvenience = calculate_late_fee(
        expected + timedelta(hours=6), expected, 100
    )

    assert fee == 750
    assert inconvenience == 0


def test_inconvenience_fee_after_6_hours():
    expected = datetime(2026, 11, 5, 10, 0)

    fee, inconvenience = calculate_late_fee(
        expected + timedelta(hours=6, minutes=1), expected, 100
    )

    assert fee == 950
    assert inconvenience == 1000
