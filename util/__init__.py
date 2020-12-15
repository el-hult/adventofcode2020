import itertools


def read_input(day: int):
    with open(f"./inputs/day{day}.txt", "rt") as ff:
        o = ff.read()
    return o


def window(iterable, n=2):
    # https://napsterinblue.github.io/notes/python/internals/itertools_sliding_window/
    iterables = itertools.tee(iterable, n)

    for iterable, num_skipped in zip(iterables, itertools.count()):
        for _ in range(num_skipped):
            next(iterable, None)

    return zip(*iterables)
