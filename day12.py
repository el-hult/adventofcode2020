from functools import reduce

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


cardinal = "ENWS"  # mapping from direction int to cardinal direction name


def navigate(state, instruction):
    if instruction[0] == "F":
        translation_instruction = (cardinal[state[2]], instruction[1])
        return translate(state, translation_instruction)
    elif instruction[0] in "NSEW":
        return translate(state, instruction)
    elif instruction[0] in "RL":
        return rotate(state, instruction)
    else:
        raise ValueError(f"Cannot handle instruction {instruction}")


def translate(state, instruction):
    ew, ns, dir = state
    action, val = instruction
    if action == "N":
        return (ew, ns + val, dir)
    elif action == "W":
        return (ew - val, ns, dir)
    elif action == "S":
        return (ew, ns - val, dir)
    elif action == "E":
        return (ew + val, ns, dir)
    else:
        raise ValueError


def rotate(state, instruction):
    ew, ns, dir = state
    action, val = instruction
    if action == "R":
        return ew, ns, (dir + (-val // 90)) % 4
    elif action == "L":
        return ew, ns, (dir + (val // 90)) % 4
    else:
        raise ValueError


def process(input):
    instructions = ((s[0], int(s[1:])) for s in input.splitlines())
    state = (
        0,
        0,
        0,
    )  # state is east/west, north/south, and direction (east=0,north=1,west=2,south=3)
    ew, ns, _ = reduce(navigate, instructions, state)
    return mahnattan(ew, ns)


def main():
    assert process(test_input) == 25

    ansA = process(true_input)
    print(ansA)
    assert ansA == 1482


if __name__ == "__main__":
    main()
