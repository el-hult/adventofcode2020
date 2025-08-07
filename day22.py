from util import read_input
from collections import deque


def parse_hands(raw_input) -> tuple[list[int], list[int]]:
  lines = raw_input.strip().splitlines()
  player1 = []
  player2 = []

  curr_player = None
  for line in lines:
    if line.strip() == "Player 1:":
      curr_player = 1
      continue
    elif line.strip() == "Player 2:":
      curr_player = 2
      continue
    elif line.strip() == "":
      continue

    card_val = int(line.strip())
    if curr_player == 1:
      player1.append(card_val)
    elif curr_player == 2:
      player2.append(card_val)
    else:
      raise ValueError(f"Unexpected player number: {curr_player}")

  return player1, player2


def play_combat(player1: list[int], player2: list[int]) -> tuple[int, int]:
  player1 = deque(player1)
  player2 = deque(player2)

  while len(player1) > 0 and len(player2) > 0:
    card1 = player1.popleft()
    card2 = player2.popleft()

    if card1 > card2:
      player1.append(card1)
      player1.append(card2)
    else:
      player2.append(card2)
      player2.append(card1)

  if len(player1) == 0:
    return 2, player2
  else:
    return 1, player1


def play_one_game_recursive_combat(
  player1: list[int], player2: list[int]
) -> tuple[int, int]:
  seen_round_states = set()

  while len(player1) > 0 and len(player2) > 0:
    round_hash = hash((tuple(player1), tuple(player2)))
    if round_hash in seen_round_states:
      return 1, None
    seen_round_states.add(round_hash)

    card1 = player1.pop(0)
    card2 = player2.pop(0)
    if len(player1) >= card1 and len(player2) >= card2:
      sub_winner, _ = play_one_game_recursive_combat(player1[:card1], player2[:card2])
    else:
      sub_winner = 1 if card1 > card2 else 2

    if sub_winner == 1:
      player1.append(card1)
      player1.append(card2)
    else:
      player2.append(card2)
      player2.append(card1)

  if len(player1) == 0:
    return 2, player2
  else:
    return 1, player1


def score(hand):
  return sum(rank * value for rank, value in enumerate(reversed(hand), start=1))


raw = read_input(22)

p1, p2 = parse_hands(raw)
_, hand = play_combat(p1, p2)
ans_1 = score(hand)
assert ans_1 == 35818, "First try"

_, hand = play_one_game_recursive_combat(p1, p2)
ans_2 = score(hand)
assert ans_2 == 34771, "First try"
