
import json
import os
from dataclasses import asdict
from datetime import date, datetime

DATA_FILE = "project_data.json"


def json_serializer(value):
    if isinstance(value, datetime):
        return {
            "__type__": "datetime",
            "value": value.isoformat()
        }

    if isinstance(value, date):
        return {
            "__type__": "date",
            "value": value.isoformat()
        }

    raise TypeError(f"Cannot serialize {type(value).__name__}")


def json_deserializer(data):
    if data.get("__type__") == "datetime":
        return datetime.fromisoformat(data["value"])

    if data.get("__type__") == "date":
        return date.fromisoformat(data["value"])

    return data


def save_data(
    hosts, guests, vehicles, bookings,
    start_reports=None,
    end_reports=None,
    booking_details_store=None,
    cancellation_records=None,
    deposit_release_records=None
):
    data = {
        "hosts": [asdict(h) for h in hosts],
        "guests": [asdict(g) for g in guests],
        "vehicles": [asdict(v) for v in vehicles],
        "bookings": [asdict(b) for b in bookings],
        "start_reports": start_reports or {},
        "end_reports": end_reports or {},
        "booking_details_store": booking_details_store or {},
        "cancellation_records": cancellation_records or {},
        "deposit_release_records": deposit_release_records or {}
    }

    with open(DATA_FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=4,
            default=json_serializer
        )


def load_data():
    from models import Host, Guest, Vehicle, Booking

    if not os.path.exists(DATA_FILE):
        return [], [], [], [], {}, {}, {}, {}, {}

    with open(DATA_FILE, "r") as file:
        data = json.load(file, object_hook=json_deserializer)

    hosts = [
        Host(**item) for item in data.get("hosts", [])
    ]

    guests = [
        Guest(**item) for item in data.get("guests", [])
    ]

    vehicles = [
        Vehicle(**item) for item in data.get("vehicles", [])
    ]

    bookings = [
        Booking(**item) for item in data.get("bookings", [])
    ]

    return (
        hosts,
        guests,
        vehicles,
        bookings,
        data.get("start_reports", {}),
        data.get("end_reports", {}),
        data.get("booking_details_store", {}),
        data.get("cancellation_records", {}),
        data.get("deposit_release_records", {})
    )

