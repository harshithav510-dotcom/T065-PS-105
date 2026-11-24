
from datetime import datetime, timedelta


class Deposit:

    def __init__(self, amount):
        if amount < 0:
            raise ValueError("Deposit cannot be negative.")

        self.amount = amount
        self.status = "ON HOLD"
        self.damage_found = False
        self.release_date = datetime.now() + timedelta(days=3)

    def complete_trip(self, damage_found):
        self.damage_found = damage_found

        if damage_found:
            self.status = "ON HOLD"
        else:
            self.status = "PENDING RELEASE"

    def release_deposit(self):

        if self.damage_found:
            self.status = "ON HOLD"
            print("Deposit cannot be released due to damage claim.")

        elif datetime.now() < self.release_date:
            self.status = "ON HOLD"
            print("Deposit is not ready for release.")

        else:
            self.status = "RELEASED"
            print("Deposit released successfully.")


def calculate_deposit(segment, trust_score):

    deposits = {
        "HATCHBACK": 3000,
        "SEDAN": 5000,
        "SUV": 8000,
        "LUXURY": 20000,
        "BIKE": 1000
    }

    segment = segment.upper()

    if segment not in deposits:
        raise ValueError("Invalid vehicle segment.")

    amount = deposits[segment]

    if trust_score >= 80:
        amount = amount / 2

    return amount


def process_deposit(
    deposit_amount,
    late_fee,
    fuel_charge,
    km_charge,
    damage_charge,
    cancellation_dues=0
):

    charges = [
        ("Late Fee", late_fee),
        ("Fuel Charge", fuel_charge),
        ("Excess KM Charge", km_charge),
        ("Damage Charge", damage_charge),
        ("Cancellation Dues", cancellation_dues)
    ]

    if deposit_amount < 0:
        raise ValueError("Deposit cannot be negative.")

    remaining_deposit = deposit_amount
    deductions = {}
    total_deducted = 0

    for name, charge in charges:

        if charge < 0:
            raise ValueError("Charges cannot be negative.")

        deducted = min(remaining_deposit, charge)

        deductions[name] = deducted

        remaining_deposit -= deducted
        total_deducted += deducted

    total_charges = sum(charge for _, charge in charges)

    excess_claim = max(0, total_charges - deposit_amount)

    return {
        "deductions": deductions,
        "amount_deducted": total_deducted,
        "refund": remaining_deposit,
        "excess_claim": excess_claim
    }


def calculate_release_date(completion_time):
    return completion_time + timedelta(days=3)


def check_deposit_release(completion_time, current_time, open_claim):

    if open_claim:
        return False, "Deposit cannot be released due to an unpaid claim."

    release_date = calculate_release_date(completion_time)

    if current_time < release_date:
        return False, "Deposit is not ready for release."

    return True, "Deposit released successfully."





