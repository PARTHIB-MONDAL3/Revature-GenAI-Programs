import unittest

from Testting.tte import calculate_error

values_positive = [1, 2, 3, 4]
values_negative = [1, 2, -3, 4]

class TestCalculateError(unittest.TestCase):

    def test_all_positive(self):
        result = calculate_error(values_positive)
        self.assertEqual(result, "All values are positive")

    def test_negative_value(self):
        with self.assertRaises(ValueError):
            calculate_error(values_negative)

if __name__ == '__main__':
    unittest.main()
