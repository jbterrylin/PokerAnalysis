
from pickle import NONE


class Game:
  Id = ""
  Blind = ""
  GameType = ""
  Day = ""
  DateTime = ""
  seat1Pos = ""
  seat = {}
  nBoard = 1
  board = []
  heroCard = []
  init = []
  preFlop = []
  flop = []
  turn = []
  river = []
  showDown = []
  # include every turn hand (preflop pair A, flop trip A, Turn full house...)
  heroHand = []
  finalHands = []
  totalPot = 0
  heroResult = None
  isShowDown = False