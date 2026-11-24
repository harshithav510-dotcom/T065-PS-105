
from settlement import calculate_final_settlement


def test_final_settlement_calculation():
    result = calculate_final_settlement(
        5000, 10, 300, 150, 1000
    )

    assert result["commission"] == 750
    assert result["damage_handling"] == 50
    assert result["host_payment"] == 4650


def test_final_settlement_zero_charges():
    result = calculate_final_settlement(
        1000, 10, 0, 0, 0
    )

    assert result["commission"] == 150
    assert result["damage_handling"] == 0
    assert result["host_payment"] == 850

