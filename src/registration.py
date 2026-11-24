from models import Host, Guest, Vehicle


def register_host(hosts, host_id, name):
    if any(h.host_id == host_id for h in hosts):
        return None

    host = Host(host_id, name)
    hosts.append(host)
    return host


def register_guest(guests, guest_id, name, age, licence_date, trust_score):
    if any(g.guest_id == guest_id for g in guests):
        return None

    guest = Guest(
        guest_id, name, age, licence_date, trust_score
    )
    guests.append(guest)
    return guest


def register_vehicle(
    vehicles, vehicle_id, host_id, vehicle_type,
    segment, hourly_rate, daily_rate, city, km_allowance=0
):
    if any(v.vehicle_id == vehicle_id for v in vehicles):
        return None

    vehicle = Vehicle(
        vehicle_id, host_id, vehicle_type, segment,
        hourly_rate, daily_rate, city, km_allowance
    )
    vehicles.append(vehicle)
    return vehicle
