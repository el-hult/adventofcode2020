from itertools import product
from collections import defaultdict

from util import read_input

test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
"""variable for the test cases"""

true_input = read_input(11)

dirs = [(-1, -1), (0, -1), (+1, -1), (-1, 0), (+1, 0), (-1, +1), (0, +1), (+1, +1)]


def neighbors(r, c):
    """ Get the neighbors
    
    This used to be a list comprehension.
    Swapping to a generator expression made everything slower.
    But going to this list of tuple expression saves 0.5-1 second runtime!
    """
    return [
        (r - 1, c - 1),
        (r + 0, c - 1),
        (r + 1, c - 1),
        (r - 1, c + 0),
        (r + 1, c + 0),
        (r - 1, c + 1),
        (r + 0, c + 1),
        (r + 1, c + 1),
    ]


ZERO = 0
LOW = 1
HIGH = 2


def statusA(r, c, state_now):
    s = 0
    for t in neighbors(r, c):
        s += state_now[t] == "#"
        if s == 4:
            return HIGH
    if s == 0:
        return ZERO
    else:
        return LOW


def statusB(r, c, h, w, state_now):
    s1 = 0
    for dx, dy in dirs:
        x = r + dx
        y = c + dy
        while 0 <= x <= h and 0 <= y <= w:
            v = state_now[(x, y)]
            if v == "#":
                s1 += 1
                if s1 == 5:
                    return HIGH
                break
            elif v == "L":
                break
            x += dx
            y += dy
    if s1 == 0:
        return ZERO
    else:
        return LOW


def process(mode, input):

    data = {
        (r, c): char
        for r, line in enumerate(input.splitlines())
        for c, char in enumerate(line)
    }
    h, w = (a + 1 for a in max(data.keys()))

    did_update = True
    state_now = defaultdict(lambda: ".", data)
    state_next = defaultdict(lambda: ".")
    while did_update:
        did_update = False
        for r, c in product(range(h), range(w)):
            if mode == "A":
                status = statusA(r, c, state_now)
            elif mode == "B":
                status = statusB(r, c, h, w, state_now)
            else:
                raise ValueError
            if state_now[(r, c)] == "L" and status == ZERO:
                state_next[(r, c)] = "#"
                did_update = True
            elif state_now[(r, c)] == "#" and status == HIGH:
                state_next[(r, c)] = "L"
                did_update = True
            else:
                state_next[(r, c)] = state_now[(r, c)]
        state_now = state_next
        state_next = defaultdict(lambda: ".")
    return sum(1 for k, v in state_now.items() if v == "#")


assert process("A", test_input) == 37

ansA = process("A", true_input)
assert ansA > 2189
assert ansA == 2247

assert process("B", test_input) == 26
ansB = process("B", true_input)
assert ansB == 2011
