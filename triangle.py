"""
Triangle.py
Robust triangle classifier with clear return labels that match the homework.

Returns one of:
  - "InvalidInput"
  - "NotATriangle"
  - "Equilateral Triangle"
  - "Isosceles Triangle"
  - "Scalene Triangle"
  - "Right Isosceles Triangle"
  - "Right Scalene Triangle"
"""

from typing import Tuple


def _is_valid_inputs(a: int, b: int, c: int) -> bool:
    # All must be ints and in a reasonable range (same as the class/homework style)
    if not all(isinstance(x, int) for x in (a, b, c)):
        return False
    if not all(x > 0 for x in (a, b, c)):
        return False
    # Optional upper bound the course often uses (keeps overflow/absurd values away)
    if not all(x <= 200 for x in (a, b, c)):
        return False
    return True


def _is_triangle(a: int, b: int, c: int) -> bool:
    # Triangle inequality (non-degenerate)
    return a + b > c and a + c > b and b + c > a


def _is_right(a: int, b: int, c: int) -> bool:
    # Sort so that z is the largest
    x, y, z = sorted((a, b, c))
    return x * x + y * y == z * z


def classifyTriangle(a: int, b: int, c: int) -> str:
    """
    Classify a triangle by its side lengths a, b, c.

    Returns a string:
      "InvalidInput"
      "NotATriangle"
      "Equilateral Triangle"
      "Isosceles Triangle"
      "Scalene Triangle"
      "Right Isosceles Triangle"
      "Right Scalene Triangle"
    """
    if not _is_valid_inputs(a, b, c):
        return "InvalidInput"

    if not _is_triangle(a, b, c):
        return "NotATriangle"

    # Equilateral
    if a == b == c:
        return "Equilateral Triangle"

    # Right?
    is_right = _is_right(a, b, c)

    # Isosceles or Scalene
    is_isosceles = a == b or b == c or a == c

    if is_right and is_isosceles:
        return "Right Isosceles Triangle"
    if is_right and not is_isosceles:
        return "Right Scalene Triangle"
    if is_isosceles:
        return "Isosceles Triangle"
    return "Scalene Triangle"


if __name__ == "__main__":
    # Tiny sanity run if you execute this file directly
    samples: Tuple[Tuple[int, int, int], ...] = (
        (3, 4, 5),
        (5, 5, 5),
        (5, 5, 7),
        (10, 6, 7),
        (1, 2, 3),
        (0, 2, 2),
        (2, 200, 2),
    )
    for sides in samples:
        print(sides, "=>", classifyTriangle(*sides))
