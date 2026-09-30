"""Integer floor logarithm for arbitrarily large integers.

The core idea is to obtain a tight, always-correct estimate of the
floor logarithm via bit-length scaling, then correct it with a small
number of multiplications. This keeps us off the slow general path
(big-integer division) whenever possible.
"""


def _floor_log2(n: int) -> int:
    # Python's int.bit_length() is the fastest path we have, and it is
    # exact for base 2. It returns the number of bits needed to represent
    # the integer, which is exactly floor(log2(n)) + 1.
    return n.bit_length() - 1


def _bsearch_floor_log(n: int, base: int) -> int:
    """Slow but simple path for non-power-of-two bases.

    Uses binary search on the exponent. We bound the exponent using
    bit-lengths (floor_log2(base) == B-1), then narrow it with a single
    multiplication per step.
    """
    k = 0
    # n >= base implies there's at least one factor. Loop until we can no
    # longer divide by base; the count of divisions is the floor log.
    # Bounded: each iteration shrinks n by a factor of at least 2.
    base_bits = base.bit_length() - 1  # floor(log2(base))
    exponent = 0
    # Binary search on exponent e in range [0, max_k].
    max_k = max(1, (n.bit_length() - 1) // base_bits + 1)  # generous upper bound
    lo = 0
    hi = max_k
    # Invariant: base^lo <= n < base^(hi+1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if base ** mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def floor_log2(n: int) -> int:
    """Return floor(log2(n)) for a non-negative integer n.

    Uses int.bit_length() directly; this is exact and O(1) relative to
    the size of n's representation.

    Raises ValueError if n < 1.
    """
    if n < 1:
        raise ValueError("logarithm undefined for n < 1")
    return _floor_log2(n)


def floor_log_base(n: int, base: int) -> int:
    """Return floor(log_base(n)) for positive integers n and base.

    For base == 2, uses int.bit_length() directly (fastest, exact).
    For bases that are exact powers of two, converts to base 2.
    For all other bases, uses bit-length scaling to form an initial
    estimate and then corrects it with repeated multiplication.

    Raises ValueError if n < 1 or base < 2.
    """
    if n < 1:
        raise ValueError("logarithm undefined for n < 1")
    if base < 2:
        raise ValueError("base must be >= 2")

    # Fast path: base is a power of two.
    # We check this by inspecting bit_length; for a power of two p,
    # p.bit_length() == p.bit_length() of (p-1) + 1.
    # Equivalently, p & (p - 1) == 0 for powers of two.
    if base & (base - 1) == 0:
        # base == 2**b2
        b2 = base.bit_length() - 1
        # n.bit_length() - 1 == floor(log2(n)); divide by b2 with floor.
        return _floor_log2(n) // b2

    return _bsearch_floor_log(n, base)


def floor_log(n: int, base: int = 10) -> int:
    """Return floor(log_base(n)) for positive integers.

    Defaults to base 10 (the common case for digit counting).

    See floor_log_base for edge cases and exceptions.
    """
    return floor_log_base(n, base)
