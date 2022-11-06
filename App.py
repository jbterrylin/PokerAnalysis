import pandas as pd
import streamlit as st
import plotly.express as px

from Helper.Convert import fakeIntToBB
from Model.Move import MoveRef


def setScreen():
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

		if st.session_state.removePlain:
			bbs = df["blind"].str[MoveRef.BIG_BLIND.value]
			df = df.loc[((df["heroMoneyChange"] > bbs) | (df["heroMoneyChange"] < -bbs))]

		heroMoneyChanges = df["heroMoneyChange"]
		if not st.session_state.isMoneyUnit:
			heroMoneyChanges = fakeIntToBB(heroMoneyChanges, df["blind"].str[MoveRef.BIG_BLIND.value])
		heroMoneyChangeViolin = px.violin(y=heroMoneyChanges, box=True, points='all', labels={
			"y": "heroMoneyChanges"
		})
		st.title("heroMoneyChange each game")
		st.plotly_chart(heroMoneyChangeViolin, use_container_width=True)

		st.title("heroMoneyChange / heroHoleCardScore (Max)")
		heroCardScore = [max(hc["score"]) for hc in df["heroCard"]]
		heroHandRank = px.scatter(x=heroMoneyChanges, y=heroCardScore, labels={
			"x": "heroMoneyChanges",
			"y": "heroHoleCardScore (Max)"
		})
		st.plotly_chart(heroHandRank, use_container_width=True)
