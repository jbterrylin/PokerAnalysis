import pandas as pd
import streamlit as st

from Enum.GameTurn import GameTurn
from Helper.Convert import fakeIntToBB
from Model.Move import MoveRef, Move
from View.Page1 import Page1
from View.Page2 import Page2
from View.Page3 import Page3
from View.Page4 import Page4


def setScreen():
	selectedPage = st.sidebar.selectbox('Page', ('Money', 'Card', 'Turn', 'Move'))
	if 'selectedDataIndex' not in st.session_state:
		st.session_state.selectedDataIndex = None

	if 'isMoneyUnit' not in st.session_state:
		st.session_state.isMoneyUnit = 1
	if st.sidebar.radio("Money Unit:", ("Money", "Big Blind"), horizontal=True) == "Money":
		st.session_state.isMoneyUnit = 1
	else:
		st.session_state.isMoneyUnit = 0

	if 'removePlain' not in st.session_state:
		st.session_state.removePlain = 1
	if st.sidebar.radio("Remove Plain:", ("True", "False"), horizontal=True, help="remove heroMoneyChange is > -1bb and "
																																								"< 1bb") == "True":
		st.session_state.removePlain = 1
	else:
		st.session_state.removePlain = 0

	if 'games' in st.session_state:
		df = pd.DataFrame([o.toDict() for o in st.session_state.games])
		# for _, row in df.iterrows():
		# 	if row["id"] == "#RC211503132":
		# 		print(row["heroCard"]["straightDraw"])
		# 		print(row["heroCard"]["openEndDraw"])

		if st.session_state.removePlain:
			bbs = df["blind"].str[MoveRef.BIG_BLIND.value]
			df = df.loc[((df["heroMoneyChange"] > bbs) | (df["heroMoneyChange"] < -bbs))]

		if not st.session_state.isMoneyUnit:
			df["heroMoneyChange"] = fakeIntToBB(df["heroMoneyChange"], df["blind"].str[MoveRef.BIG_BLIND.value])

		heroFoldTurns = []
		for _, row in df.iterrows():
			moves = sorted(row["sumMoves"], key=lambda x: x["id"])
			heroFoldTurns.append(next((m["turn"] for m in moves if
																 (m["player"] == "Hero" and (m["move"] == Move.FOLD.value or m.get("isAllIn", False)))),
																GameTurn.SHOWDOWN.value))
		if selectedPage == "Money":
			Page1(df, heroFoldTurns)
		elif selectedPage == "Card":
			Page2(df)
		elif selectedPage == "Turn":
			# get final turn each game with funnel chart
			# Page2(df, heroFoldTurns)
			Page3(df)
		elif selectedPage == "Move":
			# get final turn each game with funnel chart
			# Page2(df, heroFoldTurns)
			Page4(df)
		elif selectedPage == "Single Game":
			# get final turn each game with funnel chart
			# Page2(df, heroFoldTurns)
			print("a")