from treys.card import Card
from treys.evaluator import PLOEvaluator


def check_hand(holeCard, board):
	if len(board) != 0:
		board = [Card.new(c) for c in board]
	hand = [Card.new(c) for c in holeCard]

	evaluator = PLOEvaluator()

	# and rank your hand
	rank = evaluator.evaluate(hand, board)
	class_ = evaluator.get_rank_class(rank)

	return rank, evaluator.class_to_string(class_), evaluator
