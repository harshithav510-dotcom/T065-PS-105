from datetime import datetime


def create_start_report(booking_id, odometer, fuel_level):

    if odometer < 0:
        raise ValueError("Invalid odometer reading.")

    if not 0 <= fuel_level <= 8:
        raise ValueError("Fuel must be between 0 and 8.")

    return {
        "booking_id": booking_id,
        "start_odometer": odometer,
        "start_fuel": fuel_level,
        "start_time": datetime.now()
    }


def create_end_report(
    booking_id, start_report, end_odometer,
    end_fuel, actual_return_time, damage_items=None
):

    if end_odometer < start_report["start_odometer"]:
        raise ValueError("End odometer cannot be less than start odometer.")

    if not 0 <= end_fuel <= 8:
        raise ValueError("Fuel must be between 0 and 8.")

    if damage_items is None:
        damage_items = []

    return {
        "booking_id": booking_id,
        "start_odometer": start_report["start_odometer"],
        "end_odometer": end_odometer,
        "distance_travelled": end_odometer - start_report["start_odometer"],
        "start_fuel": start_report["start_fuel"],
        "end_fuel": end_fuel,
        "actual_return_time": actual_return_time,
        "damage_items": damage_items
    }
