import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

import Enum
from Enum.GameTurn import GameTurn
from Enum.GameType import GameType
from Helper.Combine import extractValFromDictArr
from Helper.Convert import flatArray, expandArrayLength
from View.Component.InteractiveGraph import interactiveGraph
from View.Css import setGraphStyle


# multi stack bar chart
# multi = move
# stack bar = hand type
# x = game turn
# y = total hand

def graph1(df: pd.DataFrame):
	st.title("heroHand every gameTurn")
	df["heroHands_FLOP_Hands"] = df["heroHands_Hands"].str[0]
	df["heroHands_TURN_Hands"] = df["heroHands_Hands"].str[1]
	df["heroHands_RIVER_Hands"] = df["heroHands_Hands"].str[2]
	tmp = df[["heroHands_FLOP_Hands", "heroHands_TURN_Hands", "heroHands_RIVER_Hands"]].value_counts(dropna=False)

	indexDf = tmp.index.to_frame(index=False, name=[g.value for g in GameTurn][2:5])
	indexDf["container"] = ['Main' for _ in range(tmp.shape[0])]
	indexDf["value"] = tmp.values
	indexDf = indexDf.fillna("End")

	fig = px.treemap(indexDf, path=["container"] + [g.value for g in GameTurn][2:5], values='value',
	                 color_continuous_scale='RdBu', branchvalues='total')
	st.plotly_chart(fig)


def graph2Helper(df: pd.DataFrame, gameTurn: Enum.GameTurn):
	flopCount = df[["heroHands_" + gameTurn.value + "_Hands"]].value_counts(dropna=False)

	data = {
		'gameTurn': [gameTurn.value for _ in range(len(flopCount.values))],
		'hands': flopCount.index.get_level_values(0).to_list(),
		'hand_count': flopCount.values
	}

	return pd.DataFrame(data)


def graph2(df: pd.DataFrame):
	st.title("heroHand every gameTurn")
	df["heroHands_FLOP_Hands"] = df["heroHands_Hands"].str[0]
	df["heroHands_TURN_Hands"] = df["heroHands_Hands"].str[1]
	df["heroHands_RIVER_Hands"] = df["heroHands_Hands"].str[2]

	result = pd.concat(
		[graph2Helper(df, GameTurn.FLOP), graph2Helper(df, GameTurn.TURN), graph2Helper(df, GameTurn.RIVER)])
	result = result.fillna("End")

	fig = px.histogram(result, x="gameTurn", y="hand_count",
	                   color='hands', barmode='group')
	st.plotly_chart(fig, use_container_width=True)

def graph3():
	# fig = px.line(
	# 	df, x=df.index, y=df["heroMoneyChange"],
	# 	color=df["heroCard"].str[feature])
	st.title("bet every turn")


# only get first board
def heroHands_TurnHelper(row):
	result = [extractValFromDictArr(r, "hand") for r in row["heroHand"]]
	if len(result) > 0:
		return result[0]
	return []


def Page2(df):
	# for a in df["heroHand"]:
	# 	for b in a:
	# 		print(b)
	df["heroHands_Hands"] = [heroHands_TurnHelper(d) for _, d in df[["heroHand"]].iterrows()]

	graph1(df)
	graph2(df)
