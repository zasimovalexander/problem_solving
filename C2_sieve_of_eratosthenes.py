"""
Index-based sieve laboratory.

Idea:
    Work in index space (i → 2i+1) instead of direct integer space. The starting point for marking composites is
    expressed as 2i(i+1), which corresponds to (2i+1)^2 mapped into index form.

Notes:
    This file mixes stable implementations with exploratory ideas. Some parts are intentionally experimental and
    may trade clarity for observation. Code reuse and structural abstraction are intentionally minimized to avoid
    overhead in hot paths.

Researching ideas:
    • Used:
        up //= 2 → up >>= 1
    • Maybe:
        [False] + [True] * (up - 1) → bytearray([0]) + bytearray([1] * (up - 1))
"""


# --- BASE IMPLEMENTATIONS ---

def sieve(up):
    """
    High-level implementation of a lazy prime number generator based on the classical Sieve of Eratosthenes.

    Idea:
        • Focuses on iterating through a sequential range of odd integers.
        • Each sieve cell’s boolean value directly corresponds to the ordinal index of the number it represents.
        • Uses index-based logic when iterating over cells, adjusting the starting index and step to avoid
          redundant marking operations.
        • This optimization relies on the fact that each cell is directly associated with its corresponding number:
          (a * a) // 2 |a = 2i + 1| = 2i^2 + 2i = 2i(i + 1)
    """
    yield 2
    up >>= 1
    sv = [False] + [True] * (up - 1)
    for (i, ver) in enumerate(sv):
        if ver:
            ix2 = 2 * i
            a = ix2 + 1
            yield a
            for j in range(ix2 * i + ix2, up, a):
                sv[j] = False

def sieve_max_prime(up):
    """
    Non-lazy prime generator used to find the maximum prime within a range.
    """
    up >>= 1
    sv = [False] + [True] * (up - 1)
    for (i, ver) in enumerate(sv):
        if ver:
            ix2 = 2 * i
            a = ix2 + 1
            for j in range(ix2 * (i + 1), up, a):
                sv[j] = False
    for i in range(up - 1, 0, -1):
        if sv[i]:
            return 2 * i + 1
    return 2


# --- EXPERIMENTAL ---

def sieve_shrink(up):
    """
    Bidirectional, dynamically shrinking modification of the "sieve" approach for experimental prime factorization.
        • The upper bound and active range of cells are reduced via "send()", in response to the decreasing size of
          the number being factorized.
        • Slower than direct trial division, but useful for studying adaptive sieve behavior with dynamic boundaries.

    Notes:
        The algorithm performance increases when trying to influence the following blocks:
            • prm * prm <= number
            • cnt
    """
    new_up = (yield 2)
    if new_up:
        up = new_up
    up >>= 1
    sv = [False] + [True] * (up - 1)
    for (i, ver) in enumerate(sv):
        if ver:
            ix2 = 2 * i
            a = ix2 + 1
            new_up = (yield a)  # external control: new upper bound via send()
            if new_up:
                up = new_up >> 1
                sv = sv[:up]  # shrink active range
            for j in range(ix2 * (i + 1), up, a):
                sv[j] = False


# --- APPLICATIONS ---

def prime_factors(number):
    powers = {}
    gen_prime = sieve_shrink(int(number ** 0.5) + 1)
    prm = next(gen_prime)
    while prm * prm <= number:
        cnt = 0
        while number % prm == 0:
            number //= prm
            cnt += 1
        try:
            if cnt:
                powers[prm] = cnt
                prm = gen_prime.send(int(number ** 0.5) + 1)
            else:
                prm = next(gen_prime)
        except StopIteration:
            break
    if number > 1:
        powers[number] = 1
    return powers
