
import pytest
from pricing import calculate_km_charge


def test_hatchback_excess_km():
    assert calculate_km_charge(400, 300, "HATCHBACK") == 800


def test_sedan_excess_km():
    assert calculate_km_charge(400, 300, "SEDAN") == 1200


def test_bike_excess_km():
    assert calculate_km_charge(400, 300, "BIKE") == 300


def test_no_excess_km():
    assert calculate_km_charge(200, 300, "HATCHBACK") == 0


def test_negative_distance():
    with pytest.raises(ValueError):
        calculate_km_charge(-10, 100, "HATCHBACK")


def test_invalid_segment():
    with pytest.raises(ValueError):
        calculate_km_charge(100, 50, "TRUCK")

