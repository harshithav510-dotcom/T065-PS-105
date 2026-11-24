
import pytest
from deposit import process_deposit


def test_normal_deposit_deduction():
    result = process_deposit(1500, 500, 400, 300, 200)

    assert result["amount_deducted"] == 1400
    assert result["refund"] == 100
    assert result["excess_claim"] == 0


def test_deposit_fully_deducted():
    result = process_deposit(1500, 500, 400, 300, 300)

    assert result["amount_deducted"] == 1500
    assert result["refund"] == 0


def test_excess_claim():
    result = process_deposit(1000, 500, 400, 300, 200)

    assert result["amount_deducted"] == 1000
    assert result["refund"] == 0
    assert result["excess_claim"] == 400


def test_negative_deposit():
    with pytest.raises(ValueError):
        process_deposit(-100, 0, 0, 0, 0)


def test_negative_charge():
    with pytest.raises(ValueError):
        process_deposit(1000, -100, 0, 0, 0)

