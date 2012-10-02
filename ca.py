# -*- coding: utf-8 -*-
"""
Prime calculating automaton

Ref:
  http://www.wolframscience.com/nksonline/page-1109
"""
LETTERS = u'　｜・３１２：＞≫／米①②＼Ｘノ'
ANY = None

# typedef (ANY | [Int] | Int) Match
# rules :: [((Match, Match, Match), Int)]
rules = [
    ((13, 3, 13), 12),
    ((6, ANY, 4), 15),
    ((10, ANY, [3, 11]), 15),
    ((13, 7, ANY), 8),
    ((13, 8, 7), 13),
    ((15, 8, ANY), 1),
    ((8, ANY, ANY), 7),
    ((15, 1, ANY), 2),
    ((ANY, 1, ANY), 1),
    ((1, ANY, ANY), 8),
    (([2, 4, 5], ANY, ANY), 13),
    ((15, 2, ANY), 4),
    ((ANY, 4, 8), 4),
    ((ANY, 4, ANY), 5),
    ((ANY, 5, ANY), 3),
    ((15, 3, ANY), 12)
] + [
    ((ANY, x, ANY), x) for x in [2, 3, 8]
] + [
    ((ANY, x, ANY), x-1) for x in [11, 12]
] + [
    ((11, ANY, ANY), 13),
    ((13, ANY, [1, 2, 3, 5, 6, 10, 11]), 15),
    ((13, 0, 8), 15),
    ((14, ANY, [6, 10]), 15),
    ((10, [0, 9, 13], [6, 10]), 15),
    ((6, ANY, 6), 0),
    ((ANY, ANY, 10), 9),
    (([6, 10], 15, 9), 14),
    ((ANY, [6, 10], [9, 14, 15]), 10),
    ((ANY, [6, 10], ANY), 6),
    (([6, 10], 15, ANY), 13),
    (([13, 14], ANY, [9, 15]), 14),
    (([13, 14], ANY, ANY), 13),
    ((ANY, ANY, 15), 15),
    ((ANY, ANY, [9, 14]), 9),
    ((ANY, ANY, ANY), 0)
]

def _to_char(x):
    if isinstance(x, list):
        return u"[%s]" % "".join(map(_to_char, x))
    if isinstance(x, int):
        return LETTERS[x]
    if x == None:
        return u"＊"
    raise AssertionError('not here', x)


def show_rules():
    for rule in rules:
        matches, result = rule
        print u"%s -> %s" % (
            u" ".join(map(_to_char, matches)),
            _to_char(result))


# match :: (Int, Match) -> Bool
def match(x, y):
    if isinstance(y, list):
        return (x in y)
    if isinstance(y, int):
        return (x == y)
    if y == None:
        return True
    raise AssertionError('not here', y)


# apply_rules :: (Int, Int, Int) -> Int
def apply_rules(prev):
    for rule in rules:
        matches, result = rule
        if all(match(x, y) for x, y in zip(prev, matches)):
            return result
    raise AssertionError('not here')


states = [0] * 1 + [10, 0, 4, 8] + [0] * 20
N = len(states)

def repr_states(states):
    return ''.join(LETTERS[x] for x in states)


print (u'  '  + repr_states(states)).encode('utf-8')

for t in range(70):
    states = [0] + states + [0]
    next = []
    for i in range(N):
        next.append(apply_rules(states[i:i + 3]))
    states = next
    print (u'%2d' % (t + 1) + repr_states(states)).encode('utf-8')
