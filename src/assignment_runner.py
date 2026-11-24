
import csv
import math
from pathlib import Path
from datetime import datetime, date, timedelta


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "T065-PS-105-sample-data"
COMMAND_FILE = DATA_DIR / "commands.txt"


def money(value):
    return round(float(value) + 0.0000001, 2)


def parse_time(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def read_csv(filename):
    with (DATA_DIR / filename).open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        return list(csv.DictReader(file))


def write_csv(filename, columns, rows):
    with (ROOT / filename).open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def calculate_age(dob, at_time):
    return (
        at_time.year - dob.year
        - ((at_time.month, at_time.day) < (dob.month, dob.day))
    )


def load_project_data():
    hosts = {
        r["host_id"]: {
            "name": r["host_name"],
            "city": r["city"],
            "completed_trips": int(r["completed_trips_before"]),
            "gross": 0.0,
            "commission": 0.0,
            "penalties": 0.0,
        }
        for r in read_csv("hosts.csv")
    }

    vehicles = {
        r["vehicle_id"]: {
            "host_id": r["host_id"],
            "type": r["vehicle_type"],
            "segment": r["segment"],
            "model": r["model"],
            "hourly_rate": float(r["hourly_rate"]),
            "daily_rate": float(r["daily_rate"]),
            "city": r["home_city"],
        }
        for r in read_csv("vehicles.csv")
    }

    guests = {
        r["guest_id"]: {
            "name": r["guest_name"],
            "dob": date.fromisoformat(r["dob"]),
            "licence_expiry": date.fromisoformat(r["licence_expiry"]),
            "trust_score": int(r["trust_score"]),
            "open_damage_claim": r["open_damage_claim"].lower() == "true",
        }
        for r in read_csv("guests.csv")
    }

    damage_rates = {
        r["item_code"]: float(r["assessed_amount"])
        for r in read_csv("damage_rate_card.csv")
    }

    return hosts, vehicles, guests, damage_rates


def calculate_deposit(segment, trust_score):
    amounts = {
        "HATCHBACK": 3000,
        "SEDAN": 5000,
        "SUV": 8000,
        "LUXURY": 20000,
        "BIKE": 1000,
    }

    amount = amounts.get(segment, 3000)

    if trust_score >= 80:
        amount *= 0.5

    return money(amount)


def calculate_duration(start, end, vehicle):
    hours = (end - start).total_seconds() / 3600

    if hours <= 0:
        raise ValueError("Invalid trip duration")

    if hours > 24:
        days = math.ceil(hours / 24)
        return money(days * vehicle["daily_rate"]), "DAILY"

    hourly_price = math.ceil(hours) * vehicle["hourly_rate"]
    daily_price = vehicle["daily_rate"]

    if hourly_price <= daily_price:
        return money(hourly_price), "HOURLY"

    return money(daily_price), "DAILY"


def weekend_surcharge(start, end, vehicle):
    surcharge = 0.0
    current = start.date()

    while current <= end.date():
        if current.weekday() == 4:
            weekend_start = datetime.combine(
                current, datetime.min.time()
            ).replace(hour=18)

            weekend_end = weekend_start + timedelta(
                days=2, hours=12
            )

            overlap_start = max(start, weekend_start)
            overlap_end = min(end, weekend_end)

            if overlap_end > overlap_start:
                hours = (
                    overlap_end - overlap_start
                ).total_seconds() / 3600

                surcharge += (
                    hours * vehicle["hourly_rate"] * 0.20
                )

        current += timedelta(days=1)

    return money(surcharge)


def check_eligibility(guest, vehicle, start, end, booking_time):
    if end <= start:
        return False, "Invalid trip duration."

    age = calculate_age(guest["dob"], booking_time)
    minimum_age = 18 if vehicle["type"] == "BIKE" else 21

    if age < minimum_age:
        return False, "Minimum age requirement not met."

    if guest["licence_expiry"] < end.date() + timedelta(days=1):
        return False, "Licence must be valid through one day after trip end."

    if (
        vehicle["segment"] == "LUXURY"
        and guest["trust_score"] < 40
    ):
        return False, "Trust score too low for luxury vehicle."

    if guest["open_damage_claim"]:
        return False, "Guest has an open damage claim."

    return True, "Booking successful."


def check_availability(vehicle_id, start, end, bookings):
    for booking in bookings.values():
        if (
            booking["vehicle_id"] == vehicle_id
            and booking["status"] in ("BOOKED", "IN_PROGRESS")
            and start < booking["end"]
            and end > booking["start"]
        ):
            return False

    return True


def calculate_km_charge(distance, allowed_km, segment):
    rates = {
        "HATCHBACK": 8,
        "SEDAN": 12,
        "SUV": 12,
        "LUXURY": 20,
        "BIKE": 3,
    }

    excess = max(0, distance - allowed_km)
    return excess, money(excess * rates[segment])


def calculate_fuel_charge(start_fuel, end_fuel, vehicle_type):
    shortage = max(0, start_fuel - end_fuel)
    rate = 150 if vehicle_type == "BIKE" else 600
    return money(shortage * rate)


def calculate_late_charge(actual_return, expected_return, hourly_rate):
    late_minutes = max(
        0,
        math.ceil(
            (actual_return - expected_return).total_seconds() / 60
        )
    )

    if late_minutes <= 30:
        return late_minutes, 0.0

    chargeable_hours = math.ceil((late_minutes - 30) / 60)

    first_hours = min(chargeable_hours, 3)
    next_hours = min(max(chargeable_hours - 3, 0), 3)

    late_charge = (
        first_hours * hourly_rate * 1.5
        + next_hours * hourly_rate * 2
    )

    if late_minutes > 360:
        late_charge += 1000

    return late_minutes, money(late_charge)


def calculate_commission(completed_trips):
    if completed_trips < 10:
        return 20.0
    if completed_trips < 50:
        return 15.0
    return 12.0


def calculate_damage_charge(damage_items, deposit, protection):
    assessed = sum(damage_items)

    if protection:
        assessed = min(assessed, 1500)

    # Damage liability is not capped by the deposit.
    # The deposit limits only how much can be deducted.
    return money(assessed)


def process_assignment():
    hosts, vehicles, guests, damage_rates = load_project_data()

    bookings = {}
    quotes = []
    bills = []
    settlements = []
    statements = []

    for line_number, raw_line in enumerate(
        COMMAND_FILE.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split("|")
        command = parts[0].upper()

        try:
            if command == "BOOK":
                (
                    _, ts, booking_id, guest_id, vehicle_id,
                    start_ts, end_ts, protection
                ) = parts

                booking_time = parse_time(ts)
                start = parse_time(start_ts)
                end = parse_time(end_ts)
                protected = protection.lower() == "true"

                guest = guests.get(guest_id)
                vehicle = vehicles.get(vehicle_id)

                status = "REJECTED"
                mode = ""
                duration_charge = 0.0
                deposit = 0.0
                protection_fee = 0.0
                message = "Guest or vehicle not found."

                if guest and vehicle:
                    eligible, message = check_eligibility(
                        guest, vehicle, start, end, booking_time
                    )

                    if eligible and not check_availability(
                        vehicle_id, start, end, bookings
                    ):
                        eligible = False
                        message = "Vehicle is already booked."

                    if eligible:
                        duration_charge, mode = calculate_duration(
                            start, end, vehicle
                        )

                        duration_charge = money(
                            duration_charge
                            + weekend_surcharge(start, end, vehicle)
                        )

                        deposit = calculate_deposit(
                            vehicle["segment"],
                            guest["trust_score"],
                        )

                        if protected:
                            protection_fee = max(
                                150,
                                money(duration_charge * 0.08),
                            )

                        status = "BOOKED"
                        message = "Booking successful."

                        bookings[booking_id] = {
                            "guest_id": guest_id,
                            "vehicle_id": vehicle_id,
                            "host_id": vehicle["host_id"],
                            "start": start,
                            "end": end,
                            "status": "BOOKED",
                            "protection": protected,
                            "duration_charge": duration_charge,
                            "deposit": deposit,
                            "protection_fee": protection_fee,
                            "damage": [],
                            "start_report": None,
                            "end_report": None,
                            "extension_charge": 0.0,
                        }

                quotes.append({
                    "booking_id": booking_id,
                    "status": status,
                    "pricing_mode": mode,
                    "duration_charge": money(duration_charge),
                    "deposit_blocked": money(deposit),
                    "protection_fee": money(protection_fee),
                    "message": message,
                })

            elif command == "CANCEL_BOOKING":
                _, ts, booking_id, cancelled_by = parts
                booking = bookings.get(booking_id)

                if booking and booking["status"] == "BOOKED":
                    cancellation_time = parse_time(ts)

                    hours_before = (
                        booking["start"] - cancellation_time
                    ).total_seconds() / 3600

                    if cancelled_by == "HOST":
                        if hours_before < 24:
                            hosts[booking["host_id"]]["penalties"] += 1000

                        booking["status"] = "CANCELLED"

                    elif cancelled_by == "GUEST":
                        booking["status"] = "CANCELLED"

            elif command == "START_TRIP":
                _, ts, booking_id, odometer, fuel = parts
                booking = bookings.get(booking_id)

                if booking and booking["status"] == "BOOKED":
                    odometer = float(odometer)
                    fuel = int(fuel)

                    if odometer >= 0 and 0 <= fuel <= 8:
                        booking["start_report"] = {
                            "odometer": odometer,
                            "fuel": fuel,
                            "time": parse_time(ts),
                        }
                        booking["status"] = "IN_PROGRESS"

            elif command == "EXTEND":
                _, ts, booking_id, new_end_ts = parts
                booking = bookings.get(booking_id)

                if booking and booking["status"] == "IN_PROGRESS":
                    new_end = parse_time(new_end_ts)

                    if new_end > booking["end"]:
                        blocked = False

                        for key, other in bookings.items():
                            if key == booking_id:
                                continue

                            if (
                                other["vehicle_id"] == booking["vehicle_id"]
                                and other["status"] in (
                                    "BOOKED", "IN_PROGRESS"
                                )
                            ):
                                gap = (
                                    other["start"] - new_end
                                ).total_seconds() / 3600

                                if 0 <= gap < 2:
                                    blocked = True
                                    break

                                if (
                                    other["start"] < new_end
                                    and other["end"] > booking["end"]
                                ):
                                    blocked = True
                                    break

                        if not blocked:
                            vehicle = vehicles[booking["vehicle_id"]]
                            extra_hours = math.ceil(
                                (new_end - booking["end"]).total_seconds()
                                / 3600
                            )

                            booking["extension_charge"] += money(
                                extra_hours * vehicle["hourly_rate"]
                            )
                            booking["end"] = new_end

            elif command == "END_TRIP":
                _, ts, booking_id, odometer, fuel, return_ts = parts
                booking = bookings.get(booking_id)

                if booking and booking["status"] == "IN_PROGRESS":
                    start_report = booking["start_report"]
                    odometer = float(odometer)
                    fuel = int(fuel)

                    if (
                        odometer >= start_report["odometer"]
                        and 0 <= fuel <= 8
                    ):
                        booking["end_report"] = {
                            "odometer": odometer,
                            "fuel": fuel,
                            "return_time": parse_time(return_ts),
                        }
                        booking["status"] = "RETURNED"

            elif command == "DAMAGE_REPORT":
                _, ts, booking_id, item_code, photo = parts
                booking = bookings.get(booking_id)

                if (
                    booking
                    and booking["status"] == "RETURNED"
                    and booking["end_report"]
                ):
                    report_time = parse_time(ts)
                    return_time = booking["end_report"]["return_time"]

                    valid_time = (
                        timedelta(0)
                        <= report_time - return_time
                        <= timedelta(hours=24)
                    )

                    if (
                        valid_time
                        and photo.lower() == "true"
                        and item_code in damage_rates
                    ):
                        booking["damage"].append(
                            damage_rates[item_code]
                        )

            elif command == "SETTLE":
                _, ts, booking_id = parts
                booking = bookings.get(booking_id)

                if (
                    not booking
                    or booking["status"] != "RETURNED"
                    or not booking["end_report"]
                ):
                    continue

                vehicle = vehicles[booking["vehicle_id"]]
                host = hosts[booking["host_id"]]

                start_report = booking["start_report"]
                end_report = booking["end_report"]

                distance = (
                    end_report["odometer"] - start_report["odometer"]
                )

                duration_hours = (
                    booking["end"] - booking["start"]
                ).total_seconds() / 3600

                if duration_hours > 24:
                    allowed_km = 300 * math.ceil(duration_hours / 24)
                else:
                    allowed_km = 15 * math.ceil(duration_hours)

                excess_km, excess_km_charge = calculate_km_charge(
                    distance,
                    allowed_km,
                    vehicle["segment"],
                )

                late_minutes, late_charge = calculate_late_charge(
                    end_report["return_time"],
                    booking["end"],
                    vehicle["hourly_rate"],
                )

                fuel_charge = calculate_fuel_charge(
                    start_report["fuel"],
                    end_report["fuel"],
                    vehicle["type"],
                )

                damage_charge = calculate_damage_charge(
                    booking["damage"],
                    booking["deposit"],
                    booking["protection"],
                )

                duration_charge = money(
                    booking["duration_charge"]
                    + booking["extension_charge"]
                )

                protection_fee = booking["protection_fee"]

                total = money(
                    duration_charge
                    + excess_km_charge
                    + late_charge
                    + fuel_charge
                    + damage_charge
                    + protection_fee
                )

                remaining = booking["deposit"]
                deposit_deducted = 0.0

                for charge in (
                    late_charge,
                    fuel_charge,
                    excess_km_charge,
                    damage_charge,
                ):
                    deduction = min(remaining, charge)
                    remaining -= deduction
                    deposit_deducted += deduction

                deposit_deducted = money(deposit_deducted)
                deposit_refund = money(
                    booking["deposit"] - deposit_deducted
                )

                other_charges = (
                    late_charge
                    + fuel_charge
                    + excess_km_charge
                    + damage_charge
                )

                claim_raised = (
                    "true"
                    if other_charges > booking["deposit"]
                    else "false"
                )

                bills.append({
                    "booking_id": booking_id,
                    "duration_charge": money(duration_charge),
                    "excess_km": money(excess_km),
                    "excess_km_charge": money(excess_km_charge),
                    "late_minutes": late_minutes,
                    "late_charge": money(late_charge),
                    "fuel_charge": money(fuel_charge),
                    "damage_charge": money(damage_charge),
                    "protection_fee": money(protection_fee),
                    "total": money(total),
                    "deposit_deducted": deposit_deducted,
                    "deposit_refund": deposit_refund,
                    "claim_raised": claim_raised,
                })

                commission_pct = calculate_commission(
                    host["completed_trips"]
                )

                trip_price = money(
                    duration_charge + protection_fee
                )

                commission = money(
                    trip_price * commission_pct / 100
                )

                late_fuel_passthrough = money(
                    late_charge + fuel_charge
                )

                # Assumed 5% damage-handling deduction.
                damage_recovery = money(damage_charge * 0.95)

                host_payout = money(
                    trip_price
                    - commission
                    + late_fuel_passthrough
                    + damage_recovery
                )

                settlements.append({
                    "booking_id": booking_id,
                    "host_id": booking["host_id"],
                    "trip_price": money(trip_price),
                    "commission_pct": commission_pct,
                    "commission": money(commission),
                    "late_fuel_passthrough": money(
                        late_fuel_passthrough
                    ),
                    "damage_recovery": money(damage_recovery),
                    "host_payout": money(host_payout),
                })

                host["gross"] += trip_price
                host["commission"] += commission
                host["completed_trips"] += 1

                booking["status"] = "SETTLED"

            elif command == "HOST_STATEMENT":
                _, ts, host_id = parts
                host = hosts.get(host_id)

                if host:
                    statements.append({
                        "host_id": host_id,
                        "completed_trips": host["completed_trips"],
                        "gross": money(host["gross"]),
                        "commission": money(host["commission"]),
                        "penalties": money(host["penalties"]),
                        "net": money(
                            host["gross"]
                            - host["commission"]
                            - host["penalties"]
                        ),
                    })

        except (ValueError, KeyError, IndexError) as error:
            print(
                f"Skipped invalid command at line {line_number}: {error}"
            )

    write_csv(
        "quotes.csv",
        [
            "booking_id", "status", "pricing_mode",
            "duration_charge", "deposit_blocked",
            "protection_fee", "message",
        ],
        quotes,
    )

    write_csv(
        "bills.csv",
        [
            "booking_id", "duration_charge", "excess_km",
            "excess_km_charge", "late_minutes", "late_charge",
            "fuel_charge", "damage_charge", "protection_fee",
            "total", "deposit_deducted", "deposit_refund",
            "claim_raised",
        ],
        bills,
    )

    write_csv(
        "host_settlements.csv",
        [
            "booking_id", "host_id", "trip_price",
            "commission_pct", "commission",
            "late_fuel_passthrough", "damage_recovery",
            "host_payout",
        ],
        settlements,
    )

    write_csv(
        "host_statements.csv",
        [
            "host_id", "completed_trips", "gross",
            "commission", "penalties", "net",
        ],
        statements,
    )

    print("\nAssignment processing completed.")
    print("Quotes:", len(quotes))
    print("Bills:", len(bills))
    print("Host settlements:", len(settlements))
    print("Host statements:", len(statements))
    print("Generated CSV files in:", ROOT)


if __name__ == "__main__":
    process_assignment()
