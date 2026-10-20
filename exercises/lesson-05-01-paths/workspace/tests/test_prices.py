import unittest
from prices import total_price


class PriceTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total_price(100, 3), 300)
        self.assertEqual(total_price(100, 0), 0)
        self.assertEqual(total_price(12.5, 2), 25)
