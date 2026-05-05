# For all examples first: import B2_text_parsing as B2


import re


TURN = {**{k: str(v) for v, k in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split())},
        **{k: str(10 * v) for v, k in enumerate('twenty thirty forty fifty sixty seventy eighty ninety hundred'.split(), 2)},
        **{k: str(1000 ** v) for v, k in enumerate('thousand million etc.'.split(), 1)}}

def cast(match):
    m = TURN.get(match[0], '')
    return ('*' if '100' in m else '+' * bool(m)) + m

def parse_int(text):
    """
    Interpret integers.

    Source:
        https://www.codewars.com/kata/525c7c5ab6aecef16e0001a5

    Examples:
        tst = [B2.parse_int(s) for s in ('one', 'twenty', 'two hundred forty-six',
                                         'seven hundred eighty-three thousand nine hundred and nineteen',
                                         'six hundred forty-seven million seven hundred eighty-three thousand nine hundred and nineteen')]
        tst == [1, 20, 246, 783919, 647783919]
    """
    return eval(re.sub(r'(?<=\+)(.+?)(?=\*1000)', r'(\1)', re.sub(r'\b[a-z]+\b|-', cast, text)))


def simplify_polynom(text):
    """
    Simplifying multilinear polynomials.

    Source:
        https://www.codewars.com/kata/55f89832ac9a66518f000118

    Examples:
        tst = [B2.simplify_polynom(s) for s in ('dc+dcba', '2xy-yx', '-a+5ab+3a-c-2a', '-abc+3a+2ac', 'xyz-xz', 'a+ca-ab',
                                                'xzy+zby', '-y+x', 'y-x', 'b+4a-ab+4ac', '-kq+3fk+5kv-2qvy+fkqvy')]
        tst == ['cd+abcd', 'xy', '-c+5ab', '3a+2ac-abc', '-xz+xyz', 'a-ab+ac', 'byz+xyz', 'x-y', '-x+y', '4a+b-ab+4ac',
                '3fk-kq+5kv-2qvy+fkqvy']
    """
    poly = [[p[0], ''.join(sorted(p[1]))] for p in re.findall(r'([+-]\d*)([a-z]+)',
                                                              re.sub(r'^(?=\w)', r'+', text))]
    for i in range(len(poly) - 1):
        if poly[i] != ('', ''):
            for j in range(i + 1, len(poly)):
                if poly[i][1] == poly[j][1]:
                    poly[j][0] = re.sub(r'^(?=\d)', r'+',
                                        str(eval(re.sub(r'(?<=[+-])(?:(?=[+-])|$)',
                                                        r'1', poly[i][0] + poly[j][0]))))
                    poly[i] = ('', '')
                    poly[j] = [re.sub(r'\b1$', r'', poly[j][0]), poly[j][1]] if int(poly[j][0]) else ('', '')
                    break
    return re.sub(r'^\+', r'', ''.join(''.join(p) for p in sorted(poly, key=lambda v: (len(v[1]), v[1]))))


def top_3_words(text):
    """
    Most frequently used words in a text.

    Source:
        https://www.codewars.com/kata/51e056fe544cf36c410000fb

    Notes:
        The only pattern solve:
            (?<!['a-z])(?<![a-z]-)('?(?:[a-z](?:[-'][a-z])*)+'?)(?!-[a-z])(?![a-z'])(.+)?(?<!['a-z])(?<![a-z]-)\1(?!-[a-z])(?![a-z'])

    Examples:
        long_text = ("In a village of La Mancha, the name of which I have no desire to call to\n        mind, there lived"
                    "not long since one of those gentlemen that keep a lance\n        in the lance-rack, an old buckler,"
                    "a lean hack, and a greyhound for\n        coursing. An olla of rather more beef than mutton, a salad"
                    "on most\n        nights, scraps on Saturdays, lentils on Fridays, and a pigeon or so extra\n        "
                    "on Sundays, made away with three-quarters of his income.")
        tst = [B2.top_3_words(p) for p in ("e e e e DDD ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e",
                                           "  //wont won't won't ", "  , e   .. ","'ab', 'ab, 'ab', ab'",
                                           "ab', 'ab, 'ab', 'ab","'ab, ab', 'ab', ab'", "  ...  ", "  '  ", "  '''  ",
                                           long_text)]
        tst == [["e", "ddd", "aa"], ["won't", "wont"], ["e"], ["'ab'", "'ab", "ab'"], ["'ab", "ab'", "'ab'"],
                ["ab'", "'ab", "'ab'"], [], [], [], ["a", "of", "on"]]
    """
    rule_wd = r"'?(?:[a-z]['a-z]*)+"
    rule = r"{0}({1}){2}.+?{0}\1{2}".format("(?<!['a-z])", rule_wd, "(?![a-z'])")
    words, start = {}, 0
    match = re.search(rule, text, flags=re.IGNORECASE+re.DOTALL)
    while match:
        wd = match[1].lower()
        words[wd] = (words[wd] + 1) if wd in words else 2
        start += match.end(1)
        match = re.search(rule, text[start:], flags=re.IGNORECASE+re.DOTALL)
    if len(words) < 3:
        for wd in re.findall(rule_wd, text, flags=re.IGNORECASE):
            words.setdefault(wd.lower(), 1)
    return [wd[0] for wd in sorted(words.items(), key=lambda v: v[1], reverse=True)[:3]]


WASTE = ('the', 'of', 'in', 'from', 'by', 'with', 'and', 'or', 'for', 'to', 'at', 'a')

def generate_bc(url, sep):
    """
    Breadcrumb generator.

    Source:
        https://www.codewars.com/kata/563fbac924106b8bf7000046

    Examples:
        tst = [B2.generate_bc(*p) for p in (('www.agcpartners.co.uk/', ' * '),
                                            ('linkedin.it', ' : '),
                                            ("mysite.com/pictures/holidays.html", " : "),
                                            ("https://www.codewars.com/users/GiacomoSorbi?ref=CodeWars", " / "),
                                            ("www.microsoft.com/important/confidential/docs/index.htm#top", " * "),
                                            ("mysite.com/very-long-url-to-make-a-silly-yet-meaningful-example/example.asp", " > "),
                                            ("www.very-long-site_name-to-make-a-silly-yet-meaningful-example.com/users/giacomo-sorbi", " + "))]
        tst == ['<span class="active">HOME</span>',
                '<span class="active">HOME</span>',
                '<a href="/">HOME</a> : <a href="/pictures/">PICTURES</a> : <span class="active">HOLIDAYS</span>',
                '<a href="/">HOME</a> / <a href="/users/">USERS</a> / <span class="active">GIACOMOSORBI</span>',
                '<a href="/">HOME</a> * <a href="/important/">IMPORTANT</a> * <a href="/important/confidential/">CONFIDENTIAL</a> * <span class="active">DOCS</span>',
                '<a href="/">HOME</a> > <a href="/very-long-url-to-make-a-silly-yet-meaningful-example/">VLUMSYME</a> > <span class="active">EXAMPLE</span>',
                '<a href="/">HOME</a> + <a href="/users/">USERS</a> + <span class="active">GIACOMO SORBI</span>']
    """
    url = re.sub(r'(?:/index|[.?#]).+$|/$', r'', re.sub(r'^(?:.+/{2})*[^/]+', r'HOME', url)).split('/')
    acronyms = {url.index(s): ''.join('' if w in WASTE else w[0] for w in s.split('-')) for s in url[1:] if len(s) > 30}
    for i in range(len(url)-2, -1, -1):
        url[i] = '<a href="/{}">{}</a>'.format('/'.join(url[1:i + 1]) + '/' * (i > 0),
                                               re.sub(r'-', r' ', acronyms.get(i, url[i]).upper()))
    return sep.join((*url[:-1], '<span class="active">{}</span>'.format(re.sub(r'-', r' ',
                                                                               acronyms.get(url.index(url[-1]), url[-1]).upper()))))


def parse_emails(text):
    """
    Parse emails based on the simplified RFC5322 standard.

    Notes:
        • Email = local part + @ + domain.
        • Local part: ≤64 chars, {a÷zA÷Z0÷9.-+'_}.
        • Domain: ≤255 chars, {a÷zA÷Z0÷9.-}.
        • No leading/trailing {.-+'} chars in either part.
        • No repeating {@@ .. -- ++ '' .-+'} chars in either part.
        • An email may appear inside a larger token.
        • The common logic rule:
            ≠⊄1÷64{A+'_}≠@≠⊄1÷256{A}≠  A{a÷zA÷Z0÷9.-}  ≠{.-+'}  ⊄{@@ .. -- ++ '' .-+'}

    Examples:
        tst = B2.parse_emails("Ну@жен ответ от +_0iv__An1.0@3ivn-4c.ai56.7aB. Н9@3абудьте проверить !!__ser91upin__@m.ab- "
                              "это важно (f+@ya, f@oo@y-a, f++oo@ya.ab80., @6boo@ya.a7b, Бфboo@ya_ab, f'+f'oo@y-a, f@y, "
                              "_@0._ 1234567890_+_'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz@66@)")
        tst == ['_0iv__An1.0@3ivn-4c.ai56.7aB', '9@3', '__ser91upin__@m.ab', 'f@oo', 'oo@ya.ab80', '6boo@ya.a7b', 'boo@ya',
                "f'oo@y-a", 'f@y', '_@0', "34567890_+_'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz@66"]
    """
    return re.findall(r"(?:\w|(?<=\w)[+'.-](?=\w)){{1,64}}@(?:{p}|(?<={p})[.-](?={p})){{1,256}}".format(p=r'[a-zA-Z\d]'),
                      text, flags=re.ASCII)


def parse_phones(strings):
    """
    Parse phone numbers.

    Source:
        https://www.codewars.com/kata/57a492607cb1f315ec0000bb

    Notes:
        • Use regex with capturing groups to match phone structure.
        • Extract parts (e.g.: area, prefix, line) via groups.
        • Return structured components from a single match.

    Examples:
        tst = ('0012 34 567890', '+12 34 567890', '034 567890', '34 567890', '567890', '12 34 567890', '+01 34 567890',
               '+12 04 567890', '+12 34 067895', '004 567890', '098765', '+12 034 567890', '+ab cd efghig', 'a+12 34 567890',
               ' +21 45 567890', '567890 ', '34567890')
        B2.parse_phones(tst)
    """
    rule = r'^(?:(?:\+|00)([1-9]\d) )?(?:((?:^0)?[1-9]\d) )?([1-9]\d{5})$'
    result = []
    for s in strings:
        m = re.search(rule, s)
        result.append(f'{s}, [{f'{m[1]}, {m[2]}, {m[3]}' if m else ''}]')
    return result


def sci_notation(text):
    """
    Validate real form of numbers.

    Notes:
        • Must have a decimal point, exponent, or both.
        • Decimal point requires digits on both sides.
        • The exponent (e/E) must be an integer.
        • Optional +/- at start and/or exponent.
        • No inner spaces; outer spaces allowed.

    Examples:
        tst = '1.2 \n  1. \n    1.0e-55  \n      e-12   \n  6.5E \n        1e-12  \n  +4.1234567890E-99999           \n  7.6e+12.5 \n   9 '
        B2.sci_notation(tst)
    """
    result = []
    for num in re.findall(r'\S+', text):
        r = f'{num} is {'' if re.fullmatch(r'[-+]?[1-9](?:(?:\.\d+)?[eE][-+][1-9]\d{,4}|\.\d+)', num) else 'il'}legal.'
        result.append(r)
    return result
