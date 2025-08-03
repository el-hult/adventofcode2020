
from util import read_input
from re import compile
from typing import Literal

my_input = read_input(19)
CHR = 'c'
SEQ = '>'
ALT = '|'


rules = {}
for line in my_input.splitlines():
  line = line.strip()
  if line == '':
    break # end of rules
  rule_num, rhs = line.split(': ')
  rule_num = int(rule_num)
  
  if rhs.startswith('"'):
    assert len(rhs) == 3
    char = rhs[1]
    rules[rule_num] = (CHR, char)
    continue

  if '|' in rhs:
    ors = rhs.split(' | ')
    assert len(ors) == 2
    alt1  = ('>', *map(int, ors[0].split(' ')))
    alt2 = ('>', *map(int, ors[1].split(' ')))
    alts = ('|', alt1, alt2
            )
    rules[rule_num] = alts    
    continue
  
  seq = tuple(map(int, rhs.split(' ')))
  rules[rule_num] = ('>', *seq)




# build a regex for rule 0 using the rule set above
# make it with a DFS traversal of sorts.
def build_regex(rule_num: int) -> str:
  rule = rules[rule_num]
  if rule[0] == CHR:
    assert len(rule) == 2
    return rule[1]
  elif rule[0] == SEQ:
    out = ''
    for k in rule[1:]:
      out += build_regex(k)
    return out
  elif rule[0] == ALT:
    assert len(rule) == 3
    out1 = "".join(build_regex(k) for k in rule[1][1:])
    out2 = "".join(build_regex(k) for k in rule[2][1:])
    out = f'({out1}|{out2})'
    return out
  else:
    raise ValueError(f'Unknown rule type {rule[0]} for rule {rule_num}')



regex = compile('^' + build_regex(0) + '$')

messages = my_input.splitlines()[len(rules):]
ans_one = sum(1 for m in messages if regex.match(m)
              )
assert ans_one == 120, 'First try!'