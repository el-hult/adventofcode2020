from operator import itemgetter
from itertools import combinations, starmap, count
from math import prod, gcd
from typing import Sequence, Tuple
from util import read_input

test_input = """939
7,13,x,x,59,x,31,19"""
true_input = read_input(13)


def processA(input):
    min_now, schedule = input.splitlines()
    min_now = int(min_now)
    buses = [int(b) for b in schedule.split(",") if b != "x"]
    min_to_next_bus = min(map(lambda b: (b, b - min_now % b), buses), key=itemgetter(1))
    return prod(min_to_next_bus)


def crt_sieve(ans: Sequence[Tuple[int, int]]) -> int:
    """Compute the first solution as Chinese Remainder Theorem by Sieve

    finds the smallest integer x such that

        all(x % n == a for a,n in an) == True

    """
    assert max(starmap(gcd, combinations(map(itemgetter(1), ans), r=2))) == 1, (
        "Some divisors are not coprime"
    )
    ans = sorted(ans, key=itemgetter(1), reverse=True)

    x, nprods = ans[0]
    for k in range(2, len(ans) + 1):
        x = next(x_ for x_ in count(x, nprods) if all(x_ % n == a for a, n in ans[:k]))
        nprods *= ans[k - 1][1]
    return x


def processB(input):
    _, schedule = input.splitlines()
    an_list = [
        (-i % int(b), int(b)) for i, b in enumerate(schedule.split(",")) if b != "x"
    ]
    return crt_sieve(an_list)


assert processA(test_input) == 295
ansA = processA(true_input)
assert ansA == 2305

assert processB(test_input) == 1068781
ansB = processB(true_input)
assert ansB == 552612234243498
