
from util import read_input

def eval_line(line:str, part:int) -> int:
  """Evaluate the maths expression in `line` according to the rules of part `part`."""
  MUL = '*'
  ADD = '+'
  LPAR = '('
  RPAR = ')'
  PREC = {ADD: 2, MUL: 1} if part == 2 else {ADD: 1, MUL: 1}
  BINOPS = {ADD, MUL}

  # Tokenize the input expression
  token_stream = []
  eptr = 0  # pointer into expression
  while eptr < len(line):
    if line[eptr] == ' ':
      eptr += 1
    elif line[eptr] == '+':
      token_stream.append(ADD)
      eptr += 1
    elif line[eptr] == '*':
      token_stream.append(MUL)
      eptr += 1
    elif line[eptr] == '(':
      token_stream.append(LPAR)
      eptr += 1
    elif line[eptr] == ')':
      token_stream.append(RPAR)
      eptr += 1
    elif line[eptr].isdigit():
      val = int(line[eptr])
      eptr += 1
      while eptr < len(line) and line[eptr].isdigit():
        val = val * 10 + int(line[eptr])
        eptr += 1
      token_stream.append(val)
    else:
      raise ValueError(f"Unexpected character in expression: {line[eptr]} at position {eptr}")

  # Convert token stream to Reverse Polish Notation (RPN) using the shunting yard algorithm
  operator_stack = []
  rpn_queue = []
  for tkn in token_stream:
    if isinstance(tkn, int):
      rpn_queue.append(tkn)
    elif tkn == LPAR:
      operator_stack.append(tkn)
    elif tkn == RPAR:
      while operator_stack[-1] != LPAR:
        rpn_queue.append(operator_stack.pop())
      assert operator_stack[-1] == LPAR
      operator_stack.pop()
    elif tkn in BINOPS:
      o1 = tkn # current operator
      while operator_stack and (o2 := operator_stack[-1]) != LPAR and PREC[o2] >= PREC[o1]:
        rpn_queue.append(operator_stack.pop()) # pop o2 
      operator_stack.append(o1)  # push the current operator onto the stack
  while operator_stack:
    assert operator_stack[-1] != LPAR, "Unexpected '(' on opstack at end of parsing"
    rpn_queue.append(operator_stack.pop()) # drain the operator stack at the end

  # Now output is in reverse polish notation, and we can evaluate it
  eval_stack = []
  for tkn in rpn_queue:
    if isinstance(tkn, int):
      eval_stack.append(tkn)
    elif tkn == ADD:
      right = eval_stack.pop()
      left = eval_stack.pop()
      eval_stack.append(left + right)
    elif tkn == MUL:
      right = eval_stack.pop()
      left = eval_stack.pop()
      eval_stack.append(left * right)
    else:
      raise ValueError(f"Unexpected token in RPN queue: {tkn}")
    
  assert len(eval_stack) == 1
  return eval_stack[0]

def part_one(raw_input: str) -> int:
  """Evaluate the input expression according to part one rules."""
  return sum(eval_line(line.strip(), 1) for line in raw_input.splitlines())

assert part_one("1 + 2 * 3 + 4 * 5 + 6") == 71
assert part_one("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert part_one("2 * 3 + (4 * 5)") == 26
assert part_one("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert part_one("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert part_one("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

my_input = read_input(18)
res = part_one(my_input)
assert res == 510009915468, "First try!"

def part_two(raw_input: str) -> int:
  return sum(eval_line(line.strip(), 2) for line in raw_input.splitlines())

assert part_two("1 + 2 * 3 + 4 * 5 + 6") == 231
assert part_two("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert part_two("2 * 3 + (4 * 5)") == 46
assert part_two("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert part_two("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert part_two("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

res2 = part_two(my_input)
assert res2 == 321176691637769, "First try!"