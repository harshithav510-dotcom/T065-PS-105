
from settlement import calculate_commission_rate


def test_commission_below_10_trips():
    assert calculate_commission_rate(0) == 0.20
    assert calculate_commission_rate(9) == 0.20


def test_commission_at_10_trips():
    assert calculate_commission_rate(10) == 0.15


def test_commission_below_50_trips():
    assert calculate_commission_rate(49) == 0.15


def test_commission_at_50_trips():
    assert calculate_commission_rate(50) == 0.12

