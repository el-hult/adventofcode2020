from util import read_input


def part_one(raw_input):
  lines = raw_input.splitlines()
  state = set()
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == "#":
        state.add((x, y, 0))

  for _ in range(6):
    state = step_simulation_3d(state)

  return len(state)


def step_simulation_3d(state):
  new_state = set()
  cells_to_check = set()

  # Check all active cells and their neighbors
  # these spots define what area of the grid we must simulate
  for x, y, z in state:
    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        for dz in (-1, 0, 1):
          cells_to_check.add((x + dx, y + dy, z + dz))

  for x, y, z in cells_to_check:
    # count the number of active neighbors for each cell
    n_active_neighbors = 0
    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        for dz in (-1, 0, 1):
          if dx == 0 and dy == 0 and dz == 0:
            continue
          neighbor = (x + dx, y + dy, z + dz)
          if neighbor in state:
            n_active_neighbors += 1

    # Apply the rules
    if (x, y, z) in state and n_active_neighbors in (2, 3):
      new_state.add((x, y, z))
    elif (x, y, z) not in state and n_active_neighbors == 3:
      new_state.add((x, y, z))

  return new_state


def step_simulation_4d(state):
  new_state = set()
  cells_to_check = set()

  # Check all active cells and their neighbors
  for x, y, z, w in state:
    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        for dz in (-1, 0, 1):
          for dw in (-1, 0, 1):
            cells_to_check.add((x + dx, y + dy, z + dz, w + dw))

  # simulate each cell
  for x, y, z, w in cells_to_check:
    # count active neighbors
    n_active_neighbors = 0
    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        for dz in (-1, 0, 1):
          for dw in (-1, 0, 1):
            if dx == 0 and dy == 0 and dz == 0 and dw == 0:
              continue
            neighbor = (x + dx, y + dy, z + dz, w + dw)
            if neighbor in state:
              n_active_neighbors += 1

    # Apply the rules
    if (x, y, z, w) in state and n_active_neighbors in (2, 3):
      new_state.add((x, y, z, w))
    elif (x, y, z, w) not in state and n_active_neighbors == 3:
      new_state.add((x, y, z, w))

  return new_state


def part_two(raw_input):
  lines = raw_input.splitlines()
  state = set()
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == "#":
        state.add((x, y, 0, 0))

  for _ in range(6):
    state = step_simulation_4d(state)

  return len(state)


test_input = """.#.
..#
###
"""
res = part_one(test_input)
assert res == 112, f"Test failed, expected 112 but got {res}"


my_input = read_input(17)
resA = part_one(my_input)
assert resA > 208, "One failed attempt."
assert resA == 255, "Then it worked!"

res2 = part_two(test_input)
assert res2 == 848, f"Test failed, expected 848 but got {res2}"

resB = part_two(my_input)
assert resB == 2340, "First try!"
