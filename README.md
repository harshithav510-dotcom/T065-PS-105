PS-105 – Peer-to-Peer Vehicle Sharing Trip Pricing, Damage Deposit and Owner Settlement Engine

Project Overview

This project implements a backend engine for a peer-to-peer vehicle-sharing marketplace. It manages vehicle bookings, trip pricing, damage deposits, trip lifecycle operations, damage claims, and host settlement calculations.

The system processes a predefined set of input data and commands to simulate real-world vehicle-sharing transactions. It applies business rules to ensure correct booking validation, pricing calculations, deposit handling, and settlement processing.

Project Objectives

The main objectives of this project are:

- To implement a vehicle booking management system.
- To calculate trip prices based on vehicle and booking details.
- To manage damage deposits and protection plans.
- To prevent vehicle booking conflicts.
- To handle booking cancellations and trip extensions.
- To manage trip start and end operations.
- To calculate fuel, damage, and late-return charges.
- To process damage reports and settlements.
- To generate host settlement statements.
- To validate the system using automated test cases.

Project Domain

Mobility Marketplace

Technology Stack

- Programming Language: Python
- Testing Framework: Pytest
- Data Formats: CSV and JSON
- Development Environment: Visual Studio Code
- Version Control: Git and GitHub

Project Structure

T065-PS-105/
│
├── src/
│   ├── availability.py
│   ├── booking.py
│   ├── cancellation.py
│   ├── damage.py
│   ├── damage_settlement.py
│   ├── deposit.py
│   ├── eligibility.py
│   ├── extension.py
│   ├── fuel.py
│   ├── main.py
│   ├── models.py
│   ├── pricing.py
│   ├── registration.py
│   ├── reports.py
│   ├── settlement.py
│   ├── storage.py
│   └── commands.txt
│
├── tests/
│
├── data/
│
├── outputs/
│
├── assignment_runner.py
├── README.md
└── .gitignore

Input Files

The system uses structured input data to simulate vehicle-sharing operations.

The input data includes:

- Host information
- Vehicle information
- Guest information
- Damage rate card
- Booking and trip commands

Command Processing

The system processes commands in the order specified in the command file.

The supported operations include:

BOOK

Creates a vehicle booking after validating the booking details and vehicle availability.

CANCEL_BOOKING

Cancels an existing booking according to the cancellation rules.

START_TRIP

Starts a valid booking and activates the trip.

EXTEND

Extends the booking duration and recalculates the applicable charges.

END_TRIP

Completes the trip and calculates the final trip charges.

DAMAGE_REPORT

Records damage reported during or after a trip.

SETTLE

Processes the settlement of the trip and applicable financial transactions.

HOST_STATEMENT

Generates a statement containing the host's settlement details.

Key Functionalities

1. Vehicle Availability Management

Checks vehicle availability and prevents overlapping bookings.

2. Trip Pricing Engine

Calculates trip prices according to the applicable pricing rules.

3. Damage Deposit Management

Calculates and manages the refundable damage deposit.

4. Protection Plan Management

Handles applicable protection plans and their associated charges.

5. Cancellation Management

Processes booking cancellations and applicable cancellation charges.

6. Trip Extension Management

Handles booking extensions and recalculates trip charges.

7. Fuel Charge Management

Calculates fuel-related charges based on trip information.

8. Damage Management

Records damage reports and calculates applicable damage charges.

9. Owner Settlement

Calculates the amount payable to the vehicle owner after applying the relevant charges and deductions.

10. Report Generation

Generates transaction reports and host settlement statements.

Business Rules

- A vehicle cannot have overlapping confirmed bookings.
- Booking details must be validated before confirmation.
- A valid booking is required to start a trip.
- Trip operations must follow the correct lifecycle.
- Deposits must be handled according to the defined rules.
- Pricing and settlement calculations must follow the configured business logic.
- Duplicate or invalid operations must be handled appropriately.
- Financial transactions must be recorded consistently.

Execution Instructions

Step 1: Open the Project

Open the project folder in Visual Studio Code.

Step 2: Run the Main Program

py src/main.py

Step 3: Run the Assignment Runner

py assignment_runner.py

Step 4: Run Automated Tests

py -m pytest -v

Output Files

The system generates output files containing the processed transaction details.

The expected output files include:

- "quotes.csv" – Stores trip pricing and quote information.
- "bills.csv" – Stores final trip billing details.
- "host_settlements.csv" – Stores host settlement calculations.
- "host_statements.csv" – Stores host statement information.

These files help verify the results of the booking, pricing, deposit, damage, and settlement operations.

Testing

The project includes automated test cases to verify the correctness of the implemented functionalities.

The tests cover:

- Booking validation
- Vehicle availability
- Pricing calculations
- Deposit calculations
- Cancellation operations
- Trip extensions
- Trip completion
- Damage reporting
- Settlement processing
- Report generation

Automated Test Result: 85 Tests Passed

The successful execution of the test suite demonstrates that the implemented functionality passed the defined test scenarios.

Expected Outcome

The expected outcome of this project is a functional backend engine that simulates the essential operations of a peer-to-peer vehicle-sharing marketplace.

The system automates booking management, trip pricing, damage deposit handling, trip operations, damage charges, and host settlement calculations.

It provides accurate transaction processing, reduces manual calculations, and ensures that the defined business rules are applied consistently.

Conclusion

The Peer-to-Peer Vehicle Sharing Trip Pricing, Damage Deposit and Owner Settlement Engine demonstrates the application of Python programming to a real-world mobility marketplace problem.

The project integrates multiple backend modules to manage bookings, pricing, deposits, trip operations, damage handling, and financial settlements.

With 85 automated tests passing, the project demonstrates the successful implementation and validation of its core functionalities.

Team Information

Project ID: T065-PS-105
Team ID: T065
Team: CSD A
Project Domain: Mobility Marketplace

Team Members:

- Harshitha V
- Harsha Atluru
