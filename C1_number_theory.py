# For all examples first: import C1_number_theory as C1


def small_mult(up_lim, mod=10**12):
    """
    Find the smallest multiple.

    Idea:
        Compute LCM by iterating lazily over primes (the Sieve of Eratosthenes). For each prime, take the maximal power,
        multiply these together, and use modulo arithmetic to keep numbers manageable.
    Source:
        https://projecteuler.net/problem=5

    Examples:
        C1.small_mult(20) == 232792560
    """
    from C2_sieve_of_eratosthenes import sieve

    res = 1
    for prm in sieve(up_lim + 1):
        pwr = prm
        while pwr * prm <= up_lim:
            pwr *= prm
        res = (res * (pwr % mod)) % mod  # Modular arithmetic trick for huge numbers
    return res


def even_fib(up_lim):
    """
    Sum of the even-valued terms of the Fibonacci Sequence.

    Source:
        https://projecteuler.net/problem=2

    Notes:
        N{i} = 4N{i-1} + N{i-2}
        N{i} = N{i-1} + N{i-2} = N{i-2} + N{i-3} + N{i-2} = 2N{i-2} + N{i-3} = 2(N{i-3} + N{i-4}) + N{i-3} =
        = 3N{i-3} + 2N{i-4} = 3N{i-3} + N{i-4} + N{i-5} + N{i-6} = 3N{i-3} + N{i-3} + N{i-6} = 4N{i-3} + N{i-6}

    Examples:
        C1.even_fib(4E6) == 4613732
    """
    a, b, result = 2, 8, 2
    while b < up_lim:
        result += b
        a, b = b, 4 * b + a
    return result

up_l = 4E6  # may only be changed outside func
def even_fib_gr(a=2):
    """
    Sum of the even-valued terms of the Fibonacci Sequence by the Golden Ratio and recursion.

    Notes:
        N{i} / N{i-1} -> φ = (1 + 5**0.5) / 2 ≈ 1.618033988749895
        N{i} / N{i-3} -> φ**3

    Examples:
        C1.even_fib_gr() == 4613732
    """
    a = round(4.2360679 * a)
    return a + even_fib_gr(a) if a < up_l else 2


def palindrome(r):
    """
    Largest palindrome product.

    Idea:
        Find the largest palindrome from the product of two r-digit numbers. Construct palindromes by mirroring their
        first half and check factors from the largest down. Use a step to skip unnecessary checks and return
        the first divisible palindrome found.
    Source:
        https://projecteuler.net/problem=4

    Notes:
        • Any palindrome with an even number of digits is divisible by 11. Therefore, at least one factor must be
          a multiple of 11, which reduces the search space.
        • Palindrome values decrease non-linearly due to base-10 positional weights, creating step-like transitions at
          powers of 10.
        • This allows efficient top-down search: the first valid factorization yields the maximum palindrome.
        • This func finds the following instances efficiently:
            Power  Palindrome                 1st factor     2nd factor
            12     999999000000000000999999 = 999999999999 * 999999000001
            11      9999994020000204999999     99999996349   99999943851
            10       99999834000043899999       9999996699   9999986701
            9         999900665566009999         999980347   999920317
            8          9999000000009999           99999999   99990001
            7           99956644665999             9998017   9997647
            6            999000000999               999999   999001
            5             9966006699                 99979   99681
            4              99000099                   9999   9901
            3               906609                     993   913
            2                9009                       99   91

    Examples:
        C1.palindrome(11) == 9999994020000204999999
    """
    hf = int('9' * (r - 1) + '0')
    up = int('9' * (r - 1) + ('0', '9')[r % 2 == 0])
    step = (1, 10)[r % 2 == 0 or r > 9]  # empirically chosen step to skip redundant candidates
    while True:
        p = int(str(hf) + str(hf)[::-1])
        for f in range(up, hf, -11):
            if p % f == 0:
                return p
        hf -= step
