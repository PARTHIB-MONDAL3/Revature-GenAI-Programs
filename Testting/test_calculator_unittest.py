# test_calculator_unittest.py

import unittest
import calculator

class TestCalculator(unittest.TestCase):

    def test_add_two_numbers(self):
        result = calculator.add(2, 3)
        self.assertEqual(result, 5)

    def test_is_even_true(self):
        self.assertTrue(calculator.is_even(4))

    def test_is_even_false(self):
        self.assertFalse(calculator.is_even(5))

if __name__ == "__main__":
    unittest.main()
    