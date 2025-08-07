from util import read_input
raw = read_input(24)
lines = raw.strip().splitlines()

# https://www.redblobgames.com/grids/hexagons/ has coordinate systems for hexagonal grids!
# I will use cube coordinates, because I think they are rad!
# coordinates are (q,r,s) where x + y + z = 0
# constant q = north west
# r = east
# s = south west

black_tiles = set()
for line in lines:
  q,r,s = 0,0,0
  while line:
    if line[:2] == 'nw':
      r -= 1
      s += 1
      line = line[2:]
    elif line[:2] == 'ne':
      q += 1
      r -= 1
      line = line[2:]
    elif line[:1] == 'e':
      q += 1
      s -= 1
      line = line[1:]
    elif line[:2] == 'se':
      r += 1
      s -= 1
      line = line[2:]
    elif line[:2] == 'sw':
      q -= 1
      r += 1
      line = line[2:]
    elif line[:1] == 'w':
      q -= 1
      s += 1
      line = line[1:]
    else:
      raise ValueError(f"Unexpected direction in line: {line}")
  if (q,r,s) in black_tiles:
    black_tiles.remove((q,r,s))
  else:
    black_tiles.add((q,r,s))

assert len(black_tiles) == 375, "First try!"

def get_adjacent_tiles(qrs) -> list[tuple[int,int,int]]:
  q, r, s = qrs
  return [
    (q + 1, r - 1, s),
    (q + 1, r, s - 1),
    (q, r + 1, s - 1),
    (q - 1, r + 1, s),
    (q - 1, r, s + 1),
    (q, r - 1, s + 1)
  ]


def one_step_flips(black_tiles):
  new_tiles = set()
  to_check = set()
  for t in black_tiles:
    to_check.add(t)
    to_check.update(get_adjacent_tiles(t))

  for t in to_check:
    n_adj_blk = sum(1 for adj in get_adjacent_tiles(t) if adj in black_tiles)
    is_black = t in black_tiles
    if is_black and n_adj_blk == 0 or n_adj_blk > 2:
      pass # this tile is flipped to white, i.e. not added to new_tiles
    elif is_black:
      new_tiles.add(t) # stays black
    elif not is_black and n_adj_blk == 2:
      new_tiles.add(t)
    elif not is_black:
      pass # stays white, i.e. not added to new_tiles
  return new_tiles


for day in range(100):
  black_tiles = one_step_flips(black_tiles)

assert len(black_tiles) == 3937, "First try!"
