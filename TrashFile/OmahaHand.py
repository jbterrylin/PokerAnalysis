from collections import Counter
from Helper.Definer.CommonHand import value_dict, value_str_dict

import numpy as np


def num_of_kind(cards):
	return Counter(c[0] for c in cards)


def count_pairs(cards):
	return sum(i > 1 for i in num_of_kind(cards).values())


def largest_pair(cards):
	return max(num_of_kind(cards).values())


def straight_checking(cards, board, checkATo5=False):
	values = [c[0] for c in cards] + [c[0] for c in board]
	if len(values) < 5:
		return False

	value_cards = [value_dict[c[0]] for c in cards]
	indices = np.unique(values).tolist()
	indices = sorted(value_dict[v] for v in indices)

	if checkATo5:
		if 13 in indices:
			indices.pop()
			indices.insert(0, 0)
		if 13 in value_cards:
			value_cards.pop()
			value_cards.append(0)

	while len(indices) > 4:
		if value_cards[0] in indices[-5:] and value_cards[1] in indices[-5:]:
			if all((y[0] == y[1] or x > 4) for x, y in enumerate(reversed(list(enumerate(indices, indices[0]))))):
				return True, indices[-5:]
		indices.pop()
	if checkATo5:
		return False, None
	else:
		return straight_checking(cards, board, True)


# return all(x == y for x, y in enumerate(indices, indices[0]))


def flush_checking(cards, board):
	if len(board) < 3:
		return False, None
	cards_suit = Counter(c[1] for c in cards).most_common()[0][0]
	board_same_suit = sorted([c for c in board if c[1] == cards_suit])
	if len(board_same_suit) > 2:
		board_same_suit = value_sort(board_same_suit)
		return True, value_sort(cards + board_same_suit[:3])
	return False, None


def value_sort(cards):
	return sorted(cards, key=lambda x: value_dict[x[0]], reverse=True)


# different with value_sort is sort reverse and handle A,2,3,4,5
def straight_sort(cards):
	values = [c[0] for c in cards]
	sorts = sorted(values, key=lambda x: value_dict[x[0]], reverse=False)
	return sorts


def flush_sort(cards):
	suit_pop = Counter(c[1] for c in cards)
	return sorted(cards, key=lambda x: suit_pop[x[1]], reverse=True)


def pair_sort(cards):
	num = num_of_kind(cards)
	return sorted(cards, key=lambda x: num[x[0]], reverse=True)


def card_vals(cards):
	return [value_dict[c[0]] for c in cards]


def score_hand(cards, board, can_straight, can_flush, pocket_pair):
	# quads
	# cards = ['7h', '6h']
	# board = ['6c', '7c', '7c', '7h', 'Jh']
	cards = ['6h', '6h']
	board = ['7c', '7c', '7c', '7h', 'Jh']
	pocket_pair = True



	board_pairs = num_of_kind(board)
	pairs = num_of_kind(cards + board)


	straight = False
	if can_straight:
		straight, straightInfo = straight_checking(cards, board)

	flush = False
	if can_flush:
		flush, flushInfo = flush_checking(cards, board)

	cards = value_sort(cards)
	hand_score = 0
	if flush and straight:
		board_suits = [h for h in board if h[1] == flushInfo[0][1]]
		straightFlush, straightFlushInfo = straight_checking(cards, board_suits)
		if straightFlush:
			hand_score, cards = 8, [value_str_dict[c] + flushInfo[0][1] for c in straightFlushInfo]
			info = straightFlushInfo
	if hand_score == 0 and max(board_pairs.values()) == 3 and max(pairs.values()) == 4:
		hand_score, quads_sort = 7, pair_sort(cards + board)
		cards = (quads_sort[:4] + value_sort(quads_sort[4:]))[:5]
	# pairs include trip and quads
	if hand_score == 0 and len(cards + board) > 4:
		print(pairs.keys())
		print(pairs['7'])
		if pocket_pair:
			print(pairs.most_common(2)[1][1])
			if pairs[cards[0][0]]:
				print(pairs[cards[0][0]])
				print(pairs[cards[0][0]])
		else:
			print(board_pairs)
		print(board_pairs)
		print(pairs)
		hand_score, cards = 6, pair_sort(cards)
	# elif flush:
	# 	hand_score, cards = 5, flush_sort(cards)
	# elif straight:
	# 	hand_score, cards = 4, straight_sort(cards)
	# elif largest == 3:
	# 	hand_score, cards = 3, pair_sort(cards)
	# elif pairs >= 2:
	# 	# if below to solve 3 pair
	# 	hand_score, cards = 2 if pairs > 2 else pairs, pair_sort(cards)
	# 	# AJKA99 without if statement below will return HAJJ9
	# 	if pairs >= 3:
	# 		cards = cards[:4] + value_sort(cards[4:])
	# else:
	# 	hand_score, cards = 0, cards
	# print(cards)
	print(hand_score, card_vals(cards), cards)
	return hand_score, card_vals(cards), cards
