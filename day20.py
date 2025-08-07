import pprint
import copy
from util import read_input
import re

# The symmetry group for the square tile is the dihedral group D4, which has 8 symmetries:
SYM_ID = 0
SYM_R90 = 1  # rotate 90 degrees clockwise
SYM_R180 = 2  # rotate 180 degrees
SYM_R270 = 3  # rotate 90 degrees counter-clockwise
SYM_FLIP_H = 4  # flip horizontally
SYM_FLIP_V = 5  # flip vertically
SYM_FLIP_D1 = 6  # flip along diagonal from top left to bottom right
SYM_FLIP_D2 = 7  # flip along diagonal from top right to bottom left
D4 = [
  SYM_ID,
  SYM_R90,
  SYM_R180,
  SYM_R270,
  SYM_FLIP_H,
  SYM_FLIP_V,
  SYM_FLIP_D1,
  SYM_FLIP_D2,
]
type Sym = int
type TileNum = int

DIR_UP = "U"
DIR_DOWN = "D"
DIR_LEFT = "L"
DIR_RIGHT = "R"
type Dir = str

type OriTile = tuple[TileNum, Sym]  # (tile number, symmetry)

type Allocations = list[
  list[OriTile | None]
]  # 2D array of tiles, where each tile is an OriTile or None


def does_match(candidate: OriTile, placed: OriTile, dir: Dir) -> bool:
  """If there is a placed tile, and we want to place a candidate tile in the given direction, can we?"""
  c_tile = tile_data_2[candidate[0]][candidate[1]]
  p_tile = tile_data_2[placed[0]][placed[1]]
  if dir == DIR_UP:
    return c_tile[-1] == p_tile[0]
  elif dir == DIR_DOWN:
    return c_tile[0] == p_tile[-1]
  elif dir == DIR_LEFT:
    return all(rc[-1] == rp[0] for rc, rp in zip(c_tile, p_tile))
  elif dir == DIR_RIGHT:
    return all(rc[0] == rp[-1] for rc, rp in zip(c_tile, p_tile))
  else:
    raise ValueError(f"Unknown direction {dir}")


def can_place(state: Allocations, candidate: OriTile, row: int, col: int) -> bool:
  """Can we place tile_num at (row, col) in the array?

  Will only check cardinal directions, so no diagonals.
  Diagonally adjacent tiles must align in the corners, so be sure to not place tiles diagonally next to each other.

  e.g. in a 2x2 grid, the placement order
  1 2
  3 4
  is valid, since tile 4 is placed when 2 is already placed, ensuring that the corner between 1 and 4 will align.

  The placement order
  1 3
  4 2
  is not good, since it might be that 1 and 2 do not have a shared corner, and this will be revealed when we realize no choice
  of tile can be made for tile 3 without violating 2 or 1. Thus, we get very inefficient explorations as we have 16 tries for getting 3
  right before giving up, and choosing some new try for 2.
  """
  if row > 0 and state[row - 1][col] is not None:
    # can this candidate be placed under the tile above?
    if not does_match(candidate, state[row - 1][col], DIR_DOWN):
      return False
  if col > 0 and state[row][col - 1] is not None:
    # can this candidate be placed to the right of the tile to the left?
    if not does_match(candidate, state[row][col - 1], DIR_RIGHT):
      return False
  if row < array_size - 1 and state[row + 1][col] is not None:
    # can this candidate be placed above the tile below?
    if not does_match(candidate, state[row + 1][col], DIR_UP):
      return False
  if col < array_size - 1 and state[row][col + 1] is not None:
    # can this candidate be placed to the left of the tile to the right?
    if not does_match(candidate, state[row][col + 1], DIR_LEFT):
      return False
  return True


def enact_symmetry(tile: str, sym: Sym) -> list[list[bool]]:
  """Apply symmetry sym to tile.
  Given a tile in string format (\n separated rows of . and #) return a 2D array of bools
  where True means a # and False means a ."""
  rows = tile.splitlines()
  nrows = len(rows)
  ncols = len(rows[0])
  out = [[False for _ in range(ncols)] for _ in range(nrows)]

  for r in range(nrows):
    for c in range(ncols):
      if sym == SYM_ID:
        out[r][c] = rows[r][c] == "#"
      elif sym == SYM_R90:
        out[c][nrows - 1 - r] = rows[r][c] == "#"
      elif sym == SYM_R180:
        out[nrows - 1 - r][ncols - 1 - c] = rows[r][c] == "#"
      elif sym == SYM_R270:
        out[ncols - 1 - c][r] = rows[r][c] == "#"
      elif sym == SYM_FLIP_H:
        out[r][ncols - 1 - c] = rows[r][c] == "#"
      elif sym == SYM_FLIP_V:
        out[nrows - 1 - r][c] = rows[r][c] == "#"
      elif sym == SYM_FLIP_D1:
        out[c][r] = rows[r][c] == "#"
      elif sym == SYM_FLIP_D2:
        out[ncols - 1 - c][nrows - 1 - r] = rows[r][c] == "#"
      else:
        raise ValueError(f"Unknown symmetry {sym}")

  return out


my_input = read_input(20)

tile_data: dict[TileNum, str] = {}
rawtiles = my_input.strip().split("\n\n")
for tile in rawtiles:
  tile_header, tile_image = tile.split("\n", 1)
  m = re.match(r"Tile (\d+):", tile_header)
  tile_num = int(m.group(1))
  tile_data[tile_num] = tile_image

array_size = 12
assert len(tile_data) == array_size * array_size
tile_nums = sorted(tile_data.keys())
tile_data_2 = {
  tile_num: {ori: enact_symmetry(tile_data[tile_num], ori) for ori in range(8)}
  for tile_num in tile_nums
}
pprint.pprint(tile_data_2)

# when allocating a tile to the array, we store tile number and the symmetry on it
array_allocations: list[list[OriTile | None]] = [
  [None for _ in range(array_size)] for _ in range(array_size)
]


#
# Make a DFS search for placing tiles in the array without violations
# The `state` here is the current array allocation
# the revealed_states set will only hold hashes of the states, in order to avoid creating copies of the states for storage in the
# revealed_states set.
#
def hash_state(state: list[list[OriTile | None]]) -> str:
  """The 'frontier' set dont need to hold the full states, just some hashes of it.
  this function will create a hash of the state for this purpose."""
  flattened_state = tuple(
    x for row in state for x in row
  )  # TODO check if any Tiles have identical data (i.e.g maybe (1,SYM_ID) and (3,SYM_R90) look the same, then their hash should be the same), so that we can deduplicate hashes
  return hash(flattened_state)


revealed_states = {hash_state(array_allocations)}
frontier = [
  array_allocations
]  # the state stack to pop from when expanding the next state


# TODO the first tile dont need all 8 symmetries tried, since flippding D1 and ID will create the same solution up to mirroring back.
# I think that the first tile only needs at most 4 of the symmetries tried. This could cut runtime in hald possibly
k = 0
while frontier:
  print(f"Expandi state {k}")
  print(f"Frontier size: {len(frontier)}")
  print(f"Revealed size: {len(revealed_states)}")
  k += 1
  state = frontier.pop()

  # find the first empty cell in the array
  n_occupied_cells = sum(1 for row in state for x in row if x is not None)
  # we fill the array in row major order. just need to compute which row/col is the next cell to fill
  row = n_occupied_cells // array_size
  col = n_occupied_cells % array_size
  print(f"{n_occupied_cells} occupied, next cell to fill is ({row},{col})")

  if n_occupied_cells == array_size * array_size:
    # No empty cells; we are done!
    print("Found a solution!")
    pprint.pprint(state)
    break

  # try to place a tile in the empty spots
  used_tiles = set(x[0] for row in state for x in row if x is not None)
  could_expand_state = False
  unused_tiles = set(tile_nums) - used_tiles
  print(f"Unused tiles: {len(unused_tiles)}")

  def place_all_valid(row, col):
    for tile_num in unused_tiles:
      for ori in D4:
        candidate = (tile_num, ori)
        if can_place(state, candidate, row, col):
          state[row][col] = candidate
          state_hash = hash_state(state)
          if state_hash not in revealed_states:
            new_state = copy.deepcopy(state)
            revealed_states.add(state_hash)
            frontier.append(new_state)
          state[row][col] = None

  place_all_valid(row, col)

# Verify the solution
assert all(x is not None for row in state for x in row), (
  "Every position in the array should be filled"
)
used_tiles = set(x[0] for row in state for x in row)
assert len(used_tiles) == array_size * array_size, (
  "All tiles should be used exactly once"
)
assert used_tiles == set(tile_nums), "All tiles should be used exactly once"


def print_tile(tile_num, ori: Sym):
  """Print the tile in the given orientation."""
  tile = tile_data_2[tile_num][ori]
  print(f"Tile: {tile_num}, orientation: {ori}")
  for row in tile:
    print("".join("#" if x else "." for x in row))
  print()


# Verify each tile matches to the right and down
for r in range(array_size - 1):
  for c in range(array_size - 1):
    this_tile = state[r][c]
    right_tile = state[r][c + 1]
    if not does_match(right_tile, this_tile, DIR_RIGHT):
      print(
        f"Tile {this_tile[0]} at ({r},{c}) does not match right tile {right_tile[0]} at ({r},{c + 1})"
      )
      print_tile(*this_tile)
      print_tile(*right_tile)

# get corner tile numbers
n1 = state[0][0][0]  # top left
n2 = state[0][array_size - 1][0]  # top right
n3 = state[array_size - 1][0][0]  # bottom left
n4 = state[array_size - 1][array_size - 1][0]  # bottom
ans_one = n1 * n2 * n3 * n4
print(f"Part one answer: {ans_one}")


# PART TWO! FINDING SEA MONSTERS!

# assemble the image
# each tile is 10x10 but we must remove the borders, so each tile contributes 8x8 to the image
image_data = [["." for _ in range(array_size * 8)] for _ in range(array_size * 8)]
for tile_r in range(array_size):
  for tile_c in range(array_size):
    tile_num, ori = state[tile_r][tile_c]
    tile_image = tile_data_2[tile_num][ori]
    for r in range(8):
      for c in range(8):
        image_data[tile_r * 8 + r][tile_c * 8 + c] = (
          "#" if tile_image[r + 1][c + 1] else "."
        )  # skip borders


def print_image(image: list[list[str]]):
  for row in image:
    print("".join(x for x in row))


print("Assembled image:")
print_image(image_data)

type Image = list[list[str]]


def mark_sea_monsters(image: Image, upper_left_corner: tuple[int, int]) -> bool:
  """
  Is there a sea monster at this position in the image?

                    #
  #    ##    ##    ###
   #  #  #  #  #  #

  if so, mark it by replacing those coords with 'O' in the image
  """
  monster_relative_coords = [
    (0, 18),  # the head of the monster
    (1, 0),
    (1, 5),
    (1, 6),
    (1, 11),
    (1, 12),
    (1, 17),
    (1, 18),
    (1, 19),
    (2, 1),
    (2, 4),
    (2, 7),
    (2, 10),
    (2, 13),
    (2, 16),
  ]
  r, c = upper_left_corner
  if r + 2 >= len(image) or c + 19 >= len(image[0]):
    return False  # not enough space for a sea monster here
  is_sea_monster = all(
    image[r + dr][c + dc] == "#" for dr, dc in monster_relative_coords
  )
  if is_sea_monster:
    for dr, dc in monster_relative_coords:
      image[r + dr][c + dc] = "O"  # mark the monster
  return is_sea_monster


def enact_sym_on_image(image: Image, sym: Sym) -> Image:
  """Apply symmetry sym to image.
  Image is a list of list of characters, where '#' means a filled pixel and '.' means an empty pixel.
  """
  nrows = len(image)
  ncols = len(image[0])
  out = [[" " for _ in range(ncols)] for _ in range(nrows)]

  for r in range(nrows):
    for c in range(ncols):
      if sym == SYM_ID:
        out[r][c] = image[r][c]
      elif sym == SYM_R90:
        out[c][nrows - 1 - r] = image[r][c]
      elif sym == SYM_R180:
        out[nrows - 1 - r][ncols - 1 - c] = image[r][c]
      elif sym == SYM_R270:
        out[ncols - 1 - c][r] = image[r][c]
      elif sym == SYM_FLIP_H:
        out[r][ncols - 1 - c] = image[r][c]
      elif sym == SYM_FLIP_V:
        out[nrows - 1 - r][c] = image[r][c]
      elif sym == SYM_FLIP_D1:
        out[c][r] = image[r][c]
      elif sym == SYM_FLIP_D2:
        out[ncols - 1 - c][nrows - 1 - r] = image[r][c]
      else:
        raise ValueError(f"Unknown symmetry {sym}")

  return out


for sym in D4:
  img = enact_sym_on_image(image_data, sym)
  print(f"Trying symmetry {sym}")
  n_monsters = 0
  for r in range(len(img) - 2):
    for c in range(len(img[0]) - 19):
      if mark_sea_monsters(img, (r, c)):
        n_monsters += 1

  if n_monsters > 0:
    print(f"Found {n_monsters} sea monsters!")
    break

print(n_monsters, "monsters found")
print_image(img)
n_hashes = sum(row.count("#") for row in img)
print(f"Part two answer: {n_hashes} hashes left after marking sea monsters")
