from settlement import calculate_host_settlement


def test_host_settlement():
    commission, payment = calculate_host_settlement(
        5000, 5, 300, 150
    )

    assert commission == 1000
    assert payment == 3850


def test_zero_charges_settlement():
    commission, payment = calculate_host_settlement(
        1000, 5, 0, 0
    )

    assert commission == 200
    assert payment == 800
