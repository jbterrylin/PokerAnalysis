import Hand as h


def check_hand(holeCard, board):
  comb = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

  bestHand = []
  hand = []
  for c in comb:
    hand = board + holeCard[c[0]] + holeCard[c[1]]
    if h.check_straight_flush(hand):
      bestHand.append(9)
      continue
    if h.check_four_of_a_kind(hand):
      bestHand.append(8)
      continue
    if h.check_full_house(hand):
      bestHand.append(7)
      continue
    if h.check_flush(hand):
      bestHand.append(6)
      continue
    if h.check_straight(hand):
      bestHand.append(5)
      continue
    if h.check_three_of_a_kind(hand):
      bestHand.append(4)
      continue
    if h.check_two_pairs(hand):
      bestHand.append(3)
      continue
    if h.check_one_pairs(hand):
      bestHand.append(2)
      continue
    bestHand.append(1)
  return max(bestHand)
