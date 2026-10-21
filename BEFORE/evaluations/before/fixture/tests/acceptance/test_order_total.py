import unittest

from app.order_total import invoice_total_cents


class OrderTotalAcceptance(unittest.TestCase):
    def test_two_items_ten_percent_discount(self):
        self.assertEqual(invoice_total_cents([(2, 50000), (1, 25000)], 10), 112500)

    def test_full_discount_is_zero(self):
        self.assertEqual(invoice_total_cents([(1, 9999)], 100), 0)

    def test_half_up_rounding(self):
        self.assertEqual(invoice_total_cents([(1, 5)], 50), 3)

    def test_invalid_discount_rejected(self):
        with self.assertRaises(ValueError):
            invoice_total_cents([(1, 100)], 101)
        with self.assertRaises(ValueError):
            invoice_total_cents([(1, 100)], -1)


if __name__ == "__main__":
    unittest.main()
