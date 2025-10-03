"""Triangle classifier.

Returns one of:
- "equilateral triangle"
- "isosceles triangle"
- "scalene triangle"
- "right triangle"
- "not a triangle"
"""

from __future__ import annotations
from typing import Union, Sequence
import math

Number = Union[int, float]


def _is_right(x: Number, y: Number, z: Number) -> bool:
    """Return True if x^2 + y^2 == z^2 within a small tolerance."""
    # tolerate tiny float error (e.g., sqrt(2))
    return math.isclose(x * x + y * y, z * z, rel_tol=1e-12, abs_tol=1e-12)


def classify_triangle(a: Number, b: Number, c: Number) -> str:
    """Classify a triangle by side lengths a, b, c."""
    # 1) validity
    if a <= 0 or b <= 0 or c <= 0:
        return "not a triangle"
    if a + b <= c or a + c <= b or b + c <= a:
        return "not a triangle"

    # 2) sorted sides so z is longest; helps with right-check
    x, y, z = cast(Sequence[Number], sorted([a, b, c]))  # type: ignore[name-defined]

    # 3) equilateral
    if a == b == c:
        return "equilateral triangle"

    # 4) right?
    is_right = _is_right(x, y, z)

    # 5) isosceles (two equal)
    if a == b or b == c or a == c:
        # Your course’s expected string treats “right isosceles” as just “right triangle”
        return "right triangle" if is_right else "isosceles triangle"

    # 6) scalene
    return "right triangle" if is_right else "scalene triangle"


# Small helper so mypy doesn't complain about cast without import
def cast(_: type, val):
    return val


if __name__ == "__main__":  # pragma: no cover
    # Demo lines (excluded from coverage):
    print(classify_triangle(3, 4, 5))      # right triangle
    print(classify_triangle(2, 2, 2))      # equilateral triangle
    print(classify_triangle(5, 5, 8))      # isosceles triangle
    print(classify_triangle(4, 5, 6))      # scalene triangle
    print(classify_triangle(1, 2, 3))      # not a triangle
