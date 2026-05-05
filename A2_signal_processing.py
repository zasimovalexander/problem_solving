from re import split as re__split

MAP_MORSE = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I',
             '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
             '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '-----': '0',
             '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
             '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!', '-..-.': '/',
             '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
             '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '...---...': 'SOS'}

def decode_bits_advanced(bits: str) -> str:
    """
    Decode the Morse Code for real.

    Idea:
        Normalize unknown transmission speed by extracting base time unit from run-lengths of 1 and 0, then classify
        each segment using adaptive thresholds to map into dot/dash and intra/inter-character/word gaps.
    Source:
        https://www.codewars.com/kata/decode-the-morse-code-for-real

    Notes:
        1. Problem: basic time unit of signal K is unknown (variable transmission speed, K ≥ 1)
        2. Approach: collect run lengths -> estimate K -> classify using thresholds
        3. The Morse Code timing and representation (signal model):
            Action          Inside Morse   Time units  Bits pattern
            -------------------------------------------------------
            dot             .              1           '1' * 1 * K
            dash            -              3           '1' * 3 * K
            pause_dot/dash  inside char    1           '0' * 1 * K
            pause_chars     between chars  3           '0' * 3 * K
            pause_words     space          7           '0' * 7 * K
        4. Observations:
            1st sample: '110110100111000001100000011111101001111100111111000000000001110111111110111110111110000001011000
                         111111000001111100111011000001'
                on-off pairs: 2, 1,  2, 1,  1, 2,  3, 5,  2, 6,  6, 1,  1, 2,  5, 2,  6, 11,  3, 1,  8, 1,  5, 1,  5, 6,
                              1, 1,  2, 3,  6, 5,  5, 2,  3, 1,  2, 5,  1
                statistic:    dot(1-3), dash(5-8), pause_dot/dash(1-3), pause_chars(5-6), pause_words(11)
                morse → text: . . . .   .   - . - -     . - - -   . . -   - . .   .
                              H         E   Y           J         U       D       E
            2nd sample: '111111100000011010001110111000000001110000000000000000001111111011111100001101111100000111100111
                         100011111100000001011100000011111110010001111100110000011111100101111100000000000000111111100001
                         111010110000011000111110010000011111110001111110011111110000010001111110001111111100000001111111
                         101110000000000000010110000111111110111100000111110111110011111110000000011111001011011111000000
                         000000111011111011111011111000000010001001111100000111110111111110000001110011111100011111010000
                         001100001001000000000000000000111111110011111011111100000010001001000011111000000100000000101111
                         101000000000000011111100000011110100001001100000000001110000000000000001101111101111000100000100
                         001111111110000000001111110011111100011101100000111111000011011111000111111000000000000000001111
                         110000100110000011111101111111011111111100000001111110001111100001'
                on-off pairs: 7, 6,  2, 1,  1, 3,  3, 1,  3, 8,  3, 18,  7, 1,  6, 4,  2, 1,  5, 5,  4, 2,  4, 3,  6, 7,
                              1, 1,  3, 6,  7, 2,  1, 3,  5, 2,  2, 5,  6, 2,  1, 1,  5, 14,  7, 4,  4, 1,  1, 1,  2, 5,
                              2, 3,  5, 2,  1, 5,  7, 3,  6, 2,  7, 5,  1, 3,  6, 3,  8, 7,  8, 1,  3, 14,  1, 1,  2, 4,
                              8, 1,  4, 5,  5, 1,  5, 2,  7, 8,  5, 2,  1, 1,  2, 1,  5, 12,  3, 1,  5, 1,  5, 1,  5, 7,
                              1, 3,  1, 2,  5, 5,  5, 1,  8, 6,  3, 2,  6, 3,  5, 1,  1, 6,  2, 4,  1, 2,  1, 18,  8, 2,
                              5, 1,  6, 6,  1, 3,  1, 2,  1, 4,  5, 6,  1, 8,  1, 1,  5, 1,  1, 13,  6, 6,  4, 1,  1, 4,
                              1, 2,  2, 10,  3, 15,  2, 1,  5, 1,  4, 3,  1, 5,  1, 4,  9, 9,  6, 2,  6, 3,  3, 1,  2, 5,
                              6, 4,  2, 1,  5, 3,  6, 17,  6, 4,  1, 2,  2, 5,  6, 1,  7, 1,  9, 7,  6, 3,  5, 4,  1
                statistic:    dot(1-4), dash(5-9), pause_dot/dash(1-4), pause_chars(5-10), pause_words(12-18)
                morse → text: -   . . . .   .     - - . -   . . -   . .   - . - .   - . -     - . . .   . - .   - - -
                              T   H         E     Q         U       I     C         K         B         R       O
                              . - -   - .     . . - .   - - -   - . . -     . - - -   . . -   - -   . - - .   . . .
                              W       N       F         O       X           J         U       M     P         S
                              - - -   . . . -   .   . - .     -   . . . .   .     . - . .   . -   - - . .   - . - -
                              O       V         E   R         T   H         E     L         A     Z         Y
                              - . .   - - -   - - .
                              D       O       G

    Examples:
        import A2_signal_processing as A2
        tst = ('1001', '10001', '100001', '10000001', '100000001', '1000000001', '10000000001', '10111', '111',
               '1111111', '101', '110011', '111000111', '111110000011111', '1110111', '11111100111111',
               '110110100111000001100000011111101001111100111111000000000001110111111110111110111110000001011000111111000001111100111011000001',
               '1100110011001100000011000000111111001100111111001111110000000000000011001111110011111100111111000000110011001111110000001111110011001100000011',
               '111111100000011010001110111000000001110000000000000000001111111011111100001101111100000111100111100011111100000001011100000011111110010001111100110000011111100101111100000000000000111111100001111010110000011000111110010000011111110001111110011111110000010001111110001111111100000001111111101110000000000000010110000111111110111100000111110111110011111110000000011111001011011111000000000000111011111011111011111000000010001001111100000111110111111110000001110011111100011111010000001100001001000000000000000000111111110011111011111100000010001001000011111000000100000000101111101000000000000011111100000011110100001001100000000001110000000000000001101111101111000100000100001111111110000000001111110011111100011101100000111111000011011111000111111000000000000000001111110000100110000011111101111111011111111100000001111110001111100001')
        encrypted = [A2.decode_morse(A2.decode_bits_advanced(s)) for s in tst]
        encrypted == ['EE', 'EE', 'EE', 'E E', 'E E', 'E E', 'E E', 'A', 'E', 'E', 'I', 'I', 'I', 'I', 'M', 'M',
                      'HEY JUDE', 'HEY JUDE', 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG']
    """
    bits = bits.strip('0')  # remove leading/trailing noise (extra zeros)
    # extract run-lengths of consecutive '1' and '0' (represent signal durations in unknown time units k)
    runs = [sorted(set(map(len, re__split(b + '+', bits.strip(b)))), reverse=True) for b in ('1', '0')]
    # estimate thresholds based on observed run lengths:
    # shortest runs ≈ base time unit (k), others are multiples (≈3k, ≈7k)
    if len(runs[0] + runs[1]) == 2 and runs[0][0] >= runs[1][0] or runs[0][0] == 0:
        # approximate threshold between char (~3k) and word (~7k) gaps, using averaged boundary instead of strict multiples
        thr_char_gap = runs[1][0]
        thr_word_gap = 4.0 * runs[1][0]  # = (7 * runs[1][0] + runs[1][0]) / 2
    else:
        # more general case: derive thresholds from both '1' and '0' runs; boundary between a dot/dash and longer pauses
        thr_char_gap = runs[1][0] / 2
        thr_word_gap = (runs[1][0] / 2 + runs[0][0]) / 2
    # for '1' map durations to dot or dash, and for '0' do it to gaps: inside char and between chars/words
    for rules in ((runs[0], (thr_char_gap, thr_word_gap), '0', (' ', '   ')),
                  (runs[1], (0, thr_char_gap), '1', ('.', '-'))):
        for k in rules[0]:
            # compare run length k against thresholds: decide whether it's short or long signal/gap
            if k > rules[1][k > rules[1][1]]:
                # replace all runs of length k with corresponding symbol;
                # safe here because runs are processed by distinct lengths
                bits = bits.replace(rules[2] * k, rules[3][k > rules[1][1]])
    return bits.replace('0', '')  # remove remaining '0' (intra-char gaps are already processed)

def decode_morse(morse_code: str) -> str:
    """
    Return decoded characters.
    """
    return ' '.join(''.join(MAP_MORSE[char] for char in word.split()) for word in morse_code.split('   '))
