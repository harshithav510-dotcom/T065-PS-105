def calculate_damage_charge(damage_cost, deposit, protection):

    if damage_cost < 0:
        raise ValueError("Damage cost cannot be negative.")

    if protection:
        liability = min(damage_cost, 1500)
    else:
        liability = min(damage_cost, deposit)

    return liability
