# PS-105 – Peer-to-Peer Vehicle Sharing Trip Pricing, Damage Deposit and Owner Settlement Engine — Sample Data Pack
Prepared by 10 SECONDS for Team T065.

## Files
| File | What it holds | Rows |
|---|---|---|
| hosts.csv | Vehicle hosts and prior completed-trip counts | 8 |
| vehicles.csv | Vehicles with host rates | 15 |
| guests.csv | Guests with licence, age and trust score | 20 |
| damage_rate_card.csv | Assessed amount per damage item | 8 |
| commands.txt | 60 bookings, 50 closed trips (start/end/settle), damage reports, cancellations, extensions, host statements | 231 |

## Column reference
Conventions: dates `YYYY-MM-DD`; timestamps `YYYY-MM-DD HH:MM:SS` (24h, IST, no timezone suffix); money in Rs as plain decimals with 2 places (no commas, no symbol); percentages as plain numbers (12.5 = 12.5%); booleans `true`/`false`; IDs uppercase with a fixed prefix. Row counts in the Files table exclude the header row (and comment lines in command files).

### hosts.csv
| Column | Type | Units/format | Allowed values | Notes |
|---|---|---|---|---|
| host_id | string | HST-NNN |  | PK |
| host_name | string |  |  |  |
| city | string |  |  |  |
| completed_trips_before | integer |  |  | completed trips before this file |

### vehicles.csv
| Column | Type | Units/format | Allowed values | Notes |
|---|---|---|---|---|
| vehicle_id | string | VEH-NNN |  | PK |
| host_id | string |  | hosts.host_id |  |
| vehicle_type | string |  | CAR/BIKE |  |
| segment | string |  | HATCHBACK/SEDAN/SUV/LUXURY/BIKE |  |
| model | string |  |  |  |
| hourly_rate | money | Rs/hour |  | host-set |
| daily_rate | money | Rs/day |  | host-set |
| home_city | string |  |  |  |

### guests.csv
| Column | Type | Units/format | Allowed values | Notes |
|---|---|---|---|---|
| guest_id | string | GST-NNN |  | PK |
| guest_name | string |  |  |  |
| gender | string |  | M/F |  |
| dob | date | YYYY-MM-DD |  | age computed at booking timestamp |
| licence_expiry | date | YYYY-MM-DD |  | last valid day |
| trust_score | integer |  | 0-100 |  |
| open_damage_claim | boolean |  | true/false | at file start |
| city | string |  |  |  |

### damage_rate_card.csv
| Column | Type | Units/format | Allowed values | Notes |
|---|---|---|---|---|
| item_code | string | DMG-NN |  | PK |
| description | string |  |  |  |
| assessed_amount | money | Rs |  |  |

### commands.txt
| Column | Type | Units/format | Allowed values | Notes |
|---|---|---|---|---|
| line | text | COMMAND/args | see below |  |

## Command file format
`commands.txt` holds one command per line in the form `COMMAND_NAME|arg1|arg2|...`. Commands MUST be processed in file order (top to bottom). Lines starting with `#` are comments and blank lines are ignored. Argument order per command:

| Command | Arguments (in order) | Meaning |
|---|---|---|
| BOOK | ts/booking_id/guest_id/vehicle_id/start_ts/end_ts/protection | quote + book; protection true/false |
| CANCEL_BOOKING | ts/booking_id/by | by GUEST/HOST |
| START_TRIP | ts/booking_id/odometer_start/fuel_start_eighths | fuel 0-8 |
| EXTEND | ts/booking_id/new_end_ts | extension of a running trip |
| END_TRIP | ts/booking_id/odometer_end/fuel_end_eighths/return_ts | trip-end report |
| DAMAGE_REPORT | ts/booking_id/item_code/photo | host report; photo true/false; valid only within 24 h of return |
| SETTLE | ts/booking_id | close trip: final bill, deposit deductions, host settlement |
| HOST_STATEMENT | ts/host_id | print host statement |

## Planted scenarios
Every edge case from the brief is planted at a known location, followed by extra traps. Line numbers refer to `commands.txt` counting from line 1 including comment lines.
- **Trip of exactly 24 hours (hourly vs daily tie)** — BKG-001 (line 13): sedan VEH-006 2026-10-06 10:00 → 2026-10-07 10:00, exactly 24 h: hourly×24 vs daily×1 tie; over-24h daily mandate does not trigger.
- **Return exactly 30 minutes late** — BKG-002 booked to end 2026-10-07 14:00:00; END_TRIP return at 14:30:00 (line 38) = exactly 30 min late → within grace.
- **Fuel returned at 3/8 when started at 4/8 by a bike** — BKG-003 bike VEH-013 started at 4/8, returned at 3/8 (line 45) → 1 eighth short × Rs 150.
- **Damage assessed at Rs 1,500 with protection where the guest trust score halved the deposit** — BKG-004: GST-001 (trust 85 → 50% deposit = 1500.00 on hatchback) with protection; DAMAGE_REPORT DMG-01 assessed 1500.00 at line 59 → liability cap Rs 1,500 equals the halved deposit.
- **Extension requested when the next booking starts in exactly 2 hours** — BKG-005 on VEH-003 ends 13:00; next booking starts 17:00; EXTEND to 15:00 at line 65 → next booking starts exactly 2 h after the new end (boundary of the 'within 2 hours' rule).
- **Weekend multiplier on a trip starting Friday 17:30** — BKG-007 (line 37) SUV trip Fri 2026-10-09 17:30 → 21:30: first 30 min before the Fri 18:00 weekend start, remaining hours in the weekend window.
- **Host with exactly 10 completed trips at settlement** — HST-003 has completed_trips_before = 9; SETTLE of BKG-008 at line 106 is its 10th completed trip → 20% vs 15% commission boundary (state your BR: count before or including this trip).
- **Licence expiring on the trip end date** — BKG-009 (line 123): GST-004 licence_expiry 2026-10-18 equals the trip end date → must be valid through end + 1 day → reject.
- Trap — GST-002 (dob 2006-10-20, age 20 at booking) booking a car at line 124 (reject) but a bike at line 125 (allowed, ≥ 18).
- Trap — GST-003 trust 38 booking LUXURY at line 126 (reject); GST-005 has an open damage claim, booking at line 127 (reject).
- Trap — overlapping booking on VEH-006 at line 18 (reject on availability); guest cancellation at exactly 48 h before start at line 179; host cancellation <24 h at line 189 (Rs 1,000 host penalty + Rs 500 guest credit).
- Trap — BKG-017: 7 h late (inconvenience fee), 3 eighths fuel short, excess km and DMG-02 4500.00 without protection → deductions exceed the Rs 3,000 deposit; apply the deduction order and raise a claim (report line 121).
- Trap — duplicate END_TRIP at line 103 (reject); this line is deliberately out of timestamp order with its neighbour — process in file order.
- Trap — damage report without photo flag (line 140) and a report filed 26 h after trip end (line 144) must both be ignored.

## What is NOT in this pack
Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-nn). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.

## Output format expected at evaluation
Produce the following CSV files (header row, same conventions as above, rows in the order stated). Column names are case-sensitive.

### `quotes.csv`
One row per BOOK line in file order; pricing_mode HOURLY/DAILY; status BOOKED/REJECTED.

Columns, in order: `booking_id`, `status`, `pricing_mode`, `duration_charge`, `deposit_blocked`, `protection_fee`, `message`

### `bills.csv`
One row per SETTLE in file order.

Columns, in order: `booking_id`, `duration_charge`, `excess_km`, `excess_km_charge`, `late_minutes`, `late_charge`, `fuel_charge`, `damage_charge`, `protection_fee`, `total`, `deposit_deducted`, `deposit_refund`, `claim_raised`

### `host_settlements.csv`
One row per SETTLE in file order.

Columns, in order: `booking_id`, `host_id`, `trip_price`, `commission_pct`, `commission`, `late_fuel_passthrough`, `damage_recovery`, `host_payout`

### `host_statements.csv`
One row per HOST_STATEMENT.

Columns, in order: `host_id`, `completed_trips`, `gross`, `commission`, `penalties`, `net`

## Notes and assumptions
- Fuel levels are integers 0–8 (eighths of a tank).
- Hours are billed rounded up to the next whole hour; days rounded up to the next whole day.
- Weekend window is Fri 18:00:00 to Mon 06:00:00; apply the 1.2x multiplier to the host rate for the hours falling inside the window.
