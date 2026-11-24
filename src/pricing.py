import math
from datetime import datetime, timedelta, time


def calculate_duration_price(start_time, end_time, hourly_rate, daily_rate):

    duration_hours = (
        end_time - start_time
    ).total_seconds() / 3600

    if duration_hours <= 0:
        raise ValueError("End time must be after start time.")

    hours = math.ceil(duration_hours)

    if duration_hours > 24:
        days = math.ceil(duration_hours / 24)
        return days * daily_rate

    hourly_price = hours * hourly_rate
    daily_price = daily_rate

    return min(hourly_price, daily_price)


def calculate_weekend_price(price, start_time, end_time, hourly_rate):

    current_date = start_time.date()
    weekend_hours = 0

    while current_date <= end_time.date():

        if current_date.weekday() == 4:

            weekend_start = datetime.combine(
                current_date, time(18, 0)
            )

            weekend_end = weekend_start + timedelta(
                days=2, hours=12
            )

            overlap_start = max(start_time, weekend_start)
            overlap_end = min(end_time, weekend_end)

            if overlap_end > overlap_start:
                weekend_hours += (
                    overlap_end - overlap_start
                ).total_seconds() / 3600

        current_date += timedelta(days=1)

    if end_time <= start_time:
        raise ValueError("Invalid trip duration.")

    weekend_surcharge = weekend_hours * hourly_rate * 0.20

    return price + weekend_surcharge


def calculate_km_charge(distance, allowed_km, segment):

    rates = {
        "HATCHBACK": 8,
        "SEDAN": 12,
        "SUV": 12,
        "LUXURY": 20,
        "BIKE": 3
    }

    if distance < 0 or allowed_km < 0:
        raise ValueError("Distance and allowance cannot be negative.")

    segment = segment.upper()

    if segment not in rates:
        raise ValueError("Invalid vehicle segment.")

    excess_km = max(0, distance - allowed_km)

    return excess_km * rates[segment]




