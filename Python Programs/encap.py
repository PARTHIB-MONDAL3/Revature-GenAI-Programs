class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # private variable

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

acc = BankAccount(5000)
acc.deposit(2000)
print(acc.get_balance())   # ✅ 7000
print(acc.__balance)       # ❌ AttributeError