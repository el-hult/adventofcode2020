from itertools import combinations
from math import prod

from util import read_input

input = [int(i) for i in read_input(1).splitlines()]

for r in [2, 3]:
    gen = (q for q in combinations(input, r=r) if sum(q) == 2020)
    print(prod(next(gen)))
