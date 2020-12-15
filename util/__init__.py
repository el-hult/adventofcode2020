import itertools
import functools


def read_input(day: int):
    with open(f"./inputs/day{day}.txt", "rt") as ff:
        o = ff.read()
    return o


def rolling(iterable, n=2):
    # https://napsterinblue.github.io/notes/python/internals/itertools_sliding_window/
    iterables = itertools.tee(iterable, n)

    for iterable, num_skipped in zip(iterables, itertools.count()):
        for _ in range(num_skipped):
            next(iterable, None)

    return zip(*iterables)


def flip(func):
    """Create a new function from the original with the arguments reversed
    
    https://stackoverflow.com/a/9850282/4050510
    """

    @functools.wraps(func)
    def newfunc(*args):
        return func(*args[::-1])

    return newfunc
