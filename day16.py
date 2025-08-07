from util import read_input


def parse(input):
  lines = input.splitlines()
  state = "rules"
  rules = {}
  while state == "rules":
    line = lines.pop(0)
    if line == "":
      state = "your_ticket"
      break
    field, ranges = line.split(": ")
    ranges = ranges.split(" or ")
    assert len(ranges) == 2
    low1, high1 = map(int, ranges[0].split("-"))
    low2, high2 = map(int, ranges[1].split("-"))
    rules[field] = (low1, high1, low2, high2)

  lines.pop(0)  # skip "your ticket:"
  your_ticket = list(map(int, lines.pop(0).split(",")))
  assert len(your_ticket) == len(rules)

  lines.pop(0)  # skip empty line
  nearby_tickets = []
  lines.pop(0)  # skip "nearby tickets:"
  for line in lines:
    new_ticket = list(map(int, line.split(",")))
    assert len(new_ticket) == len(rules)
    nearby_tickets.append(new_ticket)

  return rules, your_ticket, nearby_tickets


def part_one(mydata):
  rules, your_ticket, nearby_tickets = parse(mydata)

  ticket_scanning_error_rate = 0
  for ticket in nearby_tickets:
    for value in ticket:
      valid = False
      for low1, high1, low2, high2 in rules.values():
        if (low1 <= value <= high1) or (low2 <= value <= high2):
          valid = True
          break
      if not valid:
        ticket_scanning_error_rate += value

  return ticket_scanning_error_rate


def part_two(mydata):
  rules, your_ticket, nearby_tickets = parse(mydata)

  valid_tickets = []
  for ticket in nearby_tickets:
    valid = True
    for value in ticket:
      if not any(
        (low1 <= value <= high1) or (low2 <= value <= high2)
        for low1, high1, low2, high2 in rules.values()
      ):
        valid = False
        break
    if valid:
      valid_tickets.append(ticket)

  # Further processing would be needed to determine the order of fields.
  # We have a sieve-logic.
  # First, we will locate where the first field can be
  n_fields = len(rules)
  permissible_allocations = [[1 for _ in range(n_fields)] for _ in range(n_fields)]

  for field_num in range(n_fields):
    low1, high1, low2, high2 = list(rules.values())[field_num]
    for test_pos in range(n_fields):
      for ticket in valid_tickets:
        value = ticket[test_pos]
        # Check if this value is valid for the current field
        if not ((low1 <= value <= high1) or (low2 <= value <= high2)):
          permissible_allocations[field_num][test_pos] = 0
          break

  # we will sort the fields by the number of permissible allocations
  # this means we can start to allocate very constrained fields first
  field_order1 = sorted(range(n_fields), key=lambda x: sum(permissible_allocations[x]))
  # in this case, row 15 has a single permissible allocation, so it will be allocated first
  # and field_order1[0] == 15
  # so rearranged field 0 has name rules.keys()[field_order1[0]]
  ok_matrix = [permissible_allocations[i] for i in field_order1]

  # the 'ok_matrix' contains 1s where the field can be and 0s where it cannot be.
  # after sorting the data, I realized that the first row has a single 1, which means that this field can only be at one position
  # the next had two 1s, but one was blocked by the first allocation, so it also has a single 1
  # so we can make allocations greedily
  field_order = []
  for field_num in range(n_fields):
    possible_positions = [
      pos
      for pos in range(n_fields)
      if ok_matrix[field_num][pos] == 1 and pos not in field_order
    ]
    assert len(possible_positions) == 1, (
      "This input needs a DFS style algorithm to allocate fields"
    )
    field_order.append(possible_positions[0])

  # the 'field_order' now contains which field is at which position
  # if 'field_order[k] = 2' it means that column 2 corresponds to field field_order1[k]
  # and that field has name rules.keys()[field_order1[k]]
  res = 1
  for k in range(n_fields):
    field_name = list(rules.keys())[field_order1[k]]
    if field_name.startswith("departure"):
      res *= your_ticket[field_order[k]]

  return res


def main():
  mydata = read_input(16)
  res = part_one(mydata)
  assert res == 21980

  res = part_two(mydata)
  assert res == 1439429522627


if __name__ == "__main__":
  main()
