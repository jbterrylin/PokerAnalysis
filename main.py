import os
from datetime import datetime
from multiprocessing import *

import pandas as pd
import streamlit as st

import Transformer.transformer as t
from Enum.GameType import GameType
from Helper.Definer.HeroHandAndCard import setHeroHandNCard
from Helper.MoneyRelated import playerBetEachTurn
from Helper.HeroMoneyChange import heroMoneyChange
from App import setScreen

if __name__ == '__main__':
	folderName = "Resource"
	gameType = GameType.OMAHA_PL

# print("Python version: " + sys.version)
# print("Python version should above 3.10")

def fileToGames(fpath):
	print(fpath)
	games = []
	with open(fpath) as f:
		singleGame = []
		for line in f:
			if line.strip() == "" and len(singleGame) > 0:
				game = t.singleGame(singleGame)
				game.filePath = fpath
				game = setHeroHandNCard(game)
				game = playerBetEachTurn(game)
				game = heroMoneyChange(game)
				game.joinMovesWithoutInit()
				games.append(game)
				singleGame = []
			# break
			elif line.strip() != "":
				singleGame.append(line.strip())
		return games


@st.cache(persist=True, allow_output_mutation=True)
def init():
	if __name__ == '__main__':
		games = []

		gameAsyncs = []
		pool = Pool(12)

		start_time = datetime.now()
		# threads = []
		for filename in os.listdir(folderName):
			fpath = os.path.join(folderName, filename)
			if os.path.isfile(fpath):
				gameAsyncs.append(pool.apply_async(fileToGames, args=[fpath]))
			# games += fileToGames(fpath)
		pool.close()
		pool.join()
		print("time:", datetime.now() - start_time)
		print("所有进程执行完毕")
		for gameAsync in gameAsyncs:
			games += gameAsync.get()
		# export games
		df = pd.DataFrame([o.__dict__ for o in games])
		df.to_csv("data.csv")
		df = pd.DataFrame([o.toDict() for o in games])
		df.to_csv("data1.csv")
		return games


if __name__ == '__main__':
	if 'games' not in st.session_state:
		st.session_state.games = init()
	setScreen()
