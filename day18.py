
from util import read_input


class PartOneSolver:
  def __init__(self, expression: str):
    self.e = expression
    self.p = 0  # pointer in expression

  def consume_num(self) -> int:
    """Consume a number from the expression."""
    start = self.p
    while self.p < len(self.e) and self.e[self.p].isdigit():
      self.p += 1
    return int(self.e[start:self.p])
  
  def consume_value(self) -> int:
    """Consume a value, which is either a number or an expression in parentheses.
    Parenthesized expressions are evaluated"""
    if self.e[self.p] == '(':
      self.p += 1  # skip '('
      value = self.consume_expression()
      self.p += 1  # skip ')'
      return value
    else:
      return self.consume_num()
    
  def consume_op(self) -> str:
    """Consume an operator from the expression."""
    if self.e[self.p:self.p + 3] == ' + ':
      self.p += 3
      return '+'
    elif self.e[self.p:self.p + 3] == ' * ':
      self.p += 3
      return '*'
    else:
      raise ValueError(f"Unexpected operator at position {self.p}: '{self.e[self.p:self.p + 3]}'")
    
  def done(self) -> bool:
    """Completed parsing expression?"""
    return self.p >= len(self.e) or self.e[self.p] == ')'
  
  def consume_expression(self) -> int:
    """An expressions is a value followed by zero or more operators and values.
    
    Two modes available:
    - 'ltr': addition and multiplication are done left-to-right, no precedence.
    - 'advanced': addition must be evaluated before multiplication, but parentheses must be evaluated first.
    """
    lhs = self.consume_value()
    while not self.done():
      op = self.consume_op()
      rhs = self.consume_value()
      lhs = lhs + rhs if op == '+' else lhs * rhs
    return lhs

def part_one(expression:str):
  """Evaluate special maths.
  addition and multiplication must be done left-to-right, not with precedence.
  parentheses must be evaluated first.

  plus and times have spaces around them
  """
  p = PartOneSolver(expression)
  val = p.consume_expression()
  assert p.done(), f"Did not consume whole expression: {expression} at position {p.p}"

  return val

assert part_one("1 + 2 * 3 + 4 * 5 + 6") == 71
assert part_one("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert part_one("2 * 3 + (4 * 5)") == 26
assert part_one("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert part_one("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert part_one("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

my_input = read_input(18).strip().splitlines()
res = 0 
for line in my_input:
  res += part_one(line.strip())
assert res == 510009915468, "First try!"

def part_two(parsed_expression_from_token_stream:str):
  """For part two, I realized I should learn how to work with operator precedence and parentheses more properly.
  The solution will be unnecessarily complicated, but it is more like a exercise for me in how to do this"""

  token_stream = []
  MUL = '*'
  ADD = '+'
  LPAR = '('
  RPAR = ')'
  END = '$'
  eptr = 0 # pointer in expression
  while eptr < len(parsed_expression_from_token_stream):
    if parsed_expression_from_token_stream[eptr] == ' ':
      eptr += 1
    elif parsed_expression_from_token_stream[eptr] == '+':
      token_stream.append(ADD)
      eptr += 1
    elif parsed_expression_from_token_stream[eptr] == '*':
      token_stream.append(MUL)
      eptr += 1
    elif parsed_expression_from_token_stream[eptr] == '(':
      token_stream.append(LPAR)
      eptr += 1
    elif parsed_expression_from_token_stream[eptr] == ')':
      token_stream.append(RPAR)
      eptr += 1
    elif parsed_expression_from_token_stream[eptr].isdigit():
      val = int(parsed_expression_from_token_stream[eptr])
      eptr += 1
      while eptr < len(parsed_expression_from_token_stream) and parsed_expression_from_token_stream[eptr].isdigit():
        val = val * 10 + int(parsed_expression_from_token_stream[eptr])
        eptr += 1
      token_stream.append(val)
    else:
      raise ValueError(f"Unexpected character in expression: {parsed_expression_from_token_stream[eptr]} at position {eptr}")
  token_stream.append(END)  # end of expression marker



  # Run shunting yard to create a reverse polish notation expression
  operator_stack = []  # stack for operators
  out_queue = []
  PREC = {ADD: 2, MUL: 1}
  for tkn in token_stream:
    if isinstance(tkn, int):
      out_queue.append(tkn)
    elif tkn == LPAR:
      operator_stack.append(tkn)
    elif tkn == RPAR:
      while operator_stack[-1] != LPAR:
        out_queue.append(operator_stack.pop())
      assert operator_stack[-1] == LPAR, "Expected '(' on stack"
      operator_stack.pop()
    elif tkn in (ADD, MUL): # the only operators we have :)
      o1 = tkn # current operator
      while operator_stack and (o2 := operator_stack[-1]) != LPAR and PREC[o2] >= PREC[o1]:
        out_queue.append(operator_stack.pop()) # pop o2 
      operator_stack.append(o1)  # push the current operator onto the stack
  while operator_stack:
    assert operator_stack[-1] != LPAR, "Unexpected '(' on opstack at end of parsing"
    out_queue.append(operator_stack.pop()) # drain the operator stack at the end

  # Now oq is in reverse polish notation, and we can evaluate it
  stack = []
  for tkn in out_queue:
    if isinstance(tkn, int):
      stack.append(tkn)
    elif tkn == ADD:
      right = stack.pop()
      left = stack.pop()
      stack.append(left + right)
    elif tkn == MUL:
      right = stack.pop()
      left = stack.pop()
      stack.append(left * right)
    else:
      raise ValueError(f"Unexpected token in output queue: {tkn}")
    
  assert len(stack) == 1
  return stack[0]

    
assert part_two("1 + 2 * 3 + 4 * 5 + 6") == 231
assert part_two("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert part_two("2 * 3 + (4 * 5)") == 46
assert part_two("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert part_two("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert part_two("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

res2 = sum(part_two(line.strip()) for line in my_input)
assert res2 == 321176691637769, "First try!"