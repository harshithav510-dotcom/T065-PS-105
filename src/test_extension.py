
from datetime import datetime
from extension import calculate_extension_fee


def test_two_hour_extension():
    old_end = datetime(2026, 11, 5, 15, 0)
    new_end = datetime(2026, 11, 5, 17, 0)

    fee = calculate_extension_fee(old_end, new_end, 100)

    assert fee == 200


def test_one_hour_extension():
    old_end = datetime(2026, 11, 5, 15, 0)
    new_end = datetime(2026, 11, 5, 16, 0)

    fee = calculate_extension_fee(old_end, new_end, 100)

    assert fee == 100

