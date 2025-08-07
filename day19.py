from util import read_input
import re

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
      rules[rule_num] = char
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


def build_regex(rules, rule_num: int) -> str:
  """Compute the regex for a rule number."""
  rule = rules[rule_num]
  if isinstance(rule, str):
    return rule
  elif rule[0] == SEQ:
    out = ""
    for k in rule[1:]:
      out += build_regex(rules, k) if isinstance(k, int) else k
    return out
  elif rule[0] == ALT:
    assert len(rule) == 3
    out1 = build_regex(rules, rule[1]) if isinstance(rule[1], int) else rule[1]
    out2 = build_regex(rules, rule[2]) if isinstance(rule[2], int) else rule[2]
    out = f"({out1}|{out2})"
    return out
  else:
    raise ValueError(f"Unknown rule type {rule[0]} for rule {rule_num}")


def part_one(my_input):
  rules = parse_rules(my_input)
  messages = my_input.split("\n\n")[1].splitlines()

  regex = re.compile("^" + build_regex(rules, 0) + "$")
  ans_one = sum(1 for m in messages if regex.match(m))
  return ans_one


def part_two(my_input):
  rules = parse_rules(my_input)
  messages = my_input.split("\n\n")[1].splitlines()
  assert rules[0] == (SEQ, 8, 11)
  assert rules[8] == (SEQ, 42)
  assert rules[11] == (SEQ, 42, 31)
  # after update, rule 8 is 1 or more rule 42s
  # after update  rule 11 is at least one rule 42 followed by the same number of rule 31s
  # if we are a little lucky, can greedily parse a number of 42s and then some number of 31s,
  # making sure we have at least one more 42 than 31. That means all is good!
  pattern42 = build_regex(rules, 42)
  pattern31 = build_regex(rules, 31)
  n_good_messages = 0
  for message in messages:
    n_matches_42 = 0
    ptr = 0

    matches = re.finditer(pattern42, message)
    for m in matches:
      if m.start() != ptr:
        break
      ptr = m.end()
      n_matches_42 += 1

    rest = message[ptr:]

    n_matches_31 = 0
    matches = re.finditer(pattern31, rest)
    ptr = 0
    for m in matches:
      if m.start() != ptr:
        break
      ptr = m.end()
      n_matches_31 += 1

    if (
      n_matches_42 > 0
      and n_matches_31 > 0
      and n_matches_42 > n_matches_31
      and ptr == len(rest)
    ):
      n_good_messages += 1

  return n_good_messages


def main():
  my_input = read_input(19)
  ans_one = part_one(my_input)
  assert ans_one == 120, "First try!"

  ans2 = part_two(my_input)
  assert ans2 > 260, f"Failed. The answer must be > 260. got {ans2}"
  assert ans2 < 402, "Failed again. My answer must be < 402."
  assert ans2 == 350, "Third times the charm. My answer must was 350."


if __name__ == "__main__":
  main()
