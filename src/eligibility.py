from datetime import timedelta


def check_eligibility(guest, vehicle, start_time, end_time):

    # Check that trip end time is after start time
    if end_time <= start_time:
        return False, "End time must be after start time."

    # Check minimum age
    if vehicle.vehicle_type.upper() == "BIKE":
        if guest.age < 18:
            return False, "Guest must be at least 18 years old."
    else:
        if guest.age < 21:
            return False, "Guest must be at least 21 years old."

    # Check driving licence validity
    required_validity = end_time.date() + timedelta(days=1)

    if guest.licence_valid_until < required_validity:
        return False, "Driving licence is not valid for the required period."

    # Check trust score for luxury vehicles
    if vehicle.segment.upper() == "LUXURY" and guest.trust_score < 40:
        return False, "Trust score is too low for a luxury vehicle."

    # Check unpaid damage claims
    if guest.open_damage_claim:
        return False, "Guest has an unpaid damage claim."

    return True, "Guest is eligible to book."

