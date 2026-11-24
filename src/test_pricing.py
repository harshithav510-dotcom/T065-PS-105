from datetime import datetime, timedelta
from pricing import calculate_duration_price


def test_five_hour_trip_price():
    start = datetime(2026, 11, 5, 10, 0)
    end = datetime(2026, 11, 5, 15, 0)

    price = calculate_duration_price(start, end, 100, 1500)

    assert price == 500


def test_one_hour_trip_price():
    start = datetime(2026, 11, 5, 10, 0)
    end = start + timedelta(hours=1)

    price = calculate_duration_price(start, end, 100, 1500)

    assert price == 100


def test_daily_trip_price():
    start = datetime(2026, 11, 5, 10, 0)
    end = start + timedelta(hours=30)

    price = calculate_duration_price(start, end, 100, 1500)

    assert price == 3000