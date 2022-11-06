import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from statistics import mean
from streamlit_plotly_events import plotly_events

from Helper.Convert import fakeIntToBB
from Model.Move import MoveRef


def setGraphStyle(fig):
	return fig.update_layout(paper_bgcolor="rgb(14, 17, 23)", plot_bgcolor="rgb(39, 39, 49)", font_color="white")


def graph1(heroMoneyChanges):
	heroMoneyChangeViolin = px.violin(y=heroMoneyChanges, box=True, points='all', labels={
		"y": "heroMoneyChanges"
	})
	st.title("heroMoneyChange each game")
	st.plotly_chart(heroMoneyChangeViolin, use_container_width=True)


def graph2(df, heroMoneyChanges):
	st.title("heroMoneyChange / heroHoleCardScore (Max)")
	heroCardScoreBy = st.selectbox('heroHoleCardScore by: ', ('Max', 'Min', 'Mean'))
	if heroCardScoreBy == 'Max':
		heroCardScore = [max(hc["score"]) for hc in df["heroCard"]]
	elif heroCardScoreBy == 'Min':
		heroCardScore = [min(hc["score"]) for hc in df["heroCard"]]
	else:
		heroCardScore = [mean(hc["score"]) for hc in df["heroCard"]]
	heroHandRank = px.scatter(df, x=heroMoneyChanges, y=heroCardScore, labels={
		"x": "heroMoneyChanges",
		"y": "heroHoleCardScore (" + heroCardScoreBy + ")"
	})
	heroHandRank.update_traces(text=np.array(df['id']),
	                           hovertemplate='id: %{text} <br>heroMoneyChanges: %{x} <br>heroHoleCardScore: %{y}')
	heroHandRank = setGraphStyle(heroHandRank)
	selected_points = plotly_events(heroHandRank, click_event=True)
	if len(selected_points) != 0:
		print(selected_points[0]["pointIndex"])


# st.write(df.iloc[[0]])
# st.plotly_chart(heroHandRank, use_container_width=True)


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
		graph1(heroMoneyChanges)

		graph2(df, heroMoneyChanges)
