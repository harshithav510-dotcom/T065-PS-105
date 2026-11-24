import json
from datetime import date, datetime
from dataclasses import asdict
from models import Host, Guest, Vehicle, Booking
from storage import json_serializer, json_deserializer


def test_datetime_serialization():
    value = datetime(2026, 11, 5, 10, 0)

    serialized = json_serializer(value)
    restored = json_deserializer(serialized)

    assert restored == value


def test_date_serialization():
    value = date(2027, 12, 31)

    serialized = json_serializer(value)
    restored = json_deserializer(serialized)

    assert restored == value


def test_model_data_serialization():
    host = Host("H001", "Rahul")
    guest = Guest("G001", "Arun", 22, date(2027, 12, 31), 85)

    data = json.dumps(
        {"host": asdict(host), "guest": asdict(guest)},
        default=json_serializer
    )

    restored = json.loads(data, object_hook=json_deserializer)

    assert restored["host"]["host_id"] == "H001"
    assert restored["guest"]["guest_id"] == "G001"
    assert restored["guest"]["licence_valid_until"] == date(2027, 12, 31)

