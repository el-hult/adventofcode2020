from functools import reduce, partial

from util import read_input


true_input = read_input(12)
test_input = """F10
N3
F7
R90
F11"""


def mahnattan(r, c):
    """Compute manhattan distance for a 2d coordinate"""
    return abs(r) + abs(c)


cardinals = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}


def navigate(state, instruction, mode):
    ship_pos = state[:2]
    wp_pos = state[2:]
    action = instruction[0]
    argument = instruction[1]
    if action == "F":
        return (*translate(ship_pos, wp_pos, argument), *wp_pos)
    elif action in cardinals.keys() and mode == "A":
        return (
            *translate(ship_pos, cardinals[action], argument),
            *wp_pos,
        )
    elif action in cardinals.keys() and mode == "B":
        return (
            *ship_pos,
            *translate(wp_pos, cardinals[action], argument),
        )
    elif action in "RL":
        return (*ship_pos, *rotate(wp_pos, action, argument))
    else:
        raise ValueError


def translate(coord1: tuple, coord2: tuple, val: int) -> tuple:
    return (
        coord1[0] + val * coord2[0],
        coord1[1] + val * coord2[1],
    )


def rotate(pos, action, argument):
    """Rotate a 2d point in the plane around the origin"""
    if action == "R":
        n_ccw = (-argument // 90) % 4
    elif action == "L":
        n_ccw = (argument // 90) % 4
    else:
        raise ValueError

    x, y = pos
    if n_ccw == 0:
        return pos
    elif n_ccw == 1:
        return -y, x
    elif n_ccw == 2:
        return -x, -y
    elif n_ccw == 3:
        return y, -x
    else:
        raise RuntimeError


def process(input, mode):
    instructions = ((s[0], int(s[1:])) for s in input.splitlines())
    initial_state = {
        "A": (
            0,
            0,
            1,
            0,
        ),
        "B": (
            0,
            0,
            10,
            1,
        ),
    }
    ew, ns, _, _ = reduce(
        partial(navigate, mode=mode), instructions, initial_state[mode]
    )
    return mahnattan(ew, ns)


def main():
    assert process(test_input, "A") == 25
    ansA = process(true_input, "A")
    assert ansA == 1482

    assert process(test_input, "B") == 286
    ansB = process(true_input, "B")
    assert ansB == 48739


if __name__ == "__main__":
    main()
