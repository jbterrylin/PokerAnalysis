from Enum.GameType import GameType
from Enum.PokerHand import PokerHand
from Helper.Definer.HandEvaluate import check_hand as omaha_check_hand
from Helper.Definer.HandEvaluate import check_hole_card as omaha_check_hole_card

from Model.HeroHand import HeroHand


def setHeroHandNCardHelper(rank, hand, evaluator):
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
	return heroHand


def setHeroHandNCard(game):
	nCardEachTurn = []
	match game.gameType:
		case GameType.OMAHA_PL:
			nCardEachTurn = GameType.OMAHA_PL.getNBoardCardEachTurn()
		case _:
			nCardEachTurn = GameType.OMAHA_PL.getNBoardCardEachTurn()

	if len(game.board) != 0:
		for board in game.board:
			if len(board) is not len(game.board[0]):
				board = game.board[0][:len(board)+1] + board
			tmp = 0
			tmpHeroHands = []
			for n in nCardEachTurn:
				tmp += n
				if len(board) >= tmp:
					match game.gameType:
						case GameType.OMAHA_PL:
							rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, board[:tmp])
						case _:
							rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, board[:tmp])
					tmpHeroHands.append(setHeroHandNCardHelper(rank, hand, evaluator))
			game.heroHand.append(tmpHeroHands)

	game.heroCard.score = omaha_check_hole_card(game.heroCard.cards)
	return game
