from collections import Counter
from itertools import combinations
from Helper.Definer.CommonHand import *


class HeroCard:
	cards = []
	straightDraw = 0
	flushDraw = 0
	nPair = 0
	score = []

	def __init__(self, cards):
		self.score = []

		self.cards = cards
		self.nPair = check_pocket_pair(cards)

		comb = combinations(cards, 2)
		for i in list(comb):
			if check_cards_can_straight(i):
				self.straightDraw += 1
			if check_cards_can_flush(i):
				self.flushDraw += 1
