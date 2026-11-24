
from datetime import timedelta
import math


def check_extension(vehicle_id, current_booking_id, new_end_time, bookings):

    for booking in bookings:

        if (
            booking.vehicle_id == vehicle_id
            and booking.booking_id != current_booking_id
            and booking.status in ["BOOKED", "IN_PROGRESS"]
        ):

            time_difference = booking.start_time - new_end_time

            if timedelta(0) <= time_difference < timedelta(hours=2):
                return False, "Extension not allowed. Another booking starts within 2 hours."

    return True, "Extension allowed."


def calculate_extension_fee(new_end_time, requested_end_time, hourly_rate):

    extra_hours = (
        requested_end_time - new_end_time
    ).total_seconds() / 3600

    if extra_hours <= 0:
        raise ValueError("Extension time must be positive.")

    return math.ceil(extra_hours) * hourly_rate

