from string import ascii_lowercase
from util import read_input
from collections import Counter

test_data_1 = """abc

a
b
c

ab
ac

a
a
a
a

b"""

test_groups = test_data_1.split("\n\n")
yes_per_group = list(
    len(set(char for char in group if char in ascii_lowercase)) for group in test_groups
)
assert all(a == b for a, b in zip(yes_per_group, [3, 3, 3, 1, 1]))
assert sum(yes_per_group) == 11

real_groups = read_input(6).split("\n\n")
ansA = sum(
    len(set(char for char in group if char in ascii_lowercase)) for group in real_groups
)
assert 6680 == ansA

ansB = 0
for group in real_groups:
    size = len(group.splitlines())
    counter = Counter(char for char in group if char in ascii_lowercase)
    ansB += sum(val == size for val in counter.values())

assert ansB == 3117
