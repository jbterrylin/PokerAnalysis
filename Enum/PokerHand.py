from enum import Enum


class PokerHand(Enum):
	ROYAL_FLUSH = "Royal Flush"
	STRAIGHT_FLUSH = "Straight Flush"
	FOUR_OF_THE_KIND = "Four of a Kind"
	FULL_HOUSE = "Full House"
	FLUSH = "Flush"
	STRAIGHT = "Straight"
	THREE_OF_THE_KIND = "Three of a Kind"
	TWO_PAIR = "Two Pair"
	ONE_PAIR = "Pair"
	HIGH_CARD = "High Card"
