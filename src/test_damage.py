
from damage import calculate_damage_charge


def test_damage_with_protection():
    charge = calculate_damage_charge(3000, 1500, True)
    assert charge == 1500


def test_damage_without_protection():
    charge = calculate_damage_charge(3000, 1500, False)
    assert charge == 1500


def test_damage_below_deposit():
    charge = calculate_damage_charge(500, 1500, False)
    assert charge == 500


def test_zero_damage():
    charge = calculate_damage_charge(0, 1500, False)
    assert charge == 0

