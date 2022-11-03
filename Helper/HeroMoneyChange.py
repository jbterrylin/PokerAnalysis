from Enum.Common import HERO, WIN, LOSE
from Model.Move import Move


def heroMoneyChange(game):
	if game.sumBets.get(HERO) is not None:
		for sd in game.showDown:
			heroCollect = next((g for g in sd if g.player == HERO and g.move == Move.COLLECT), None)
			if heroCollect is not None:
				game.heroMoneyChange += heroCollect.money - game.sumBets[HERO]
			else:
				game.heroMoneyChange += -game.sumBets[HERO]
		if game.heroMoneyChange > 0:
			game.heroResult = WIN
		elif game.heroMoneyChange < 0:
			game.heroResult = LOSE
	return game
