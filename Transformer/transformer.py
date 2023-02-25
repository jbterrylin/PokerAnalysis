from Enum.GameType import GameType
from Enum.PokerHand import PokerHand
from Enum.Common import *
from Model.Game import Game
from Model.Move import Move, PlayerMove, MoveRef
from Model.Player import Player
from Model.HeroCard import HeroCard
from Model.HeroHand import HeroHand
from Enum.GameTurn import GameTurn, Number
from Helper.Convert import strToInt, strToFakeInt
from Helper.Definer.HandEvaluate import check_hand as omaha_check_hand
import regex_spm
import re
from datetime import datetime


def singleGame(lines):
	# print(lines)
	game = Game()
	gameTurn = None
	nShowDown = Number.FIRST
	nMove = 0

	for line in lines:
		match regex_spm.fullmatch_in(line):
			case r"Poker Hand .*: .*  (.*) - .*":
				regex = re.compile(r"Poker Hand (.*): (.*)  \((.*)\) - (.*) (.*)")
				mo = regex.search(line)
				game.id = mo.group(1)
				match mo.group(2).strip():
					case GameType.OMAHA_PL.value:
						game.gameType = GameType.OMAHA_PL
				game.blind = mo.group(3)
				if "/" in mo.group(3):
					game.blind = {
						MoveRef.SMALL_BLIND: strToFakeInt(mo.group(3).split("/")[0].replace("$","")),
						MoveRef.BIG_BLIND: strToFakeInt(mo.group(3).split("/")[1].replace("$",""))
					}
				game.day = datetime.strptime(mo.group(4), '%Y/%m/%d')
				game.dateTime = datetime.strptime(mo.group(5), '%H:%M:%S')
			case r".* Seat #1 is the .*":
				regex = re.compile(r".* Seat #1 is the (.*)")
				mo = regex.search(line)
				game.seat1Pos = mo.group(1)
			case r"Seat .*: .* \(\$.* in chips\)":
				regex = re.compile(r"Seat (.*): (.*) \(\$(.*) in chips\)")
				mo = regex.search(line)
				player = Player()
				player.id = mo.group(2)
				player.initMoney = mo.group(3)
				game.seat[strToInt(mo.group(1))] = player
			case r"Cash Drop to Pot : total \$.*":
				regex = re.compile(r"Cash Drop to Pot : total \$(.*)")
				mo = regex.search(line)
				move = PlayerMove(nMove)
				nMove += 1
				move.player = SYSTEM
				move.move = Move.POST
				move.money = strToFakeInt(mo.group(1))
				move.moveRef = MoveRef.CASH_DROP
				game.init.append(move)
			case r".*: posts .* \$.*":
				regex = re.compile(r"(.*): posts (.*) \$(.*)")
				mo = regex.search(line)
				move = PlayerMove(nMove)
				nMove += 1
				move.player = mo.group(1)
				move.move = Move.POST
				move.moveRef = mo.group(2)
				match mo.group(2).strip():
					case "small blind":
					  move.moveRef = MoveRef.SMALL_BLIND
					case "big blind":
						move.moveRef = MoveRef.BIG_BLIND
				move.money = strToFakeInt(mo.group(3))
				game.init.append(move)
			case r"\*\*\* HOLE CARDS \*\*\*":
				gameTurn = GameTurn.PREFLOP
			case r"\*\*\* .*FLOP \*\*\* .*":
				gameTurn = GameTurn.FLOP
			case r"\*\*\* .*TURN \*\*\* .*":
				gameTurn = GameTurn.TURN
			case r"\*\*\* .*RIVER \*\*\* .*":
				gameTurn = GameTurn.RIVER
			case r"\*\*\* .*SHOWDOWN \*\*\*":
				regex = re.compile(r"\*\*\* (.*)SHOWDOWN \*\*\*")
				mo = regex.search(line)
				match mo.group(1).strip():
					case Number.FIRST.value | "":
						nShowDown = Number.FIRST
					case Number.SECOND.value:
						nShowDown = Number.SECOND
					case Number.THIRD.value:
						nShowDown = Number.THIRD
			case r"Dealt to Hero \[.*\]":
				regex = re.compile(r"Dealt to Hero \[(.*)\]")
				mo = regex.search(line)
				game.heroCard = HeroCard(mo.group(1).split(" "))
			case r".*: .* \$.*" | r".*: .* \$.* to \$.*" | r".*: folds" | r".*: checks":
				move = PlayerMove(nMove)
				nMove+=1
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
					move.money = strToFakeInt(mo.group(3))
					move.moveRef = strToFakeInt(mo.group(2))
					if re.search("(.*): (.*) and is all-in", line):
						move.isAllIn = True
				elif re.search("(.*): checks", line):
					regex = re.compile(r"(.*): checks")
					mo = regex.search(line)
					move.player = mo.group(1)
					move.move = Move.CHECK
				else:
					regex = None
					if re.search("(.*): (.*) and is all-in", line):
						regex = re.compile(r"(.*): (.*) \$(.*) and is all-in")
						move.isAllIn = True
					else:
						regex = re.compile(r"(.*): (.*) \$(.*)")
					mo = regex.search(line)
					move.player = mo.group(1)
					move.money = strToFakeInt(mo.group(3))

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
				move = PlayerMove(nMove)
				nMove += 1
				move.player = mo.group(2)
				move.move = Move.RETURN
				move.money = strToFakeInt(mo.group(1))
				match gameTurn:
					case GameTurn.PREFLOP:
						game.preFlop.append(move)
					case GameTurn.FLOP:
						game.flop.append(move)
					case GameTurn.TURN:
						game.turn.append(move)
					case GameTurn.RIVER:
						game.river.append(move)
			case r".*: shows \[.*\].*":
				regex = re.compile(r"(.*): shows \[(.*)\](.*)")
				mo = regex.search(line)
				move = PlayerMove(nMove)
				nMove += 1
				move.player = mo.group(1)
				move.move = Move.SHOW
				move.card = mo.group(2).split(" ")
				move.moveRef = mo.group(3).strip().replace("(","").replace(")","")
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
				move = PlayerMove(nMove)
				nMove += 1
				move.player = mo.group(1)
				move.move = Move.COLLECT
				move.money = strToFakeInt(mo.group(2))
				match nShowDown:
					case Number.FIRST:
						if len(game.showDown) < 1:
							game.showDown.append([move])
						else:
							game.showDown[0].append(move)
					case Number.SECOND:
						if len(game.showDown) < 2:
							game.showDown.append([move])
						else:
							game.showDown[1].append(move)
					case Number.THIRD:
						if len(game.showDown) < 3:
							game.showDown.append([move])
						else:
							game.showDown[2].append(move)

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
				game.totalPot = strToFakeInt(mo.group(1))
			case r".*":
				# use for debug
				match regex_spm.fullmatch_in(line):
					case r"Dealt to (.*)" | r"\*\*\* (.*) \*\*\*" | r"Seat \d: .*":
						continue
					case r"Seat \d: (.*) folded before Flop(.*)" | r"Seat \d: (.*) showed \[(.*)\] and (.*) with (.*)":
						continue
					case r"(.*): Receives Cashout \(\$.*\)" | r"(.*): Chooses to EV Cashout" | r"(.*): Pays Cashout Risk \(\$.*\)":
						continue
					case _:
						print(game.id)
						print(line)
	return game
