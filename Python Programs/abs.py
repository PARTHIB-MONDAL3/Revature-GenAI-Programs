from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCard(Payment):
    def process_payment(self, amount):
        print(f"Processing Credit Card payment of ₹{amount}")

pay = CreditCard()
pay.process_payment(5000)