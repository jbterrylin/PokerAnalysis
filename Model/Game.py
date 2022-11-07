from enum import Enum

from Enum.GameTurn import GameTurn
from Helper.Convert import dictWithClassValueToDict, classesToDict, allEnumInDictsToVal, allEnumInDictToVal, toDict


class Result(Enum):
	WIN = "WIN"
	LOSE = "LOSE"
	CHOP = "CHOP"


# class NShowDown(Enum):
#   FIRST = "FIRST"
#   SECOND = "SECOND"
#   THIRD = "THIRD"


class Game:
	filePath = ""
	id = ""
	blind = ""
	gameType = ""
	day = ""
	dateTime = ""
	seat1Pos = ""
	seat = {}
	nBoard = 1
	board = []
	heroCard = None
	init = []
	preFlop = []
	flop = []
	turn = []
	river = []
	showDown = []
	sumMoves = []
	# include every turn hand (preflop pair A, flop trip A, Turn full house...)
	heroHand = []
	finalHands = []
	totalPot = 0
	heroResult = None
	isShowDown = False
	bets = None
	sumBets = None
	heroMoneyChange = 0

	def __init__(self):
		self.seat = {}
		self.board = []
		self.init = []
		self.preFlop = []
		self.flop = []
		self.turn = []
		self.river = []
		self.showDown = []
		self.sumMoves = []
		self.heroHand = []
		self.finalHands = []

	def joinMovesWithoutInit(self):
		for turn in [
			(self.preFlop, GameTurn.PREFLOP),
			(self.flop, GameTurn.FLOP),
			(self.turn, GameTurn.TURN),
			(self.river, GameTurn.RIVER)
		]:
			for m in turn[0]:
				m.turn = turn[1]
				self.sumMoves.append(m)

	def toDict(self):
		result = self.__dict__
		result["seat"] = dictWithClassValueToDict(self.seat)

		result["init"] = classesToDict(self.init)
		result["preFlop"] = classesToDict(self.preFlop)
		result["flop"] = classesToDict(self.flop)
		result["turn"] = classesToDict(self.turn)
		result["river"] = classesToDict(self.river)
		result["showDown"] = classesToDict(self.showDown)
		result["sumMoves"] = classesToDict(self.sumMoves)
		result["heroHand"] = classesToDict(self.heroHand)
		result["init"] = allEnumInDictsToVal(result["init"])
		result["preFlop"] = allEnumInDictsToVal(result["preFlop"])
		result["flop"] = allEnumInDictsToVal(result["flop"])
		result["turn"] = allEnumInDictsToVal(result["turn"])
		result["river"] = allEnumInDictsToVal(result["river"])
		result["showDown"] = allEnumInDictsToVal(result["showDown"])
		result["sumMoves"] = allEnumInDictsToVal(result["sumMoves"])
		result["heroHand"] = allEnumInDictsToVal(result["heroHand"])

		result["heroCard"] = toDict(self.heroCard)
		result["blind"] = allEnumInDictToVal(self.blind)
		result["bets"] = allEnumInDictToVal(self.bets)
		return result
