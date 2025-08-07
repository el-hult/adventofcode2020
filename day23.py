from util import read_input
from dataclasses import dataclass


@dataclass(slots=True)
class Cup:
  value: int
  next: "Cup" = None


def play_one_move(all_cups, current_cup):
  """
  PRECONDITION: all_cups[j] holds cup with value j+1
  """
  first = current_cup.next
  second = first.next
  third = second.next
  destination_cup_value = (
    current_cup.value - 1 if current_cup.value > 1 else len(all_cups)
  )
  while destination_cup_value in (first.value, second.value, third.value):
    destination_cup_value -= 1
    if destination_cup_value < 1:
      destination_cup_value = len(all_cups)
  dest = all_cups[destination_cup_value - 1]
  current_cup.next = third.next
  third.next = dest.next
  dest.next = first
  return current_cup.next


def initialize(raw: str, part_two: bool):
  val = raw.strip()
  cups = [Cup(int(c), None) for c in val]
  current_cup = cups[0]
  if part_two:
    for j in range(len(cups), 1000000):
      cups.append(Cup(j + 1, None))
  for i in range(len(cups)):
    cups[i].next = cups[(i + 1) % len(cups)]
  cups = sorted(
    cups, key=lambda c: c.value
  )  # sort by value, so that cup 1 is at position 0 in the list. for quick lookups!
  return cups, current_cup


def part_one(raw, rounds):
  all_cups, current = initialize(raw, part_two=False)
  for _ in range(rounds):
    current = play_one_move(all_cups, current)

  cup_1 = all_cups[0]
  out = ""
  for _ in range(len(all_cups) - 1):
    cup_1 = cup_1.next
    out += str(cup_1.value)
  return out


assert part_one(read_input(23), 100) == "25468379", "First try!"
# assert part_one('389125467',10) == '92658374', "Test case"


def part_two(raw):
  all_cups, current = initialize(raw, part_two=True)
  for _ in range(10_000_000):
    current = play_one_move(all_cups, current)
  cup_1 = all_cups[0]
  return cup_1.next.value * cup_1.next.next.value


# assert part_two('389125467') == 149245887792, "Test case"
ans_two = part_two(read_input(23))
assert ans_two < 999980000099, (
  "I had a mistake in first try :( Just ran 1 million rounds instead of 10 million"
)
assert ans_two == 474747880250, "This is my right answer!"
