from enum import Enum


class GameType(Enum):
	OMAHA_PL = "Omaha Pot Limit"
	TEXAS = "Texas"

	def getNBoardCardEachTurn(self):
		match self:
			case self.OMAHA_PL | self.TEXAS:
				return [0, 3, 1, 1]
