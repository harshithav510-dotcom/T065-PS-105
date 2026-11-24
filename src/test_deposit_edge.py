
from deposit import calculate_deposit


def test_trust_score_80_gets_half_deposit():
    assert calculate_deposit("HATCHBACK", 80) == 1500


def test_trust_score_79_gets_full_deposit():
    assert calculate_deposit("HATCHBACK", 79) == 3000


def test_bike_high_trust_deposit():
    assert calculate_deposit("BIKE", 90) == 500

