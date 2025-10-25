# Triangle.py
# Clean, spec-compliant triangle classifier

def classifyTriangle(a, b, c):
    """
    Return a string classifying a triangle from side lengths a, b, c.

    Returns one of:
      - 'InvalidInput'  : any side not int, <=0, or >200
      - 'NotATriangle'  : violates triangle inequality
      - 'Equilateral'   : all three equal
      - 'Right'         : Pythagorean (any side order)
      - 'Isoceles'      : exactly two equal  (spelling retained to match legacy tests)
      - 'Scalene'       : all unequal

    Notes:
      * Inputs must be integers in (0, 200].
      * Triangle inequality: sum of any two sides must be strictly greater than the third.
    """

    # Type & range checks
    if not (isinstance(a, int) and isinstance(b, int) and isinstance(c, int)):
        return 'InvalidInput'
    if a <= 0 or b <= 0 or c <= 0:
        return 'InvalidInput'
    if a > 200 or b > 200 or c > 200:
        return 'InvalidInput'

    # Triangle inequality (strict)
    if a + b <= c or a + c <= b or b + c <= a:
        return 'NotATriangle'

    # Equilateral first (all equal)
    if a == b == c:
        return 'Equilateral'

    # Right triangle: check with sorted sides
    x, y, z = sorted([a, b, c])  # z is largest
    if x * x + y * y == z * z:
        return 'Right'

    # Isoceles (exactly two equal) — spelling kept to match legacy tests
    if a == b or b == c or a == c:
        return 'Isoceles'

    # Otherwise scalene
    return 'Scalene'
