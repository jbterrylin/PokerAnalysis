from enum import Enum


class GameTurn(Enum):
  INIT = "INIT"
  PREFLOP = "PREFLOP"
  FLOP = "FLOP"
  TURN = "TURN"
  RIVER = "RIVER"
  SHOWDOWN = "SHOWDOWN"


class Number(Enum):
  FIRST = "FIRST"
  SECOND = "SECOND"
  THIRD = "THIRD"
