from util import read_input
from re import compile

CHR = "c"
SEQ = ">"
ALT = "|"

def parse_rules(raw):
  extra_id = 100000
  rules = {}
  for line in raw.splitlines():
    line = line.strip()
    if line == "":
      break  # end of rules
    rule_num, rhs = line.split(": ")
    rule_num = int(rule_num)

    if rhs.startswith('"'):
      assert len(rhs) == 3
      char = rhs[1]
      rules[rule_num] = (CHR, char)
      continue

    if "|" in rhs:
      ors = rhs.split(" | ")
      assert len(ors) == 2
      alt1 = (">", *map(int, ors[0].split(" ")))
      alt2 = (">", *map(int, ors[1].split(" ")))
      rules[rule_num] = ("|", extra_id, extra_id + 1)
      rules[extra_id] = alt1
      rules[extra_id + 1] = alt2
      extra_id += 2
      continue

    seq = tuple(map(int, rhs.split(" ")))
    rules[rule_num] = (">", *seq)
  return rules


# build a regex for rule 0 using the rule set above
# make it with a DFS traversal of sorts.
def build_regex(rules,rule_num: int) -> str:
  rule = rules[rule_num]
  if rule[0] == CHR:
    assert len(rule) == 2
    return rule[1]
  elif rule[0] == SEQ:
    out = ""
    for k in rule[1:]:
      out += build_regex(rules, k)
    return out
  elif rule[0] == ALT:
    assert len(rule) == 3
    out1 = build_regex(rules, rule[1])
    out2 = build_regex(rules, rule[2])
    out = f"({out1}|{out2})"
    return out
  else:
    raise ValueError(f"Unknown rule type {rule[0]} for rule {rule_num}")

def part_one(my_input):
  rules = parse_rules(my_input)
  messages = my_input.split("\n\n")[1].splitlines()

  regex = compile("^" + build_regex(rules, 0) + "$")
  ans_one = sum(1 for m in messages if regex.match(m))
  return ans_one

def part_two(my_input):
  return 0

def main():
  my_input = read_input(19)
  ans_one = part_one(my_input)
  assert ans_one == 120, "First try!"

  ans2 = part_two(my_input)
  print(ans2)
  assert ans2 > 260, f"Failed. The answer must be > 260. got {ans2}"



if __name__ == "__main__":
  main()