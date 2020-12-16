from itertools import combinations
from math import prod

from util import read_input

input = [int(i) for i in read_input(1).splitlines()]

ansA = prod(next((q for q in combinations(input, r=2) if sum(q) == 2020)))
ansB = prod(next((q for q in combinations(input, r=3) if sum(q) == 2020)))

assert ansA == 989824
assert ansB == 66432240
