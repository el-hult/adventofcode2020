from re import compile
from collections import Counter

from util import read_input


def parseline(line, re):
    a, b, c, d = re.match(line).groups()
    return int(a), int(b), c, d


def valid_a(low, high, letter, pwd):
    return low <= Counter(pwd)[letter] <= high


def valid_b(first, second, letter, pwd):
    ok = (pwd[first - 1] == letter) != (pwd[second - 1] == letter)
    return ok


if __name__ == "__main__":
    re = compile(r"(\d+)-(\d+) ([a-z]): (.+)")
    input = [parseline(i, re) for i in read_input(2).splitlines()]
    print(sum(int(valid_a(*line)) for line in input))
    print(sum(int(valid_b(*line)) for line in input))
