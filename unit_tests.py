class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        (self.assertEqual(add_numbers(3, 5), 8))

    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-3, -5), -8)

    def test_mixed_numbers(self):
        self.assertEqual(add_numbers(-3, 5), 2)

    def test_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)