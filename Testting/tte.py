#take an array take 2 3 positive value and return the error for the negative value uisng unittest
def calculate_error(values):
    for value in values:
        if value < 0:
            raise ValueError(f"Negative value encountered: {value}")
    return "All values are positive"
import unittest
