from datetime import datetime
from pricing import calculate_weekend_price


def test_friday_evening_to_saturday_morning():
    price = 1000
    hourly_rate = 100

    start = datetime(2026, 11, 6, 19, 0)
    end = datetime(2026, 11, 7, 10, 0)

    final_price = calculate_weekend_price(
        price, start, end, hourly_rate
    )

    assert final_price == 1300


def test_weekday_trip_without_weekend_hours():
    price = 1000
    hourly_rate = 100

    start = datetime(2026, 11, 2, 10, 0)
    end = datetime(2026, 11, 2, 20, 0)

    final_price = calculate_weekend_price(
        price, start, end, hourly_rate
    )

    assert final_price == 1000
