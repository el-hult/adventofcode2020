from itertools import combinations

from util import read_input, window

data = read_input(9)
data = [int(line) for line in data.splitlines()]
preamble_len = 25

for k in range(preamble_len, len(data)):
    ss = (a + b for a, b in combinations(data[k - preamble_len : k], r=2))
    if data[k] in ss:
        continue
    else:
        ansA = data[k]
        break

assert ansA != 35
assert ansA == 400480901
print(ansA)


searching = True
m = 1
while searching:
    m += 1
    for k in window(data, m):
        s = sum(k)
        if s == ansA:
            ansB = min(k) + max(k)
            searching = False
            break

assert ansB < 800961802
assert ansB == 67587168
print(ansB)
