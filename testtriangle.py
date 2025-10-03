import unittest
import math

from triangle import classify_triangle


class NewTriangleTests(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "equilateral triangle")

    def test_isosceles(self):
        self.assertEqual(classify_triangle(5, 5, 8), "isosceles triangle")

    def test_scalene(self):
        self.assertEqual(classify_triangle(4, 5, 6), "scalene triangle")

    def test_right_integer(self):
        self.assertEqual(classify_triangle(3, 4, 5), "right triangle")

    def test_right_isosceles_float(self):
        self.assertEqual(classify_triangle(1.0, 1.0, math.sqrt(2)), "right triangle")

    def test_zero_or_negative(self):
        self.assertEqual(classify_triangle(0, 2, 3), "not a triangle")

    def test_triangle_inequality(self):
        self.assertEqual(classify_triangle(1, 2, 3), "not a triangle")


if __name__ == "__main__":  # optional for direct run
    unittest.main(verbosity=2)
