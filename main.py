import os
from datetime import datetime
from multiprocessing import *

import pandas as pd
import numpy as np
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

def singleRowToDistribute(df: pd.DataFrame):
	seatDf = pd.DataFrame.from_dict(df["seat"].to_list())
	seatDf["id"] = df.index.values.tolist()
	seatDf = seatDf.melt(id_vars=["id"], 
        var_name="seat", 
        value_name="value")
	seatDf.to_csv("result/seat.csv")
 
	def split2dArray(colName: str):
		multiDf = pd.DataFrame.from_dict(df[colName])
		multiDf["first"] = [multi[0] if len(multi) > 0 else [] for multi in multiDf[colName]]
		multiDf["second"] = [multi[1] if len(multi) > 1 else [] for multi in multiDf[colName]]
		multiDf["third"] = [multi[2] if len(multi) > 2 else [] for multi in multiDf[colName]]
		multiDf = multiDf.drop([colName], axis=1)
		return multiDf
 
	def meltMultiCol(col: tuple,ids: any):
		moveDf = pd.DataFrame.from_dict(col.to_list())
		moveDf["id"] = ids
		moveDf = moveDf.melt(id_vars=["id"], 
					var_name="order",
					value_name="value")
		return moveDf
  
	meltMultiCol(df["init"],df.index.values.tolist()).to_csv("result/init.csv")
	meltMultiCol(df["preFlop"],df.index.values.tolist()).to_csv("result/preFlop.csv")
	meltMultiCol(df["flop"],df.index.values.tolist()).to_csv("result/flop.csv")
	meltMultiCol(df["turn"],df.index.values.tolist()).to_csv("result/turn.csv")
	meltMultiCol(df["river"],df.index.values.tolist()).to_csv("result/river.csv")
	meltMultiCol(df["sumMoves"],df.index.values.tolist()).to_csv("result/sumMoves.csv")
 
	split2dArray("board").to_csv("result/board.csv")
	showDownDf = split2dArray("showDown")
	showDownDf = meltMultiCol(showDownDf["first"],df.index.values.tolist())
	showDownDf.to_csv("result/showDown.csv")
 
	heroHandDf = split2dArray("heroHand")
	heroHandDf = meltMultiCol(heroHandDf["first"],df.index.values.tolist())
	heroHandDf.to_csv("result/heroHand.csv")

	betsDf = pd.DataFrame.from_dict(df["bets"].to_list())
	betsDf["id"] = df.index.values.tolist()
	betsDf = betsDf.melt(id_vars=["id"], 
				var_name="gameTurn",
				value_name="value")
	betsDf = betsDf.where(betsDf.notna(), lambda x: [{}])
	betsDf = pd.concat([betsDf, pd.DataFrame.from_dict(betsDf["value"].to_list())], axis=1)
	betsDf = betsDf.drop(["value"], axis=1)
	betsDf = betsDf.melt(id_vars=["id", "gameTurn"], 
				var_name="player",
				value_name="value")
	betsDf.dropna(inplace=True)
	betsDf.to_csv("result/bets.csv")
 
	pd.DataFrame.from_dict(df["blind"].to_list()).to_csv("result/blind.csv")
	
	sumBetsDf = meltMultiCol(df["sumBets"],df.index.values.tolist())
	sumBetsDf.dropna(inplace=True)
	sumBetsDf.to_csv("result/sumBets.csv")

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
		df["id"] = df.index.values.tolist()
		df.to_csv("result/single_row.csv")
		singleRowToDistribute(df)
		return games


if __name__ == '__main__':
	# if 'games' not in st.session_state:
	st.session_state.games = init()
	setScreen()
