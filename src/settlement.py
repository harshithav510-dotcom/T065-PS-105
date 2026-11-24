
def calculate_commission_rate(completed_trips):

    if completed_trips < 10:
        return 0.20
    elif completed_trips < 50:
        return 0.15
    else:
        return 0.12


def calculate_host_settlement(
    trip_price, completed_trips, late_fee=0, fuel_charge=0
):

    commission_rate = calculate_commission_rate(completed_trips)
    commission = trip_price * commission_rate

    host_payment = (
        trip_price - commission
        - late_fee
        + fuel_charge
    )

    return commission, host_payment


def calculate_protection_fee(trip_price):

    if trip_price < 0:
        raise ValueError("Trip price cannot be negative.")

    return max(150, trip_price * 0.08)


def calculate_final_settlement(
    trip_price,
    completed_trips,
    late_fee=0,
    fuel_charge=0,
    damage_recovery=0
):

    values = [trip_price, late_fee, fuel_charge, damage_recovery]

    if any(value < 0 for value in values):
        raise ValueError("Settlement amounts cannot be negative.")

    commission_rate = calculate_commission_rate(completed_trips)
    commission = trip_price * commission_rate

    damage_handling = damage_recovery * 0.05

    host_payment = (
        trip_price
        - commission
        + late_fee
        + fuel_charge
        - damage_handling
    )

    return {
        "commission": commission,
        "damage_handling": damage_handling,
        "host_payment": host_payment
    }

