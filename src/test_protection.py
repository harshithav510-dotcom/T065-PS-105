from settlement import calculate_protection_fee


def test_protection_fee_minimum():
    assert calculate_protection_fee(1000) == 150


def test_protection_fee_percentage():
    assert calculate_protection_fee(5000) == 400


def test_protection_fee_high_trip_price():
    assert calculate_protection_fee(10000) == 800
