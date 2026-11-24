
from fuel import calculate_fuel_charge


def test_bike_fuel_charge():
    assert calculate_fuel_charge(4, 3, "BIKE") == 150


def test_car_fuel_charge():
    assert calculate_fuel_charge(8, 7, "CAR") == 600


def test_no_fuel_shortage():
    assert calculate_fuel_charge(5, 5, "CAR") == 0


def test_multiple_units_bike():
    assert calculate_fuel_charge(6, 3, "BIKE") == 450

