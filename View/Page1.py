import numpy as np
import streamlit as st
import plotly.express as px
from statistics import mean
from streamlit_plotly_events import plotly_events

from Enum.GameTurn import GameTurn
from View.Component.InteractiveGraph import interactiveGraph
from View.Css import setGraphStyle


def graph1(df):
	st.title("heroMoneyChange each game")
	fig = px.violin(y=df["heroMoneyChange"], box=True, points='all', labels={
		"y": "heroMoneyChange"
	})
	setGraphStyle(fig)
	interactiveGraph(fig, df)


def graph2(df, heroFoldTurns):
	st.title("heroMoneyChange split by turn that game end or hero all in, fold")
	fig = px.violin(x=heroFoldTurns, y=df["heroMoneyChange"], category_orders={"x": [g.value for g in GameTurn][1:5]},
	                box=True, points='all', labels={
			"x": "gameTurn",
			"y": "heroMoneyChange"
		})
	setGraphStyle(fig)
	interactiveGraph(fig, df)


def graph3(df, heroFoldTurns):
	st.title("heroMoneyChange split by turn that game end or hero all in, fold(mean)")
	df["heroFoldTurns"] = heroFoldTurns

	data = df.groupby("heroFoldTurns").mean(numeric_only=True)
	fig = px.bar(x=data.index, y=data["heroMoneyChange"], category_orders={"x": [g.value for g in GameTurn][1:5]},
	             labels={
		             "x": "gameTurn",
		             "y": "heroMoneyChange"
	             })
	setGraphStyle(fig)
	st.plotly_chart(fig, use_container_width=True)


def graph4(df):
	st.title("heroMoneyChange by heroHoleCardScore（0-1, 6 combination)")
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
	interactiveGraph(fig, df)


def graph5(df):
	st.title("by hero hole card feature")
	cardFeature = st.selectbox('Hole card feature: ',
    ('Num of Pair', 'Num of flush draw', 'Num of straight draw', 'Num of open end straight draw'))
	showBy = st.selectbox('Feature show by: ', ('color', 'shape', 'size'))

	feature = None
	match cardFeature:
		case 'Num of Pair':
			feature = "nPair"
		case 'Num of flush draw':
			feature = "flushDraw"
		case 'Num of straight draw':
			feature = "straightDraw"
		case _:
			feature = "openEndDraw"
	match showBy:
		case 'color':
			fig = px.scatter(
				df, x=df.index, y=df["heroMoneyChange"],
				color=df["heroCard"].str[feature])
		case 'shape':
			fig = px.scatter(
				df, x=df.index, y=df["heroMoneyChange"],
				symbol=df["heroCard"].str[feature],
				category_orders={"symbol": [0, 1, 2, 3, 4, 5, 6]})
		case _:
			fig = px.scatter(
				df, x=df.index, y=df["heroMoneyChange"],
				size=df["heroCard"].str[feature])
	fig.update_layout(legend=dict(
		yanchor="top",
		y=0.99,
		xanchor="left",
		x=0.01
	))
	setGraphStyle(fig)
	interactiveGraph(fig, df)


def Page1(df, heroFoldTurns):
	graph1(df)
	graph2(df, heroFoldTurns)
	graph3(df, heroFoldTurns)
	graph4(df)
	graph5(df)
