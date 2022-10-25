from Enum.GameType import GameType
from lib import *
import Enum

folderName = "Resource"
gameType = GameType.PLO_PL

import sys
print("Python version: " + sys.version)
print("Python version should above 3.10")

with open(folderName+"/GG20221017-1004 - RushAndCash1425563 - 0.01 - 0.02 - 6max.txt") as f:
  singleGame = []
  for line in f:
    if line.strip() == "":
      t.singleGame(singleGame)
      singleGame = []
      break
    else:
      singleGame.append(line.strip())
    # print(line.strip())
    

print("tup1,tup2")
