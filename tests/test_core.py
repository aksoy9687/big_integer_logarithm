import unittest

from big_integer_logarithm import floor_log, floor_log_base, floor_log2


class TestFloorLog2(unittest.TestCase):
    def test_one(self):
        self.assertEqual(floor_log2(1), 0)

    def test_powers_of_two(self):
        for e in range(1, 20):
            self.assertEqual(floor_log2(1 << e), e)

    def test_non_powers(self):
        # floor_log2(2^k - 1) == k - 1, and floor_log2(2^k + 1) == k.
        for k in range(1, 20):
            self.assertEqual(floor_log2((1 << k) - 1), k - 1)
            self.assertEqual(floor_log2((1 << k) + 1), k)

    def test_large(self):
        # An arbitrarily large power of two.
        big = 1 << 1000
        self.assertEqual(floor_log2(big), 1000)

    def test_zero_and_negative_raise(self):
        with self.assertRaises(ValueError):
            floor_log2(0)
        with self.assertRaises(ValueError):
            floor_log2(-5)


class TestFloorLogBase(unittest.TestCase):
    def test_base_two_matches_floor_log2(self):
        for n in [1, 2, 3, 7, 8, 9, 1 << 64, (1 << 64) - 1]:
            self.assertEqual(floor_log_base(n, 2), floor_log2(n))

    def test_base_four_power_of_two(self):
        # 4 == 2^2, so floor(log4(n)) == floor(log2(n) // 2).
        for n in [1, 3, 4, 5, 15, 16, 17, 63, 64, 65]:
            self.assertEqual(floor_log_base(n, 4), floor_log2(n) // 2)

    def test_base_ten(self):
        # Classic digit-count boundary.
        for e in range(0, 18):
            self.assertEqual(floor_log_base(10 ** e, 10), e)
            self.assertEqual(floor_log_base(10 ** e + 1, 10), e)
            self.assertEqual(floor_log_base(10 ** (e + 1) - 1, 10), e)

    def test_base_three_non_power_of_two(self):
        for e in range(0, 20):
            self.assertEqual(floor_log_base(3 ** e, 3), e)
            self.assertEqual(floor_log_base(3 ** e + 1, 3), e)
            if e > 0:
                self.assertEqual(floor_log_base(3 ** e - 1, 3), e - 1)

    def test_huge_base(self):
        # A base that is itself large but a power of two.
        big_base = 1 << 500
        self.assertEqual(floor_log_base(big_base, big_base), 1)
        self.assertEqual(floor_log_base(big_base * big_base, big_base), 2)

    def test_huge_non_power_of_two_base(self):
        big_base = (1 << 500) - 1  # not a power of two
        self.assertEqual(floor_log_base(big_base, big_base), 1)
        self.assertEqual(floor_log_base(big_base * big_base, big_base), 2)

    def test_n_equals_one(self):
        # log_b(1) == 0 for any valid base.
        for b in [2, 3, 4, 10, 256, 1000]:
            self.assertEqual(floor_log_base(1, b), 0)

    def test_invalid_base_raises(self):
        with self.assertRaises(ValueError):
            floor_log_base(5, 0)
        with self.assertRaises(ValueError):
            floor_log_base(5, 1)

    def test_invalid_n_raises(self):
        with self.assertRaises(ValueError):
            floor_log_base(0, 10)
        with self.assertRaises(ValueError):
            floor_log_base(-1, 10)

    def test_large_non_power_of_two_n(self):
        # 3 ** 200 is well outside typical float range; ensure correctness.
        n = 3 ** 200
        self.assertEqual(floor_log_base(n, 3), 200)
        self.assertEqual(floor_log_base(n + 1, 3), 200)
        self.assertEqual(floor_log_base(n - 1, 3), 199)


class TestFloorLogDefaultBase(unittest.TestCase):
    def test_default_base_is_ten(self):
        for e in range(0, 18):
            self.assertEqual(floor_log(10 ** e), e)
            self.assertEqual(floor_log(10 ** e + 1), e)


if __name__ == "__main__":
    unittest.main()
