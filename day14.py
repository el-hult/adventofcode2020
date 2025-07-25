from typing import Dict
from util import read_input

from enum import Enum, auto


class CollisionResult(Enum):
    full_cover = auto()
    partial_cover = auto()
    disjoint = auto()


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
    """Analyze adress colission

    addr1 and addr2 are masked adresses referring to a set of actual adresses.
    When writing to the adresses specified by the masked addr1, will that write
    instruction cover the adresses specified by addr2?

    If the adress spaces are not disjoint, is the overlap partial or complete?

    When the overlap is partial - specify one bit in addr2 that needs to be changed
    from X to 1 or 0 in order fo make a full cover or a disjoint cover
    """
    split = -1
    full_cover = True
    for j in range(nbits):
        c1 = addr1[j]
        cs = c1 + addr2[j]
        if cs in ["01", "10"]:
            return CollisionResult.disjoint, split
        elif cs == "XX":
            pass
        elif cs in ["11", "00"]:
            pass
        else:
            if c1 != "X":
                full_cover = False
                split = j

    if full_cover:
        return CollisionResult.full_cover, split
    else:
        return CollisionResult.partial_cover, split


def processB_write(addr1: str, val: int, mem: Dict[str, int]):
    """Takes an address and a value to write into memory

    Run once per write instruction in the source file
    """
    nbits = len(addr1)
    if len(mem) == 0:
        mem[addr1] = val
    else:
        check_collisions = True
        while check_collisions:
            check_collisions = False
            for addr2 in list(mem.keys()):
                colltype, split = find_collide(addr1, addr2, nbits)
                if colltype == CollisionResult.full_cover:
                    # The new write makes the old one obsolete
                    del mem[addr2]
                elif colltype == CollisionResult.disjoint:
                    pass
                elif colltype == CollisionResult.partial_cover:
                    # The write collides in part with memory
                    # Split the memory.
                    # no collision checks!
                    mem[addr2[:split] + "0" + addr2[split + 1 :]] = mem[addr2]
                    mem[addr2[:split] + "1" + addr2[split + 1 :]] = mem[addr2]
                    del mem[addr2]
                    # Recursive splitting to resolve collisions
                    check_collisions = True
                else:
                    raise RuntimeError
        mem[addr1] = val


def processB(input, nbits):
    mem = {}
    mask = ""
    for line in input.splitlines():
        instr, arg = line.split(" = ")
        if instr == "mask":
            mask = arg
            assert len(mask) == nbits, (
                "The bit mask don't correspond to the address space given"
            )
        elif instr[:3] == "mem":
            addr_raw = f"{int(instr[4:-1]):b}".zfill(nbits)
            val = int(arg)
            addr = "".join(
                addr_raw[j] if mask[j] == "0" else mask[j] for j in range(nbits)
            )
            processB_write(addr, val, mem)
        else:
            raise ValueError

    out = 0
    for k, v in mem.items():
        mult = sum(1 for j in k if j == "X")
        out += v * 2**mult
    return out


def main():
    true_input = read_input(14)
    ansA = processA(true_input)
    assert ansA == 13727901897109

    ansB = processB(true_input, 36)
    assert ansB < 5605677382384
    assert ansB == 5579916171823


if __name__ == "__main__":
    main()
