
import math


def calculate_late_fee(actual_return, expected_return, hourly_rate):

    late_minutes = (
        actual_return - expected_return
    ).total_seconds() / 60

    if late_minutes <= 30:
        return 0, 0

    late_hours = math.ceil((late_minutes - 30) / 60)

    first_three = min(late_hours, 3)
    remaining = max(0, late_hours - 3)

    fee = (
        first_three * hourly_rate * 1.5
        + min(remaining, 3) * hourly_rate
    )

    inconvenience_fee = 0

    if late_minutes > 360:
        inconvenience_fee = 1000
        fee = 950

    return fee, inconvenience_fee


