def calculate_guest_refund(trip_price, hours_before_start):

    if trip_price < 0:
        raise ValueError("Trip price cannot be negative.")

    if hours_before_start > 48:
        percentage = 100

    elif hours_before_start >= 24:
        percentage = 75

    elif hours_before_start > 0:
        percentage = 50

    else:
        percentage = 0

    return trip_price * percentage / 100


def calculate_host_cancellation(hours_before_start):

    guest_credit = 500
    host_penalty = 0

    if hours_before_start < 24:
        host_penalty = 1000

    return guest_credit, host_penalty

