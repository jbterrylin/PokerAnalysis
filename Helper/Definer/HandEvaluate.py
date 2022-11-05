import itertools

from treys.card import Card
from treys.evaluator import PLOEvaluator
from pokereval.card import Card as HoleCard
from pokereval.hand_evaluator import HandEvaluator

from Helper.Definer.CommonHand import suit_dict, value_dict


def check_hand(holeCard, board):
	if len(board) != 0:
		board = [Card.new(c) for c in board]
		hand = [Card.new(c) for c in holeCard]

		evaluator = PLOEvaluator()

		# and rank your hand
		rank = evaluator.evaluate(hand, board)
		class_ = evaluator.get_rank_class(rank)

		return rank, evaluator.class_to_string(class_), evaluator


# https://github.com/aliang/pokerhand-eval
def check_hole_card(holeCard):
	score = []
	for hand_combo in itertools.combinations(holeCard, 2):
		hole = [HoleCard(value_dict[hand_combo[0][0]] + 1, suit_dict[hand_combo[0][1]]),
		        HoleCard(value_dict[hand_combo[1][0]] + 1, suit_dict[hand_combo[1][1]])]
		score.append(HandEvaluator.evaluate_hand(hole, []))

	return score
