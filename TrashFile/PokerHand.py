import itertools

value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
value_dict.update((str(x), x) for x in range(2, 10))


def eval_hand(hand):
	# Return ranking followed by tie-break information.
	# 8. Straight Flush
	# 7. Four of a Kind
	# 6. Full House
	# 5. Flush
	# 4. Straight
	# 3. Three of a Kind
	# 2. Two pair
	# 1. One pair
	# 0. High card

	values = sorted([c[0] for c in hand], reverse=True)
	suits = [c[1] for c in hand]
	straight = (values == list(range(values[0], values[0] - 5, -1))
	            or values == [14, 5, 4, 3, 2])
	flush = all(s == suits[0] for s in suits)

	if straight and flush: return 8, values[1]
	if flush: return 5, values
	if straight: return 4, values[1]

	trips = []
	pairs = []
	for v, group in itertools.groupby(values):
		count = sum(1 for _ in group)
		if count == 4:
			return 7, v, values
		elif count == 3:
			trips.append(v)
		elif count == 2:
			pairs.append(v)

	if trips: return (6 if pairs else 3), trips, pairs, values
	return len(pairs), pairs, values
