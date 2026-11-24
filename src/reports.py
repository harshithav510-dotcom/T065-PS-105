
def print_trip_bill(
    booking_id,
    trip_price,
    late_fee,
    fuel_charge,
    km_charge,
    damage_charge,
    protection_fee=0,
    inconvenience_fee=0
):

    charges = [
        trip_price,
        late_fee,
        fuel_charge,
        km_charge,
        damage_charge,
        protection_fee,
        inconvenience_fee
    ]

    if any(amount < 0 for amount in charges):
        raise ValueError("Bill amounts cannot be negative.")

    total = sum(charges)

    print("\n========== TRIP BILL ==========")
    print("Booking ID:", booking_id)
    print("Trip Price: Rs.", trip_price)
    print("Late Fee: Rs.", late_fee)
    print("Inconvenience Fee: Rs.", inconvenience_fee)
    print("Fuel Charge: Rs.", fuel_charge)
    print("Extra KM Charge: Rs.", km_charge)
    print("Damage Liability: Rs.", damage_charge)
    print("Protection Fee: Rs.", protection_fee)
    print("-------------------------------")
    print("Total Amount: Rs.", total)
    print("===============================")

    return total


def print_deposit_ledger(amount_blocked, amount_deducted):

    if amount_blocked < 0 or amount_deducted < 0:
        raise ValueError("Deposit amounts cannot be negative.")

    refund = max(0, amount_blocked - amount_deducted)

    print("\n======= DEPOSIT LEDGER =======")
    print("Amount Blocked: Rs.", amount_blocked)
    print("Amount Deducted: Rs.", amount_deducted)
    print("Amount Refunded: Rs.", refund)
    print("==============================")

    return refund


def print_host_statement(host_name, total_payment):

    print("\n======= HOST STATEMENT =======")
    print("Host Name:", host_name)
    print("Total Payment: Rs.", total_payment)
    print("==============================")
