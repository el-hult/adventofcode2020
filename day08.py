import re
from copy import deepcopy
from enum import Enum, auto

from util import read_input


class instruction(Enum):
    acc = auto()
    jmp = auto()
    nop = auto()


class exit_code(Enum):
    looping = auto()
    completed = auto()


_line_re = re.compile("(jmp|acc|nop) (.*)")


def parse_line(line):
    m = _line_re.match(line)
    if m:
        a, b = m.group(1, 2)
        return instruction[a], int(b)
    else:
        raise ValueError


def run_program(program):
    visited_rows = set()
    instruction_ptr = 0
    run = True
    accumulator = 0
    finish_line = len(program)
    while run:
        if instruction_ptr in visited_rows:
            return exit_code["looping"], accumulator
        elif instruction_ptr == finish_line:
            return exit_code["completed"], accumulator
        else:
            visited_rows.add(instruction_ptr)
        inst, arg = program[instruction_ptr]
        if inst == instruction.nop:
            instruction_ptr += 1
        elif inst == instruction.acc:
            accumulator += arg
            instruction_ptr += 1
        elif inst == instruction.jmp:
            instruction_ptr += arg
        else:
            raise ValueError("bad program")


program = [parse_line(line) for line in read_input(8).splitlines()]
code, ansA = run_program(program)
assert ansA == 1521


def process():
    for position in range(len(program)):
        prog2 = deepcopy(program)
        if prog2[position][0] == instruction.jmp:
            prog2[position] = instruction.nop, prog2[position][1]
        elif prog2[position][0] == instruction.nop:
            prog2[position] = instruction.jmp, prog2[position][1]
        else:
            continue
        code, acc = run_program(prog2)
        if code == exit_code.completed:
            return acc
    raise RuntimeError


ansB = process()
assert ansB == 1016

