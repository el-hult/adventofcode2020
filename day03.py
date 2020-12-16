from itertools import islice
from math import prod

from util import read_input


lines = read_input(3).splitlines()
linewidth = len(lines[0])

ans_a = sum(line[(3 * i) % linewidth] == "#" for i, line in enumerate(lines))

ans_b = prod(
    sum(
        line[(right * i) % linewidth] == "#"
        for i, line in enumerate(islice(lines, None, None, down))
    )
    for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
)

assert ans_a == 153
assert ans_b == 2421944712
