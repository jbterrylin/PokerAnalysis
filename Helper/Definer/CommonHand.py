import numpy as np


value_dict = {
	'A': 0,
	'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
	'9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}

value_str_dict = {
	0: 'A',
	1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8',
	8: '9', 9: 'T', 10: 'J', 11: 'Q', 12: 'K', 13: 'A'}


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
