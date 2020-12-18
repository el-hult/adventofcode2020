import unittest
from day14 import CollisionResult, processB, processA, find_collide


fuu = """mask = 0000
mem[0] = 1
mem[0] = 0
mem[4] = 1
mask = 0X00
mem[1] = 2
mask = 0000
mem[5] = 3
mask = 00XX
mem[0] = 4
mask = 001X
mem[2] = 5
mask = 1XXX
mem[0] = 1
mask = 110X
mem[0] = 0
"""


def get_fuu(n):
    return "\n".join(fuu.splitlines()[: 1 + n])


test_input_b = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

test_input_a = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


class TestPRocessA(unittest.TestCase):
    def test_given(self):
        assert processA(test_input_a) == 165


class TestProcessB(unittest.TestCase):
    def test_given(self):
        assert processB(test_input_b, 36) == 208

    def test_fuu(self):
        nbits = 4
        self.assertEqual(processB(get_fuu(1), nbits), 1)  # regular write
        self.assertEqual(processB(get_fuu(2), nbits), 0)  # overwrite single position
        self.assertEqual(processB(get_fuu(5), nbits), 5)  # write chunk
        self.assertEqual(processB(get_fuu(7), nbits), 6)  # split a written memory
        self.assertEqual(processB(get_fuu(9), nbits), 20)  # overwrite 2
        self.assertEqual(processB(get_fuu(11), nbits), 22)  # 2bit collision/1bit split
        self.assertEqual(processB(get_fuu(15), nbits), 28)  # 2bit collision/2bit split


class TestCollisions(unittest.TestCase):
    def test_abc(self):
        self.assertEqual(find_collide("0", "1", 1), (CollisionResult.disjoint, -1, -1))
        self.assertEqual(find_collide("1", "1", 1), (CollisionResult.supset, -1, -1))
        self.assertEqual(find_collide("X1", "11", 2), (CollisionResult.supset, 0, -1))
        self.assertEqual(find_collide("11", "X1", 2), (CollisionResult.subset, -1, 0))
        self.assertEqual(
            find_collide("1X", "X1", 2), (CollisionResult.intersects, 1, 0)
        )


if __name__ == "__main__":
    # unittest.main()
    TestCollisions().test_abc()
    TestProcessB().test_fuu()
