
from deposit import Deposit
from damage_settlement import DamageSettlement


def test_damage_settlement():

    deposit = Deposit(2000)

    deposit.complete_trip(True)

    settlement = DamageSettlement(deposit, 3000)

    settlement.settle()

    assert deposit.status == "SETTLED"
