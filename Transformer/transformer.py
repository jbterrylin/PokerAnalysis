import Model
from Model.Game import Game, NShowDown
from Model.Move import Move, MoveRef, PlayerMove
from Model.Player import Player
import Enum
from Enum.GameTurn import GameTurn
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
        game.GameType = mo.group(2)
        game.Blind = mo.group(3)
        game.Day = mo.group(4)
        game.DateTime = mo.group(5)
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
        try:
          game.seat[int(mo.group(1))] = player
        except:
          print("seat x is not number")
      case r".*: posts .* \$.*":
        regex = re.compile(r"(.*): posts (.*) \$(.*)")
        mo = regex.search(line)
        move = PlayerMove()
        move.player = mo.group(1)
        move.move = Move.POST
        move.moveRef = mo.group(2)
        # if mo.group(2) == "small blind":
        #   move.moveRef = MoveRef.SMALL_BLIND
        move.money = mo.group(3)
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
        game.heroCard = mo.group(1).split(" ")
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
          move.money = mo.group(3)
          move.moveRef = mo.group(2)
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
          move.money = mo.group(3)
          
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
        move.money = mo.group(1)
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
        move.money = mo.group(2)
        game.showDown.append(move)
      case r"Hand was run .* times":
        regex = re.compile(r"Hand was run (.*) times")
        mo = regex.search(line)
        match(mo.group(1)):
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
        game.totalPot = mo.group(1)
      case r".*":
        # use for debug
        match regex_spm.fullmatch_in(line):
          case r"Dealt to (.*)" | r"\*\*\* (.*) \*\*\*":
            continue
          case r"Seat \d: (.*) folded before Flop(.*)" | r"Seat \d: (.*) showed \[(.*)\] and (.*) with (.*)":
            continue
          case _:
            print(line)
  return game