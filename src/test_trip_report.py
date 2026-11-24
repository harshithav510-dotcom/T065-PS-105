from datetime import datetime
from trip_report import create_start_report, create_end_report


def test_create_start_report():
    report = create_start_report("B001", 10000, 8)

    assert report["booking_id"] == "B001"
    assert report["start_odometer"] == 10000
    assert report["start_fuel"] == 8


def test_create_end_report():
    start_report = create_start_report("B001", 10000, 8)

    report = create_end_report(
        "B001",
        start_report,
        10100,
        7,
        datetime(2026, 11, 5, 15, 0),
        ["Scratch on door"]
    )

    assert report["booking_id"] == "B001"
    assert report["distance_travelled"] == 100
    assert report["end_odometer"] == 10100
    assert report["end_fuel"] == 7
    assert report["damage_items"] == ["Scratch on door"]
