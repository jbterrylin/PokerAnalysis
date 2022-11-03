from Enum.GameTurn import GameTurn
from Model.Move import MoveRef, Move
from Helper.Combine import *


def playerBetEachTurnHelper(moves):
	result = {}
	if len(moves) > 0:
		for move in sorted(moves, key=lambda x:
			x.Id if x.moveRef != MoveRef.SMALL_BLIND or x.moveRef != MoveRef.BIG_BLIND else -1):
			match move.move:
				case Move.CALL:
					result[move.player] = noneTo0(result.get(move.player)) + move.money
				case Move.RETURN:
					result[move.player] = noneTo0(result.get(move.player)) - move.money
				case Move.RAISE | Move.BET | Move.POST:
					result[move.player] = move.money
	else:
		return None
	return result


def playerBetEachTurn(game):
	inits = {}
	initBlindMoves = []
	for init in sorted(game.init, key=lambda x: x.Id, reverse=True):
		if init.moveRef == MoveRef.SMALL_BLIND or init.moveRef == MoveRef.BIG_BLIND:
			initBlindMoves.append(init)
		else:
			inits[init.player] = init.money
	preFlops = playerBetEachTurnHelper(initBlindMoves + game.preFlop)

	sumResult = combineDictWithSum(inits, preFlops)
	result = {
		GameTurn.INIT: inits,
		GameTurn.PREFLOP: preFlops
	}

	for key, value in {
		GameTurn.FLOP: playerBetEachTurnHelper(game.flop),
		GameTurn.TURN: playerBetEachTurnHelper(game.turn),
		GameTurn.RIVER: playerBetEachTurnHelper(game.river)}.items():
		if value is not None:
			sumResult = combineDictWithSum(sumResult, value)
			result[key] = value
		else:
			game.bets = result
			game.sumBets = sumResult
			return game

	if sum(sumResult.values()) != game.totalPot:
		print(sumResult.values())
		print(sum(sumResult.values()), game.totalPot)
		print(game.Id, "playerBetEachTurn error")

	game.bets = result
	game.sumBets = sumResult
	return game
