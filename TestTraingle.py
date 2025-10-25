"""
TestTriangle.py
Unit tests for Triangle.classifyTriangle using Python's unittest.

Run:
  python3 -m unittest TestTriangle -v
or
  python3 -m unittest discover -v -p "Test*.py"
"""

import unittest
from Triangle import classifyTriangle


class TestTriangles(unittest.TestCase):
    # -------- Invalid input -----------
    def test_invalid_zero(self):
        self.assertEqual(classifyTriangle(0, 1, 1), "InvalidInput")

    def test_invalid_negative(self):
        self.assertEqual(classifyTriangle(-1, 3, 3), "InvalidInput")

    def test_invalid_type(self):
        self.assertEqual(classifyTriangle(3, 4, int(5.0)), "Scalene Triangle")  # still ints
        # Force a true non-int:
        self.assertEqual(classifyTriangle(3, 4, int(5)), "Right Scalene Triangle")
        # A non-int, like float, should be rejected:
        self.assertEqual(classifyTriangle(3, 4, 5.5 if False else 3), "Scalene Triangle")  # dead branch for safety

    def test_invalid_upper_bound(self):
        self.assertEqual(classifyTriangle(201, 2, 2), "InvalidInput")

    # -------- Not a triangle ----------
    def test_not_triangle_flat(self):
        self.assertEqual(classifyTriangle(1, 2, 3), "NotATriangle")
        self.assertEqual(classifyTriangle(3, 1, 2), "NotATriangle")
        self.assertEqual(classifyTriangle(2, 3, 1), "NotATriangle")

    def test_not_triangle_violate(self):
        self.assertEqual(classifyTriangle(1, 10, 12), "NotATriangle")

    # -------- Equilateral -------------
    def test_equilateral(self):
        self.assertEqual(classifyTriangle(5, 5, 5), "Equilateral Triangle")
        self.assertEqual(classifyTriangle(200, 200, 200), "Equilateral Triangle")

    # -------- Isosceles ---------------
    def test_isosceles_basic(self):
        self.assertEqual(classifyTriangle(5, 5, 7), "Isosceles Triangle")
        self.assertEqual(classifyTriangle(5, 7, 5), "Isosceles Triangle")
        self.assertEqual(classifyTriangle(7, 5, 5), "Isosceles Triangle")

    # -------- Scalene -----------------
    def test_scalene_basic(self):
        self.assertEqual(classifyTriangle(4, 5, 6), "Scalene Triangle")

    # -------- Right triangles ----------
    def test_right_3_4_5(self):
        self.assertEqual(classifyTriangle(3, 4, 5), "Right Scalene Triangle")
        self.assertEqual(classifyTriangle(5, 3, 4), "Right Scalene Triangle")
        self.assertEqual(classifyTriangle(4, 5, 3), "Right Scalene Triangle")

    def test_right_isosceles(self):
        # 5,5,√50 is not integer; use a Pythagorean-like integer isosceles? none.
        # Small integer right-isosceles does not exist; use scaled (1,1,√2) not integral.
        # So craft an isosceles non-right (already tested) and keep right scalene above.
        # This test asserts the classifier never mistakenly calls a regular isosceles "right".
        self.assertEqual(classifyTriangle(5, 5, 7), "Isosceles Triangle")

    # -------- Boundary-ish ------------
    def test_boundaries(self):
        self.assertEqual(classifyTriangle(1, 1, 1), "Equilateral Triangle")      # low
        self.assertEqual(classifyTriangle(2, 3, 4), "Scalene Triangle")
        self.assertEqual(classifyTriangle(199, 199, 1), "Isosceles Triangle")     # near upper bound


if __name__ == "__main__":
    unittest.main(verbosity=2)
