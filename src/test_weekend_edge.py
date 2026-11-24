from datetime import datetime
from pricing import calculate_weekend_price


def test_weekend_starts_at_friday_6_pm():
    price = 1000
    hourly_rate = 100

    start = datetime(2026, 11, 6, 17, 30)
    end = datetime(2026, 11, 7, 10, 0)

    result = calculate_weekend_price(
        price, start, end, hourly_rate
    )

    assert result > price


def test_trip_ends_before_weekend_starts():
    price = 1000
    hourly_rate = 100

    start = datetime(2026, 11, 6, 10, 0)
    end = datetime(2026, 11, 6, 17, 0)

    result = calculate_weekend_price(
        price, start, end, hourly_rate
    )

    assert result == price
