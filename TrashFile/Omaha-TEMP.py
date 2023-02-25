from TrashFile.OmahaHand import *
from Helper.Definer.CommonHand import value_dict


def check_cards_can_straight(cards):
	values = sorted([value_dict[c[0]] for c in cards])
	if values[1] - values[0] < 5:
		return True
	if values[1] == 13:
		values = [0, values[0]]
		if values[1] - values[0] < 5:
			return True
	return False


def check_cards_can_flush(cards):
	values = np.unique([c[1] for c in cards])
	if len(values) == 1:
		return True
	return False


def check_pocket_pair(cards):
	values = np.unique([c[0] for c in cards])
	if len(values) == 1:
		return True
	return False

def check_hand(holeCard, board):
	comb = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

	bestHand = []
	hand = []
	for c in comb:
		cards = [holeCard[c[0]], holeCard[c[1]]]
		can_straight = check_cards_can_straight(cards)
		can_flush = check_cards_can_flush(cards)
		pocket_pair = check_pocket_pair(cards)
		score, _, hand = score_hand(cards, board, can_straight, can_flush, pocket_pair)
		bestHand.append([hand[::-1], score])
	# print(bestHand)
	topRank = max([c[1] for c in bestHand])
	bestHand = [p for p in bestHand if p[1] == topRank]
	print("-" * 20)
	print(bestHand)
	return bestHand
