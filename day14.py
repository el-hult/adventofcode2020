from typing import Literal
from util import read_input

from enum import Enum, auto


class CollisionResult(Enum):
    supset = auto()
    subset = auto()
    disjoint = auto()
    intersects = auto()


def processA(input):
    mem = {}
    mark_and = 0
    mark_or = 0
    for line in input.splitlines():
        instr, arg = line.split(" = ")
        if instr == "mask":
            mark_or = int(arg.replace("X", "0"), 2)
            mark_and = int(arg.replace("X", "1"), 2)
        elif instr[:3] == "mem":
            addr = int(instr[4:-1])
            val = int(arg)
            fixedval = (val & mark_and) | mark_or
            mem[addr] = fixedval
        else:
            raise ValueError
    return sum(mem.values())


def find_collide(addr1, addr2, nbits):
    split1 = split2 = -1
    is_subset = True
    is_supset = True
    for j in range(nbits):
        c1: Literal["X", "1", "0"] = addr1[j]
        c2: Literal["X", "1", "0"] = addr2[j]
        cs = c1 + c2
        if cs in ["01", "10"]:
            return CollisionResult.disjoint, -1, -1
        elif cs == "XX":
            pass
        elif cs in ["11", "00"]:
            pass
        else:
            if c2 != "X":
                is_subset = False
                split1 = j
            if c1 != "X":
                is_supset = False
                split2 = j

    if is_supset:
        return CollisionResult.supset, split1, split2
    elif is_subset:
        return CollisionResult.subset, split1, split2
    else:
        return CollisionResult.intersects, split1, split2


def processB(input, nbits):
    mem = {}
    mask = ""
    for line in input.splitlines():
        instr, arg = line.split(" = ")
        if instr == "mask":
            mask = arg
            assert (
                len(mask) == nbits
            ), "The bit mask don't correspond to the address space given"
        elif instr[:3] == "mem":
            to_write = []
            addr_raw = f"{int(instr[4:-1]):b}".zfill(nbits)
            val = int(arg)
            addr = "".join(
                addr_raw[j] if mask[j] == "0" else mask[j] for j in range(nbits)
            )
            # print("mem", addr_raw, addr, val)
            to_write.insert(0, (addr, val))
            while len(to_write) > 0:
                addr1, val1 = to_write.pop(0)
                if len(mem) == 0:
                    mem[addr1] = val1
                    # print("Fresh write")
                else:
                    check_collisions = True
                    while check_collisions:
                        check_collisions = False
                        for addr2 in list(mem.keys()):
                            colltype, split1, split2 = find_collide(addr1, addr2, nbits)
                            # print(colltype, split1, split2, addr1, addr2)
                            if colltype == CollisionResult.supset:
                                # The new write makes the old one obsolete
                                del mem[addr2]
                                # Chck with other data in memory for collisions
                                continue
                            if colltype == CollisionResult.disjoint:
                                # This one is fint too. Check with other collisions!
                                continue
                            if (
                                colltype == CollisionResult.subset
                                or colltype == CollisionResult.intersects
                            ):
                                # The write collides in part with memory
                                # Split the memory.
                                # no collision checks!
                                mem[addr2[:split2] + "0" + addr2[split2 + 1 :]] = mem[
                                    addr2
                                ]
                                mem[addr2[:split2] + "1" + addr2[split2 + 1 :]] = mem[
                                    addr2
                                ]
                                del mem[addr2]
                                # Recursive splitting to resolve collisions
                                check_collisions = True
                            if colltype == CollisionResult.intersects:
                                # only split memory, never the write
                                continue
                    mem[addr1] = val1
        else:
            raise ValueError

    # print(mem)
    out = 0
    for k, v in mem.items():
        mult = sum(1 for j in k if j == "X")
        out += v * 2 ** mult
    return out


def main():
    true_input = read_input(14)
    ansA = processA(true_input)
    assert ansA == 13727901897109

    ansB = processB(true_input, 36)
    print(ansB)
    assert ansB < 5605677382384
    assert ansB == 5579916171823


if __name__ == "__main__":
    main()
