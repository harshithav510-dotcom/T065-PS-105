
from deposit import Deposit
from datetime import datetime, timedelta


def test_no_damage_deposit_release():

    deposit = Deposit(2000)

    deposit.complete_trip(False)

    deposit.release_date = datetime.now() - timedelta(days=3)

    deposit.release_deposit()

    assert deposit.status == "RELEASED"


def test_damage_deposit_hold():

    deposit = Deposit(2000)

    deposit.complete_trip(True)

    deposit.release_deposit()

    assert deposit.status == "ON HOLD"
