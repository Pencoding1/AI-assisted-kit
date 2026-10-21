import unittest

from app.order_total import invoice_total_cents


class OrderTotalSafety(unittest.TestCase):
    def test_total_is_integer_cents(self):
        total = invoice_total_cents([(2, 50000), (1, 25000)], 10)
        self.assertIs(type(total), int)

    def test_total_bounds(self):
        total = invoice_total_cents([(2, 50000), (1, 25000)], 10)
        self.assertGreaterEqual(total, 0)
        self.assertLessEqual(total, 125000)

    def test_empty_basket_is_integer_zero(self):
        total = invoice_total_cents([], 0)
        self.assertEqual(total, 0)
        self.assertIs(type(total), int)

    def test_invalid_line_input_rejected(self):
        for items in (
            [(0, 100)],
            [(1, -1)],
            [(True, 100)],
            [("1", 100)],
        ):
            with self.assertRaises(ValueError):
                invoice_total_cents(items, 0)


if __name__ == "__main__":
    unittest.main()
