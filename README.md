# Big Integer Logarithm

Returns the integer floor of the base-b logarithm of an arbitrarily large Python integer, using bit-length scaling and correction.

## Usage

```python
from big_integer_logarithm import floor_log, floor_log_base, floor_log2

# Default base is 10.
floor_log(10 ** 50)           # 50
floor_log(10 ** 50 + 1)       # 50
floor_log(10 ** 51 - 1)       # 50

# Any integer base >= 2.
floor_log_base(3 ** 100, 3)   # 100
floor_log_base((1 << 64) - 1, 2)  # 63

# Base-2 shortcut, exact and fast.
floor_log2(1 << 1000)         # 1000
```

## Why this exists

Python's `math.log` converts to float, so it overflows and loses precision past ~1e308. When you need the integer floor of the logarithm of a genuinely large integer (RSA-sized numbers, big factorials, combinatorial counts), you need an integer-only path. This library provides one with no dependencies.

The fast path uses `int.bit_length()`, which is exact for base 2 and gives a tight estimate for any base that is a power of two. For other bases, it binary-searches the exponent with one `base ** mid` computation per step, bounded above by a bit-length-derived estimate. This avoids general big-integer division entirely.

## Edge cases

- `n < 1` raises `ValueError`. There is no floor logarithm for zero or negatives in the integers.
- `base < 2` raises `ValueError`.
- `floor_log_base(n, 4)` uses the power-of-two fast path: `floor(log2(n)) // 2`.
- For non-power-of-two bases, the result is exact but uses the slower binary-search path; expect it to be slower than the base-2 path for inputs of comparable size.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

