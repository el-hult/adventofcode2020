from collections import Counter
from itertools import starmap, groupby
from operator import sub

from util import read_input, flip, rolling

inputs = [int(i) for i in read_input(10).splitlines()]

voltages = list(sorted(inputs))
voltages.insert(0, 0)
voltages.append(voltages[-1] + 3)


c = Counter((starmap(flip(sub), rolling(voltages, 2))))
n1 = c.pop(1)
n3 = c.pop(3)
ansA = n1 * n3
assert ansA > 2628
assert ansA == 2738
print(ansA)


assert len(c) == 0  # there were only 1-diff and 3-diff voltages!
diffs = starmap(flip(sub), rolling(voltages, 2))
n_combs = 1
comb_dict = {1: 2 ** 0, 2: 2 ** 1, 3: 2 ** 2, 4: 2 ** 3 - 1}
for key, grp in groupby(diffs):
    if key == 3:
        # 3-steps are fixed. no freedom to choose here...
        continue
    else:
        # the longest chunk is 4, so i have precomputed the number of choices possible
        grp_len = sum(1 for _ in grp)
        n_combs *= comb_dict[grp_len]
ansB = n_combs
assert ansB == 74049191673856
print(ansB)
