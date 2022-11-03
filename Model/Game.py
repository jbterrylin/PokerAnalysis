from enum import Enum


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
	bets = None
	sumBets = None
	heroMoneyChange = 0

	def __init__(self):
		self.seat = {}
		self.board = []
		self.heroCard = []
		self.init = []
		self.preFlop = []
		self.flop = []
		self.turn = []
		self.river = []
		self.showDown = []
		self.heroHand = []
		self.finalHands = []
