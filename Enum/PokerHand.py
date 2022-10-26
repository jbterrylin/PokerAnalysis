from enum import Enum

class PokerHand(Enum):
  HIGI_CARD = "highest-card"
  ONE_PAIR = "one-pair"
  TWO_PAIR = "two-pairs" 
  THREE_OF_THE_KIND = "three-of-a-kind"
  STRAIGHT = "straight"
  FLUSH = "flush"
  FULL_HOUSE = "full-house"
  FOUR_OF_THE_KIND = "four-of-a-kind"
  STRAIGHT_FLUSH = "straight-flush"