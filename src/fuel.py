def calculate_fuel_charge(start_fuel, end_fuel, vehicle_type):

    shortage = max(0, start_fuel - end_fuel)

    # Fuel is measured in eighths
    if vehicle_type.upper() == "BIKE":
        rate = 150
    else:
        rate = 600

    return shortage * rate
