from reports import print_trip_bill


def test_trip_bill_total():
    total = print_trip_bill(
        "B001",
        5000,
        300,
        150,
        100,
        0,
        400,
        1000
    )

    assert total == 6950

