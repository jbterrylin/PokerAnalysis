import threading
from Enum.GameType import GameType
from Enum.PokerHand import PokerHand
from Helper.Definer.Omaha import check_hand as omaha_check_hand
from Model.HeroHand import HeroHand


def setGameResult(game):
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
				if len(game.board) != 0:
					for board in game.board:
						rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, board[:tmp])
				else:
					rank, hand, evaluator = omaha_check_hand(game.heroCard.cards, [])
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