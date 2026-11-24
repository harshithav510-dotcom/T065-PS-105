def check_availability(vehicle_id, start_time, end_time, bookings):

    for booking in bookings:

        if (
            booking.vehicle_id == vehicle_id
            and booking.status in ["BOOKED", "IN_PROGRESS"]
        ):

            if (
                start_time < booking.end_time
                and end_time > booking.start_time
            ):
                return False, "Vehicle is already booked for this time."

    return True, "Vehicle is available."

