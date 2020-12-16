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
    return [(r + dr, c + dc) for dr, dc in dirs]


def rays(r, c, h, w):
    for dir in dirs:
        yield ray(r, c, h, w, dir)


def ray(r, c, h, w, dir):
    r = r + dir[0]
    c = c + dir[1]
    while 0 <= r <= h and 0 <= c <= w:
        yield (r, c)
        r = r + dir[0]
        c = c + dir[1]


def print_state(d, h, w):
    """Helper used in debugging"""
    for r in range(h):
        for c in range(w):
            print(d[(r, c)], end="")
        print("")


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
                to_check = neighbors(r, c)
                neighbor_vals = [state_now[t] for t in to_check]
                s1 = sum(1 for v in neighbor_vals if v == "#")
                threshold = 4
            elif mode == "B":
                s1 = 0
                for ray in rays(r, c, h, w):
                    next_seat = next(
                        ((x, y) for x, y in ray if state_now[(x, y)] != "."), None
                    )
                    s1 += 1 if state_now[next_seat] == "#" else 0
                threshold = 5
            else:
                raise ValueError
            if state_now[(r, c)] == "L" and s1 == 0:
                state_next[(r, c)] = "#"
                did_update = True
            elif state_now[(r, c)] == "#" and s1 >= threshold:
                state_next[(r, c)] = "L"
                did_update = True
            else:
                state_next[(r, c)] = state_now[(r, c)]
        state_now = state_next
        state_next = defaultdict(lambda: ".")
        # print("\n\n\n\n\n\n")
        # print_state(state_now, h, w)
    return sum(1 for k, v in state_now.items() if v == "#")


assert process("A", test_input) == 37
assert process("B", test_input) == 26

ansA = process("A", true_input)
assert ansA > 2189
assert ansA == 2247
print(ansA)

ansB = process("B", true_input)
assert ansB == 2011
print(ansB)
