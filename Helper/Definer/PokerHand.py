import Hand as h


def check_hand(hand):
  if h.check_straight_flush(hand):
    return 9
  if h.check_four_of_a_kind(hand):
      return 8
  if h.check_full_house(hand):
      return 7
  if h.check_flush(hand):
      return 6
  if h.check_straight(hand):
      return 5
  if h.check_three_of_a_kind(hand):
      return 4
  if h.check_two_pairs(hand):
      return 3
  if h.check_one_pairs(hand):
      return 2
  return 1
