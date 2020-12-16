from util import read_input
from itertools import starmap

test_data_1 = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
"""
test_output_1 = [
    (70, 7, 567),
    (14, 7, 119),
    (102, 4, 820),
]


def get_row_col(line):
    assert len(line) == 10
    assert all(t in "FB" for t in line[:7])
    assert all(t in "LR" for t in line[7:10])
    row_bin = line[:7].replace("F", "0").replace("B", "1")
    row_num = int(row_bin, base=2)
    col_bin = line[7:10].replace("L", "0").replace("R", "1")
    col_num = int(col_bin, base=2)
    return row_num, col_num


def seat_id(row, col):
    return row * 8 + col


assert all(
    a == (*b, seat_id(*b))
    for a, b in zip(test_output_1, map(get_row_col, test_data_1.splitlines()))
)

seen_boarding_pass_seat_ids = list(
    starmap(seat_id, map(get_row_col, read_input(5).splitlines()))
)
ansA = max(seen_boarding_pass_seat_ids)
assert ansA == 901

all_valid_seats = set(
    range(min(seen_boarding_pass_seat_ids), max(seen_boarding_pass_seat_ids) + 1)
)
not_seet_seat_ids = all_valid_seats - set(seen_boarding_pass_seat_ids)
(ansB,) = not_seet_seat_ids
assert ansB == 661
