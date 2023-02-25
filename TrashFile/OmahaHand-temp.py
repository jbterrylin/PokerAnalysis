from collections import Counter
from itertools import combinations

import numpy as np

# https://stackoverflow.com/questions/54559536/efficient-algorithms-ordering-5-out-of-7-card-poker-non-straight-non-flush

value_dict = {
	'A': 0,
	'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
	'9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}


def num_of_kind(cards):
	return Counter(c[0] for c in cards)


def count_pairs(cards):
	return sum(i > 1 for i in num_of_kind(cards).values())


def largest_pair(cards):
	return max(num_of_kind(cards).values())


def is_straight(cards):
	values = [c[0] for c in cards]
	# index = "A23456789TJQKA"["K" in values:].index
	# indices = sorted(index(v) for v in values)
	indices = sorted(value_dict[v] for v in values)
	if 'A' in values:
		indices.insert(0, 0)
	indices = np.unique(indices).tolist()
	while len(indices) >= 5:
		for x, y in enumerate(enumerate(indices, indices[0])):
			print(x, y[0], y[1])
		print("-" * 10)
		print(list((y[0] == y[1] or x > 4) for x, y in enumerate(enumerate(indices, indices[0]))))
		if all((y[0] == y[1] or x > 4) for x, y in enumerate(enumerate(indices, indices[0]))):
			return True
		indices.pop(0)
	return False


# return all(x == y for x, y in enumerate(indices, indices[0]))


def is_flush(cards):
	suit_pop = Counter(c[1] for c in cards)
	return any(s > 4 for s in suit_pop.values())


def value_sort(cards):
	# values = [c[0] for c in cards]
	# index = "A23456789TJQKA"["K" in values:].index
	# print("*" * 20)
	# print(sorted(cards, key=lambda x: index(x[0]), reverse=True))
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


def score_hand(cards):
	# cards = ['Ac', '3c', '2c', '4c', '5d', 'Ad']
	# cards = ['6c', '3c', '2c', '4c', '5d', '2d']
	cards = ['2h', 'Ac', '3c', 'Th', '4h', '5c', 'Kc']
	pairs = count_pairs(cards)
	largest = largest_pair(cards)
	straight = is_straight(cards)
	flush = is_flush(cards)

	cards = value_sort(cards)
	hand_score = 0
	if flush and straight:
		cards = flush_sort(cards)
		suits = [h for h in cards if h[1] == cards[0][1]]
		if is_straight(suits):
			hand_score, cards = 8, flush_sort(cards)
	if hand_score == 0:
		if largest == 4:
			hand_score, cards = 7, pair_sort(cards)
			cards = cards[:4] + value_sort(cards[4:])
		# pairs include trip and quads
		elif pairs >= 2 and largest == 3:
			hand_score, cards = 6, pair_sort(cards)
		elif flush:
			hand_score, cards = 5, flush_sort(cards)
		elif straight:
			hand_score, cards = 4, straight_sort(cards)
		elif largest == 3:
			hand_score, cards = 3, pair_sort(cards)
		elif pairs >= 2:
			# if below to solve 3 pair
			hand_score, cards = 2 if pairs > 2 else pairs, pair_sort(cards)
			# AAJJK99 without if statement below will return AAJJ9
			if pairs >= 3:
				cards = cards[:4] + value_sort(cards[4:])
		else:
			hand_score, cards = 0, cards
	# print(cards)
	if len(cards) > 5:
		cards = cards[0:5]
	print(hand_score, card_vals(cards), cards)
	return hand_score, card_vals(cards), cards
