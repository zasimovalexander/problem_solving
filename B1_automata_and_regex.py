import re

PATT_DIV = {3: r'^(?:0|1(?:01*0)*1)*$',
            5: r'^(0|1(10)*(0|11)(01*0(01)*(1|00))*1)+$'}

def bin_div_3_5(mode: int,
                bit_strings: tuple[str, ...]) -> list[str]:
    """
    Finite state machines for checking binary numbers divisible by 3 or 5.

    Idea:
        Build a finite state machine (FSM) where each state represents the remainder of a binary number modulo N (3|5):
            • Read the binary string from left to right:
            • Each new bit updates the current state (remainder).
            • Accepting states correspond to a remainder = 0, meaning the number is divisible by N.
            • The FSM is then converted into a regular expression.
    Source:
         https://www.codewars.com/kata/5647c3858d4acbbe550000ad

    Notes:
        • Finite State Machines checking binary numbers divisible by 3:
              ┌───1─>─┐ ┌───0─>─┐   │
            •(A)<─0   (B)   1─>(C)  │  ((0))<─1─>()<─0─>(1)
              └─<─1───┘ └─<─0───┘   │
        • Finite State Machines checking binary numbers divisible by 5:
               ┌────── ← 1 ────────┐     │
            0→(A)── 1 → (B)── 0 → (C)    │    |<-----1-----------|<-----1----------|
               •        │ ↑     🡥  │     │  ((A|0))--1->(B)--0->(C)--0->(D|1)--0->(E)
                        1 0   1    0     │               |<-----0- - - - - -1----->|
                        ↓ │ ╱      ↓     │
                        (E) ← 0 ──(D)←1  │

    Examples:
        import B1_automata_and_regex as B1
        B1.bin_div_3_5(3, ('00','11','110','11011','10010','11000','11110','101111000110000101001110','001101010000110001'))
        B1.bin_div_3_5(3, ('100','010','001','111',' 0','1 10','abc','abc11','1011100100001011000'))
        B1.bin_div_3_5(5, ('00', '101', '1010', '10100', '1111110111111100', '0010111000010100100111001'))
        B1.bin_div_3_5(5, ('10110101', '101001000', ' 0', '1 01', 'abc', 'abc101'))
    """
    try:
        patt = PATT_DIV[mode]
    except KeyError:
        raise ValueError("Mode must be 3 or 5")
    result = []
    for bs in bit_strings:
        prefix = 'is' if re.fullmatch(patt, bs) else 'not'
        result.append(f'{prefix}/{mode}:"{bs}"')
    return result
