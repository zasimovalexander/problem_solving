from itertools import cycle

ABC = 'abcdefghijklmnopqrstuvwxyz'

class VigenereCipher:
    """
    Vigenere Cipher helper.

    Idea:
        Processes text character by character using a repeating key. Instead of the classical 2D Vigenere square
        (row/column intersection), the implementation uses a set of shifted alphabets (column-based mapping), reducing
        the transformation to direct index lookup.
    Source:
        https://www.codewars.com/kata/52d1bd3694d26f8d6e0000d3

    Notes:
        In this method, the key and the original/encrypted text depend on the alphabet, and the algorithm works as
        follows (from a coding perspective):
            • Build a reference map of alphabets, each shifted left by one position relative to its predecessor (similar
              to the Vigenere square).
            • Form a string (mask) by repeating the key until it matches the length of the text.
            • When encrypting, for each character in the original text (if it belongs to the alphabet; otherwise, it is
              written as is): find its index in the original alphabet -> write the character from the shifted alphabet
              that starts with the character at the same position in the mask.
            • For decrypting, the same process, but the search is in the shifted alphabet, and the write is from
              the original alphabet.
        Practical notes:
            • A short key, a small alphabet, or an overly long message reduces the method’s resilience.
            • A long random key and a unique alphabet increase it.
            • Currently, the method is weak on its own and is recommended as an additional encryption layer. For example,
              to strengthen a previous field-level method: form a card-based key (deck shuffle) or re-encode a message.
            • Resilience can also be improved by using a non-standard alphabet, excluding certain letters, or increasing
              the number and variety of ignored symbols (including excluded characters).

    Examples:
        from A1_cryptography import VigenereCipher
        tst = VigenereCipher('password')
        [tst.encrypt(s) for s in ('waffles', "it's a shiFt cipher!")] == ['laxxhsj', "xt'k o vwiFl qzswej!"]
        [tst.decrypt(s) for s in ("xt'k o vwiFl qzswej!", 'laxxhsj')] == ["it's a shiFt cipher!", 'waffles']
        tst = VigenereCipher('カタカナ', 'アイウエオァィゥェォカキクケコサシスセソタチツッテトナニヌネノハヒフヘホマミムメモヤャユュヨョラリルレロワヲンー')
        tst.encrypt('ドモアリガトゴザイマス') == 'ドオカセガヨゴザキアニ'
        tst.decrypt('ドオカセガヨゴザキアニ') == 'ドモアリガトゴザイマス'
    """

    def __init__(self,
                 key: str,
                 abc: str =ABC):
        self.key = key
        self.map = {abc[idx]: abc[idx:] + abc[:idx] for idx in range(len(abc))}  # like columns in the Vigenere Square
        self.k_orig = abc[0]  # the original form of the alphabet is already available by this key in the hash map

    def __action(self,
                 text: str,
                 mode: int) -> str:
        """
        Perform bidirectional transformation (modes: 0 - encryption, 1 - decryption).
        """
        veil = ''.join(k for k, _ in zip(cycle(self.key), text))  # key = 'sun', text = 'morning' -> 'sunsuns'
        result = []
        origin = set(self.map[self.k_orig])  # for faster search
        for idx, ch in enumerate(text):
            if ch in origin:
                k = [self.k_orig, veil[idx]]  # the mode-keys for the appropriate alphabet
                i = self.map[k[mode]].index(ch)  # an original char index in the appropriate alphabet
                k.reverse()  # the next mode-keys for the appropriate alphabet
                result.append(self.map[k[mode]][i])  # an en/de_crypted symbol
            else:
                result.append(ch)
        return ''.join(result)

    def encrypt(self,
                text: str) -> str:
        return self.__action(text, 0)

    def decrypt(self,
                text: str) -> str:
        return self.__action(text, 1)


MAP = {}
for suit in ('CSB', 'DHR'):
    hh = {}
    for abc_suit in (('ABCDEFGHIJKLM', suit[0]), ('NOPQRSTUVWXYZ', suit[1])):
        for card_abc in zip('A23456789TJQK', abc_suit[0]):
            hh[card_abc[0] + abc_suit[1]] = card_abc[1]
    hh['X' + suit[2]] = ' '  # the Joker card acts as space
    MAP[suit[2]] = {'chr': hh, 'crd': {v: k for k, v in hh.items()}}

class CardChameleon:
    """
    Card-Chameleon, a cipher with playing cards.

    Idea:
        Implementation of a card-driven stream cipher where the deck acts as mutable state. Each symbol is transformed
        via chained card lookups with positional shifts, producing a keystream-dependent substitution. After each step,
        the deck is mutated (swap + rotation), ensuring state evolution and non-repeating output. Encryption and
        decryption share the same pipeline with inverted traversal rules.
    Source:
        https://www.codewars.com/kata/card-chameleon-a-cipher-with-playing-cards

    Notes:
        The cryptographic key is represented by the order of the cards in the deck (the sender and the recipient must
        start the process with the same key). The alphabet and cards must be related as follows:
                     Clubs & Diamonds                 Spades & Hearts
        A 2 3 4 5 6 7 8 9 T J Q K X     A 2 3 4 5 6 7 8 9 T J Q K X
        A B C D E F G H I J K L M " "   N O P Q R S T U V W X Y Z " "
        therefore the dict "MAP" includes the black, and the red hashes considering both request (cards, letters):
        {'B': {'chr': {'AC': 'A', '2C': 'B', '3C': 'C', '4C': 'D', '5C': 'E', '6C': 'F', '7C': 'G', '8C': 'H', '9C': 'I',
                       'TC': 'J', 'JC': 'K', 'QC': 'L', 'KC': 'M', 'AS': 'N', '2S': 'O', '3S': 'P', '4S': 'Q', '5S': 'R',
                       '6S': 'S', '7S': 'T', '8S': 'U', '9S': 'V', 'TS': 'W', 'JS': 'X', 'QS': 'Y', 'KS': 'Z', 'XB': ' '},
               'crd': {'A': 'AC', 'B': '2C', 'C': '3C', 'D': '4C', 'E': '5C', 'F': '6C', 'G': '7C', 'H': '8C', 'I': '9C',
                       'J': 'TC', 'K': 'JC', 'L': 'QC', 'M': 'KC', 'N': 'AS', 'O': '2S', 'P': '3S', 'Q': '4S', 'R': '5S',
                       'S': '6S', 'T': '7S', 'U': '8S', 'V': '9S', 'W': 'TS', 'X': 'JS', 'Y': 'QS', 'Z': 'KS', ' ': 'XB'}},
         'R': {'chr': {'AD': 'A', '2D': 'B', '3D': 'C', '4D': 'D', '5D': 'E', '6D': 'F', '7D': 'G', '8D': 'H', '9D': 'I',
                       'TD': 'J', 'JD': 'K', 'QD': 'L', 'KD': 'M', 'AH': 'N', '2H': 'O', '3H': 'P', '4H': 'Q', '5H': 'R',
                       '6H': 'S', '7H': 'T', '8H': 'U', '9H': 'V', 'TH': 'W', 'JH': 'X', 'QH': 'Y', 'KH': 'Z', 'XR': ' '},
               'crd': {'A': 'AD', 'B': '2D', 'C': '3D', 'D': '4D', 'E': '5D', 'F': '6D', 'G': '7D', 'H': '8D', 'I': '9D',
                       'J': 'TD', 'K': 'JD', 'L': 'QD', 'M': 'KD', 'N': 'AH', 'O': '2H', 'P': '3H', 'Q': '4H', 'R': '5H',
                       'S': '6H', 'T': '7H', 'U': '8H', 'V': '9H', 'W': 'TH', 'X': 'JH', 'Y': 'QH', 'Z': 'KH', ' ': 'XR'}}}

    Examples:
        from random import sample; from A1_cryptography import CardChameleon
        DECK = ['AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AS', '2S', '3S', '4S',
                '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'XB', 'AD', '2D', '3D', '4D', '5D', '6D', '7D',
                '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
                'QH', 'KH', 'XR']
        message, deck = 'THIS IS A SIMPLE EXAMPLE', sample(DECK, len(DECK))
        tst_en = CardChameleon(message, deck)
        egassem = tst_en.encrypt()
        tst_de = CardChameleon(egassem, deck)
        tst_de.decrypt() == message
    """

    def __init__(self,
                 message: str,
                 deck: list[str]):
        self.__validate(message, deck)
        self.message = message
        self.deck = tuple(deck)

    @staticmethod
    def __validate(msg: str,
                   dck: list[str]):
        if any(ch not in set(MAP['B']['crd']) for ch in msg):
            raise ValueError("Invalid message characters")
        if set(dck) != set(MAP['B']['chr']) | set(MAP['R']['chr']):
            raise ValueError("Deck must be a permutation of valid cards")
        if len(msg) > len(dck):
            raise ValueError("Message too long for deck size")

    def __prepare_deck(self) -> list[str]:
        """
        A deck is modeled as face-up (index 0 = top), and all operations preserve order (no implicit reversals):
            • splitting appends to the bottom (keeps original order)
            • interleaving builds a deck top-to-bottom directly
        this avoids double-reversal behavior as opposed to manual mixing.
        """
        separated = ([], [])
        for crd in self.deck:  # separating cards according to color for two piles (red, black)
            is_black = any(ch in crd for ch in 'CSB')
            separated[is_black].append(crd)
        mix = []
        for pair in zip(separated[0], separated[1]):  # interleaving cards to one deck
            mix.extend(pair)
        return mix

    def __action(self,
               color: str,
               shift: int,
               mode: int) -> str:
        """
        Perform bidirectional transformation (modes: 0 - encryption, 1 - decryption).
        """
        mix_deck = self.__prepare_deck()
        result = []
        for i in range(len(self.message)):
            card1 = MAP[color[0]]['crd'][self.message[i]]  # the 1st card corresponding to a message char
            card = mix_deck[mix_deck.index(card1) - shift]  # the 2nd card above/below the 1st card in the deck
            char = MAP[color[1]]['chr'][card]  # the char of the 2nd card
            card = MAP[color[0]]['crd'][char]  # the 3rd card corresponding to the char of the 2nd card
            card4 = mix_deck[mix_deck.index(card) - shift]  # the 4th card above/below the 3rd card in the deck
            result.append(MAP[color[1]]['chr'][card4])  # the char of the 4th card (en/de_crypted symbol)
            index = mix_deck.index((card4, card1)[mode])  # the 4th/1st red card corresponding to en/de_cryption scenario
            mix_deck[index], mix_deck[0] = mix_deck[0], mix_deck[index]  # exchange with the red card on top of the deck
            mix_deck = mix_deck[2:] + mix_deck[:2]  # top pair of cards to the bottom (red and black)
        return ''.join(result)

    def encrypt(self) -> str:
        return self.__action('BR', 1, 0)

    def decrypt(self) -> str:
        return self.__action('RB', -1, 1)
