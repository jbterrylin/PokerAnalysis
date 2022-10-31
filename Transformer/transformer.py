from Enum.GameType import GameType
from Enum.PokerHand import PokerHand
from Model.Game import Game
from Model.Move import Move, PlayerMove
from Model.Player import Player
from Model.HeroCard import HeroCard
from Model.HeroHand import HeroHand
from Enum.GameTurn import GameTurn
from Helper.Convert import strToInt, strToFloat
from Helper.Definer.Omaha import check_hand as omaha_check_hand
from lib import *


def singleGame(lines):
	# print(lines)
	game = Game()
	gameTurn = None
	for line in lines:
		match regex_spm.fullmatch_in(line):
			case r"Poker Hand .*: .*  (.*) - .*":
				regex = re.compile(r"Poker Hand (.*): (.*)  \((.*)\) - (.*) (.*)")
				mo = regex.search(line)
				game.Id = mo.group(1)
				match mo.group(2):
					case GameType.OMAHA_PL.value:
						game.GameType = GameType.OMAHA_PL
				game.Blind = mo.group(3)
				game.Day = datetime.strptime(mo.group(4), '%Y/%m/%d')
				game.DateTime = datetime.strptime(mo.group(5), '%H:%M:%S')
			case r".* Seat #1 is the .*":
				regex = re.compile(r".* Seat #1 is the (.*)")
				mo = regex.search(line)
				game.seat1Pos = mo.group(1)
			case r"Seat .*: .* \(\$.* in chips\)":
				regex = re.compile(r"Seat (.*): (.*) \(\$(.*) in chips\)")
				mo = regex.search(line)
				player = Player()
				player.Id = mo.group(2)
				player.initMoney = mo.group(3)
				game.seat[strToInt(mo.group(1))] = player
			case r".*: posts .* \$.*":
				regex = re.compile(r"(.*): posts (.*) \$(.*)")
				mo = regex.search(line)
				move = PlayerMove()
				move.player = mo.group(1)
				move.move = Move.POST
				move.moveRef = mo.group(2)
				# if mo.group(2) == "small blind":
				#   move.moveRef = MoveRef.SMALL_BLIND
				move.money = strToFloat(mo.group(3))
				game.init.append(move)
			case r"\*\*\* HOLE CARDS \*\*\*":
				gameTurn = GameTurn.PREFLOP
			case r"\*\*\* .*FLOP \*\*\* .*":
				gameTurn = GameTurn.FLOP
			case r"\*\*\* .*TURN \*\*\* .*":
				gameTurn = GameTurn.TURN
			case r"\*\*\* .*RIVER \*\*\* .*":
				gameTurn = GameTurn.RIVER
			case r"Dealt to Hero \[.*\]":
				regex = re.compile(r"Dealt to Hero \[(.*)\]")
				mo = regex.search(line)
				game.heroCard = HeroCard(mo.group(1).split(" "))
			case r".*: .* \$.*" | r".*: .* \$.* to \$.*" | r".*: folds":
				move = PlayerMove()
				if re.search("(.*): folds", line):
					regex = re.compile(r"(.*): folds")
					mo = regex.search(line)
					move.player = mo.group(1)
					move.move = Move.FOLD
				elif re.search("(.*): raises \$(.*) to \$(.*)", line):
					regex = None
					if re.search("(.*): (.*) and is all-in", line):
						regex = re.compile(r"(.*): raises \$(.*) to \$(.*) and is all-in")
						move.isAllIn = True
					else:
						regex = re.compile(r"(.*): raises \$(.*) to \$(.*)")
					mo = regex.search(line)
					move.player = mo.group(1)
					move.move = Move.RAISE
					move.money = strToFloat(mo.group(3))
					move.moveRef = strToFloat(mo.group(2))
					if re.search("(.*): (.*) and is all-in", line):
						move.isAllIn = True
				else:
					regex = None
					if re.search("(.*): (.*) and is all-in", line):
						regex = re.compile(r"(.*): (.*) \$(.*) and is all-in")
						move.isAllIn = True
					else:
						regex = re.compile(r"(.*): (.*) \$(.*)")
					mo = regex.search(line)
					move.player = mo.group(1)
					move.money = strToFloat(mo.group(3))

					match mo.group(2):
						case "bets":
							move.move = Move.BET
						case "calls":
							move.move = Move.CALL
				match gameTurn:
					case GameTurn.PREFLOP:
						game.preFlop.append(move)
					case GameTurn.FLOP:
						game.flop.append(move)
					case GameTurn.TURN:
						game.turn.append(move)
					case GameTurn.RIVER:
						game.river.append(move)
			case r"Uncalled bet \(\$.*\) returned to .*":
				regex = re.compile(r"Uncalled bet \(\$(.*)\) returned to (.*)")
				mo = regex.search(line)
				move = PlayerMove()
				move.player = mo.group(2)
				move.move = Move.RETURN
				move.money = strToFloat(mo.group(1))
			case r".*: shows \[.*\] \(.*\)":
				regex = re.compile(r"(.*): shows \[(.*)\] \((.*)\)")
				mo = regex.search(line)
				move = PlayerMove()
				move.player = mo.group(1)
				move.card = mo.group(2).split(" ")
				move.moveRef = mo.group(3)
				match gameTurn:
					case GameTurn.PREFLOP:
						game.preFlop.append(move)
					case GameTurn.FLOP:
						game.flop.append(move)
					case GameTurn.TURN:
						game.turn.append(move)
					case GameTurn.RIVER:
						game.river.append(move)
			case r".* collected \$.* from pot":
				regex = re.compile(r"(.*) collected \$(.*) from pot")
				mo = regex.search(line)
				move = PlayerMove()
				move.player = mo.group(1)
				move.move = Move.COLLECT
				move.money = strToFloat(mo.group(2))
				game.showDown.append(move)
			case r"Hand was run .* times":
				regex = re.compile(r"Hand was run (.*) times")
				mo = regex.search(line)
				match (mo.group(1)):
					case "two":
						game.nBoard = 2
					case "three":
						game.nBoard = 3
			case r".*Board \[(.*)\]":
				regex = re.compile(r"(.*)Board \[(.*)\]")
				mo = regex.search(line)
				game.board.append(mo.group(2).split(" "))
			case r"Total pot \$(.*) \| Rake \$(.*) \| Jackpot \$(.*) \| Bingo \$(.*)":
				regex = re.compile(r"Total pot \$(.*) \| Rake \$(.*) \| Jackpot \$(.*) \| Bingo \$(.*)")
				mo = regex.search(line)
				game.totalPot = strToFloat(mo.group(1))
			case r".*":
				# use for debug
				match regex_spm.fullmatch_in(line):
					case r"Dealt to (.*)" | r"\*\*\* (.*) \*\*\*":
						continue
					case r"Seat \d: (.*) folded before Flop(.*)" | r"Seat \d: (.*) showed \[(.*)\] and (.*) with (.*)":
						continue
					case _:
						print(line)
	nCardEachTurn = []
	match game.GameType:
		case GameType.OMAHA_PL:
			nCardEachTurn = GameType.OMAHA_PL.getNBoardCardEachTurn()
		case _:
			nCardEachTurn = GameType.OMAHA_PL.getNBoardCardEachTurn()
	tmp = 0
	for n in nCardEachTurn:
		tmp += n
		match game.GameType:
			case GameType.OMAHA_PL:
				for board in game.board:
					print(board[:tmp])
					rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, board[:tmp])
			case _:
				# check_hand(game.heroCard)
				rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, board[:tmp])
		heroHand = HeroHand()
		heroHand.evaluator = evaluator
		heroHand.rank = rank
		match hand:
			case PokerHand.ROYAL_FLUSH.value:
				heroHand.hand = PokerHand.ROYAL_FLUSH
			case PokerHand.STRAIGHT_FLUSH.value:
				heroHand.hand = PokerHand.STRAIGHT_FLUSH
			case PokerHand.FOUR_OF_THE_KIND.value:
				heroHand.hand = PokerHand.FOUR_OF_THE_KIND
			case PokerHand.FULL_HOUSE.value:
				heroHand.hand = PokerHand.FULL_HOUSE
			case PokerHand.FLUSH.value:
				heroHand.hand = PokerHand.FLUSH
			case PokerHand.STRAIGHT.value:
				heroHand.hand = PokerHand.STRAIGHT
			case PokerHand.THREE_OF_THE_KIND.value:
				heroHand.hand = PokerHand.THREE_OF_THE_KIND
			case PokerHand.TWO_PAIR.value:
				heroHand.hand = PokerHand.TWO_PAIR
			case PokerHand.ONE_PAIR.value:
				heroHand.hand = PokerHand.ONE_PAIR
			case PokerHand.HIGH_CARD.value:
				heroHand.hand = PokerHand.HIGH_CARD
		game.heroHand.append(heroHand)
	return game
