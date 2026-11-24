from eligibility import check_eligibility
from availability import check_availability
from pricing import calculate_duration_price, calculate_weekend_price
from deposit import calculate_deposit
from settlement import calculate_protection_fee


def create_booking(guest, vehicle, start_time, end_time, bookings, protection=False):

    eligible, message = check_eligibility(
        guest, vehicle, start_time, end_time
    )

    if not eligible:
        return None, message

    available, message = check_availability(
        vehicle.vehicle_id, start_time, end_time, bookings
    )

    if not available:
        return None, message

    trip_price = calculate_duration_price(
        start_time, end_time,
        vehicle.hourly_rate, vehicle.daily_rate
    )

    trip_price = calculate_weekend_price(
        trip_price,
        start_time,
        end_time,
        vehicle.hourly_rate
    )

    deposit = calculate_deposit(
        vehicle.segment, guest.trust_score
    )

    protection_fee = 0

    if protection:
        protection_fee = calculate_protection_fee(trip_price)

    return {
        "trip_price": trip_price,
        "deposit": deposit,
        "protection": protection,
        "protection_fee": protection_fee,
        "status": "BOOKED"
    }, "Booking successful."
