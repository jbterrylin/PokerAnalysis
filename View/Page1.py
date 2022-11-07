import numpy as np
import streamlit as st
import plotly.express as px
from statistics import mean
from streamlit_plotly_events import plotly_events

from Enum.GameTurn import GameTurn
from View.Css import setGraphStyle


def graph1(df):
	st.title("heroMoneyChange each game")
	fig = px.violin(y=df["heroMoneyChange"], box=True, points='all', labels={
		"y": "heroMoneyChange"
	})
	setGraphStyle(fig)
	st.plotly_chart(fig, use_container_width=True)


def graph2(df, heroFoldTurns):
	st.title("heroMoneyChange split by turn that game end or hero all in, fold")
	fig = px.violin(x=heroFoldTurns, y=df["heroMoneyChange"], category_orders={"x": [g.value for g in GameTurn][1:5]},
    box=True, points='all', labels={
			"x": "gameTurn",
			"y": "heroMoneyChange"
	})
	setGraphStyle(fig)
	st.plotly_chart(fig, use_container_width=True)


def graph3(df, heroFoldTurns):
	st.title("heroMoneyChange split by turn that game end or hero all in, fold(mean)")
	df["heroFoldTurns"] = heroFoldTurns

	data = df.groupby("heroFoldTurns").mean(numeric_only=True)
	fig = px.bar(x=data.index, y=data["heroMoneyChange"], category_orders={"x": [g.value for g in GameTurn][1:5]}, labels={
		"x": "gameTurn",
		"y": "heroMoneyChange"
	})
	setGraphStyle(fig)
	st.plotly_chart(fig, use_container_width=True)


def graph4(df):
	st.title("heroMoneyChange by heroHoleCardScore（0-1, 6 combi)")
	heroCardScoreBy = st.selectbox('heroHoleCardScore by: ', ('Max', 'Min', 'Mean'))
	if heroCardScoreBy == 'Max':
		heroCardScore = [max(hc["score"]) for hc in df["heroCard"]]
	elif heroCardScoreBy == 'Min':
		heroCardScore = [min(hc["score"]) for hc in df["heroCard"]]
	else:
		heroCardScore = [mean(hc["score"]) for hc in df["heroCard"]]
	fig = px.scatter(df, x=df["heroMoneyChange"], y=heroCardScore, labels={
		"x": "heroMoneyChange",
		"y": "heroHoleCardScore (" + heroCardScoreBy + ")"
	})
	fig.update_traces(text=np.array(df['id']),
	                  hovertemplate='id: %{text} <br>heroMoneyChange: %{x} <br>heroHoleCardScore: %{y}')
	fig = setGraphStyle(fig)
	selected_points = plotly_events(fig, click_event=True)
	if len(selected_points) != 0:
		print(selected_points[0]["pointIndex"])


def Page1(df, heroFoldTurns):
	graph1(df)
	graph2(df, heroFoldTurns)
	graph3(df, heroFoldTurns)
	graph4(df)
