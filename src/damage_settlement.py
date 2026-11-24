class DamageSettlement:

    def __init__(self, deposit, damage_amount):
        self.deposit = deposit
        self.damage_amount = damage_amount

    def settle(self):

        print("Damage Amount: Rs.", self.damage_amount)
        print("Deposit Amount: Rs.", self.deposit.amount)

        if self.damage_amount <= self.deposit.amount:

            refund = self.deposit.amount - self.damage_amount

            print("Owner Compensation: Rs.", self.damage_amount)
            print("Guest Refund: Rs.", refund)

            self.deposit.status = "SETTLED"

        else:
            extra = self.damage_amount - self.deposit.amount

            print("Deposit Used: Rs.", self.deposit.amount)
            print("Additional Amount Due: Rs.", extra)

            self.deposit.status = "SETTLED"