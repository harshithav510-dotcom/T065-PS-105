
from deposit import calculate_deposit


def test_hatchback_high_trust_deposit():
    assert calculate_deposit("HATCHBACK", 85) == 1500


def test_hatchback_normal_trust_deposit():
    assert calculate_deposit("HATCHBACK", 70) == 3000


def test_suv_high_trust_deposit():
    assert calculate_deposit("SUV", 85) == 4000


def test_bike_deposit():
    assert calculate_deposit("BIKE", 70) == 1000
