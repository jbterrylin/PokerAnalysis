from enum import Enum

class Move(Enum):
  POST = "POST"
  BET = "BET"
  CALL = "CALL"
  RAISE = "RAISE"
  FOLD = "FOLD"
  RETURN = "RETURN"
  SHOW = "SHOW"
  COLLECT = "COLLECT"

class MoveRef(Enum):
  SMALL_BLIND = "SMALL_BLIND"
  BIG_BLIND = "BIG_BLIND"

class PlayerMove:
  player = None
  move = None
  money = 0
  card = []
  moveRef = None
  isAllIn = False