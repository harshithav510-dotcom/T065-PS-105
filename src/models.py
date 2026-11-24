from dataclasses import dataclass
from datetime import date, datetime


# Host details
@dataclass
class Host:
    host_id: str
    name: str
    completed_trips: int = 0
    rank: int = 0


# Guest details
@dataclass
class Guest:
    guest_id: str
    name: str
    age: int
    licence_valid_until: date
    trust_score: int
    open_damage_claim: bool = False


# Vehicle details
@dataclass
class Vehicle:
    vehicle_id: str
    host_id: str
    vehicle_type: str
    segment: str
    hourly_rate: float
    daily_rate: float
    home_city: str
    km_allowance: int = 0


# Booking details
@dataclass
class Booking:
    booking_id: str
    guest_id: str
    vehicle_id: str
    start_time: datetime
    end_time: datetime
    status: str = "BOOKED"


# Trip report details
@dataclass
class TripReport:
    booking_id: str
    start_odometer: float
    end_odometer: float
    start_fuel: int
    end_fuel: int
    actual_return_time: datetime
    damage_items: list
    photo_flag: bool = False


# Deposit details
@dataclass
class Deposit:
    booking_id: str
    amount_blocked: float
    amount_deducted: float = 0
    amount_refunded: float = 0
    status: str = "BLOCKED"
