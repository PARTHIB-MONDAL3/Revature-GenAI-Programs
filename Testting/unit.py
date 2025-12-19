import unittest

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def clear(self):
        self.items.clear()

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        # Runs before each test
        self.cart = ShoppingCart()

    def tearDown(self):
        # Runs after each test
        self.cart.clear()

    def test_cart_starts_empty(self):
        self.assertEqual(self.cart.total(), 0)

    def test_add_single_item(self):
        self.cart.add_item("Book", 299.0)
        self.assertEqual(self.cart.total(), 299.0)

if __name__ == "__main__":
    unittest.main()