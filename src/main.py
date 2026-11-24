
import json
from pathlib import Path
from datetime import datetime, date

from reports import print_trip_bill
from registration import register_host, register_guest, register_vehicle
from booking import create_booking
from models import Booking
from trip_report import create_start_report, create_end_report
from pricing import calculate_km_charge
from fuel import calculate_fuel_charge
from trip_manager import calculate_late_fee
from damage import calculate_damage_charge
from deposit import process_deposit, check_deposit_release
from settlement import calculate_final_settlement
from cancellation import calculate_guest_refund, calculate_host_cancellation
from extension import check_extension, calculate_extension_fee
from storage import save_data, load_data


(
    hosts,
    guests,
    vehicles,
    bookings,
    start_reports,
    end_reports,
    booking_details_store,
    cancellation_records,
    deposit_release_records
) = load_data()


def save_project_data():
    save_data(
        hosts,
        guests,
        vehicles,
        bookings,
        start_reports,
        end_reports,
        booking_details_store,
        cancellation_records,
        deposit_release_records
    )


def process_command(command):

    action = command["action"].upper()

    if action == "REGISTER_HOST":

        host = register_host(hosts, command["host_id"], command["name"])

        if host:
            print("Host registered:", host.name)
            save_project_data()

    elif action == "REGISTER_GUEST":

        guest = register_guest(
            guests,
            command["guest_id"],
            command["name"],
            command["age"],
            date.fromisoformat(command["licence_valid_until"]),
            command["trust_score"]
        )

        if guest:
            print("Guest registered:", guest.name)
            save_project_data()

    elif action == "REGISTER_VEHICLE":

        vehicle = register_vehicle(
            vehicles,
            command["vehicle_id"],
            command["host_id"],
            command["vehicle_type"],
            command["segment"],
            command["hourly_rate"],
            command["daily_rate"],
            command["city"],
            command.get("km_allowance", 0)
        )

        if vehicle:
            print("Vehicle registered:", vehicle.vehicle_id)
            save_project_data()

    elif action == "BOOK":

        guest = next(
            (g for g in guests if g.guest_id == command["guest_id"]),
            None
        )

        vehicle = next(
            (v for v in vehicles if v.vehicle_id == command["vehicle_id"]),
            None
        )

        if guest is None or vehicle is None:
            print("Guest or vehicle not found.")
            return

        if guest.open_damage_claim:
            print("Booking rejected: Guest has an unpaid damage claim.")
            return

        start = datetime.fromisoformat(command["start_time"])
        end = datetime.fromisoformat(command["end_time"])

        protection = command.get("protection", False)

        details, message = create_booking(
            guest, vehicle, start, end, bookings, protection
        )

        print(message)

        if details:
            booking_id = f"B{len(bookings) + 1:03d}"

            booking = Booking(
                booking_id,
                guest.guest_id,
                vehicle.vehicle_id,
                start,
                end
            )

            bookings.append(booking)
            booking_details_store[booking_id] = details

            print("Booking ID:", booking_id)
            print("Booking details:", details)

            save_project_data()

    elif action == "START_TRIP":

        booking_id = command["booking_id"]

        booking = next(
            (b for b in bookings if b.booking_id == booking_id),
            None
        )

        if booking is None or booking.status != "BOOKED":
            print("Valid booking not found.")
            return

        start_reports[booking_id] = create_start_report(
            booking_id,
            command["odometer"],
            command["fuel"]
        )

        booking.status = "IN_PROGRESS"

        print("Trip started:", booking_id)
        save_project_data()

    elif action == "END_TRIP":

        booking_id = command["booking_id"]

        booking = next(
            (b for b in bookings if b.booking_id == booking_id),
            None
        )

        if booking is None or booking.status != "IN_PROGRESS":
            print("Active trip not found.")
            return

        if booking_id not in start_reports:
            print("Start report not found.")
            return

        vehicle = next(
            (v for v in vehicles if v.vehicle_id == booking.vehicle_id),
            None
        )

        host = next(
            (h for h in hosts if h.host_id == vehicle.host_id),
            None
        ) if vehicle else None

        guest = next(
            (g for g in guests if g.guest_id == booking.guest_id),
            None
        )

        if vehicle is None or host is None or guest is None:
            print("Vehicle, host or guest record not found.")
            return

        return_time = datetime.fromisoformat(
            command["actual_return_time"]
        )

        report = create_end_report(
            booking_id,
            start_reports[booking_id],
            command["end_odometer"],
            command["end_fuel"],
            return_time,
            command.get("damage_items", [])
        )

        end_reports[booking_id] = report

        distance = report["distance_travelled"]

        duration_hours = (
            booking.end_time - booking.start_time
        ).total_seconds() / 3600

        if duration_hours > 24:
            allowed_km = 300 * int((duration_hours + 23.999999) // 24)
        else:
            allowed_km = 15 * int((duration_hours + 0.999999) // 1)

        km_charge = calculate_km_charge(
            distance,
            allowed_km,
            vehicle.segment
        )

        fuel_charge = calculate_fuel_charge(
            report["start_fuel"],
            report["end_fuel"],
            vehicle.vehicle_type
        )

        late_fee, inconvenience_fee = calculate_late_fee(
            return_time,
            booking.end_time,
            vehicle.hourly_rate
        )

        damage_cost = sum(
            item.get("cost", 0)
            for item in report["damage_items"]
        )

        details = booking_details_store[booking_id]

        deposit_amount = details["deposit"]
        protection = details["protection"]
        protection_fee = details["protection_fee"]

        damage_charge = calculate_damage_charge(
            damage_cost,
            deposit_amount,
            protection
        )

        deposit_result = process_deposit(
            deposit_amount,
            late_fee + inconvenience_fee,
            fuel_charge,
            km_charge,
            damage_charge
        )

        if deposit_result["excess_claim"] > 0:
            guest.open_damage_claim = True
            print("WARNING: Guest blocked due to unpaid claim.")

        deposit_release_records[booking_id] = {
            "completion_time": return_time,
            "refund_amount": deposit_result["refund"],
            "released": False
        }

        duration_price = details["trip_price"]
        trip_price = duration_price + km_charge

        actual_damage_recovery = deposit_result["deductions"]["Damage Charge"]

        settlement = calculate_final_settlement(
            trip_price,
            host.completed_trips,
            late_fee + inconvenience_fee,
            fuel_charge,
            actual_damage_recovery
        )

        host.completed_trips += 1
        booking.status = "COMPLETED"

        print("\n----- FINAL TRIP BILL -----")
        print("Distance:", distance, "km")
        print("Allowed KM:", allowed_km)

        print_trip_bill(
            booking_id,
            duration_price,
            late_fee,
            fuel_charge,
            km_charge,
            0,
            protection_fee,
            inconvenience_fee
        )

        print("Protection selected:", protection)
        print("Damage cost:", damage_cost)
        print("Damage liability: Rs.", damage_charge)
        print("Deposit deducted: Rs.", deposit_result["amount_deducted"])
        print("Deposit refund pending: Rs.", deposit_result["refund"])
        print("Extra claim: Rs.", deposit_result["excess_claim"])
        print("Deposit release date:", return_time.date())

        print("\n----- HOST SETTLEMENT -----")
        print("Commission: Rs.", settlement["commission"])
        print("Damage handling: Rs.", settlement["damage_handling"])
        print("Host payment: Rs.", settlement["host_payment"])
        print("Completed trips:", host.completed_trips)

        save_project_data()

    elif action == "RELEASE_DEPOSIT":

        booking_id = command["booking_id"]

        record = deposit_release_records.get(booking_id)

        if record is None:
            print("Deposit record not found.")
            return

        if record["released"]:
            print("Deposit has already been released.")
            return

        booking = next(
            (b for b in bookings if b.booking_id == booking_id),
            None
        )

        if booking is None:
            print("Booking not found.")
            return

        guest = next(
            (g for g in guests if g.guest_id == booking.guest_id),
            None
        )

        if guest is None:
            print("Guest not found.")
            return

        current_time = (
            datetime.fromisoformat(command["current_time"])
            if "current_time" in command
            else datetime.now()
        )

        allowed, message = check_deposit_release(
            record["completion_time"],
            current_time,
            guest.open_damage_claim
        )

        print(message)

        if allowed:
            record["released"] = True
            print("Released deposit amount: Rs.", record["refund_amount"])
            save_project_data()

    elif action in ["GUEST_CANCEL", "HOST_CANCEL"]:

        booking_id = command["booking_id"]

        booking = next(
            (b for b in bookings if b.booking_id == booking_id),
            None
        )

        if booking is None or booking.status != "BOOKED":
            print("Active booking not found.")
            return

        hours_before_start = (
            booking.start_time - datetime.now()
        ).total_seconds() / 3600

        trip_price = booking_details_store[booking_id]["trip_price"]

        vehicle = next(
            (v for v in vehicles if v.vehicle_id == booking.vehicle_id),
            None
        )

        host = next(
            (h for h in hosts if h.host_id == vehicle.host_id),
            None
        ) if vehicle else None

        if vehicle is None or host is None:
            print("Vehicle or host not found.")
            return

        if action == "GUEST_CANCEL":

            refund = calculate_guest_refund(
                trip_price,
                hours_before_start
            )

            cancellation_records[booking_id] = {
                "type": "GUEST_CANCEL",
                "refund": refund
            }

            print("Guest refund: Rs.", refund)

        else:

            guest_credit, host_penalty = calculate_host_cancellation(
                hours_before_start
            )

            if host_penalty > 0:
                host.rank -= 1

            cancellation_records[booking_id] = {
                "type": "HOST_CANCEL",
                "guest_credit": guest_credit,
                "host_penalty": host_penalty
            }

            print("Full guest refund: Rs.", trip_price)
            print("Guest credit: Rs.", guest_credit)
            print("Host penalty: Rs.", host_penalty)

        booking.status = "CANCELLED"

        print("Booking status: CANCELLED")
        save_project_data()

    elif action == "EXTEND_TRIP":

        booking_id = command["booking_id"]

        booking = next(
            (b for b in bookings if b.booking_id == booking_id),
            None
        )

        if booking is None or booking.status != "IN_PROGRESS":
            print("Active trip not found.")
            return

        vehicle = next(
            (v for v in vehicles if v.vehicle_id == booking.vehicle_id),
            None
        )

        if vehicle is None:
            print("Vehicle not found.")
            return

        requested_end = datetime.fromisoformat(
            command["new_end_time"]
        )

        allowed, message = check_extension(
            booking.vehicle_id,
            booking_id,
            requested_end,
            bookings
        )

        print(message)

        if not allowed:
            return

        fee = calculate_extension_fee(
            booking.end_time,
            requested_end,
            vehicle.hourly_rate
        )

        booking.end_time = requested_end

        print("Extension successful.")
        print("Extension fee: Rs.", fee)
        print("New return time:", booking.end_time)

        save_project_data()

    else:
        print("Unknown command:", action)


def main():

    commands_path = Path(__file__).resolve().parent.parent / "commands.txt"

    try:
        with open(commands_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    command = json.loads(line)
                    process_command(command)

                except (json.JSONDecodeError, KeyError, ValueError) as error:
                    print(f"Command error on line {line_number}: {error}")

    except FileNotFoundError:
        print("commands.txt file not found.")

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()











