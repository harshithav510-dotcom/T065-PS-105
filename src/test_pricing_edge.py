from datetime import datetime
from pricing import calculate_duration_price


def test_exactly_24_hours():
    start = datetime(2026, 11, 5, 10, 0)
    end = datetime(2026, 11, 6, 10, 0)

    price = calculate_duration_price(start, end, 100, 1500)

    assert price == 1500


def test_25_hours():
    start = datetime(2026, 11, 5, 10, 0)
    end = datetime(2026, 11, 6, 11, 0)

    price = calculate_duration_price(start, end, 100, 1500)

    assert price == 3000