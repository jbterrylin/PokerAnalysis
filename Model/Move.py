from enum import Enum


class Move(Enum):
	POST = "POST"
	CHECK = "CHECK"
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
	CASH_DROP = "CASH_DROP"


class PlayerMove:
	id = 0
	player = None
	move = None
	money = 0
	card = []
	moveRef = None
	isAllIn = False

	def __init__(self, id):
		self.id = id
		self.card = []
