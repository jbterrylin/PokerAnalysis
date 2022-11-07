import pandas as pd
import streamlit as st
import plotly.express as px

from Enum.GameTurn import GameTurn
from View.Component.InteractiveGraph import interactiveGraph
from View.Css import setGraphStyle


def graph5(df):
	st.title("bet every turn")
	# size = df["heroCard"].str["straightDraw"],
	# symbol = df["heroCard"].str["flushDraw"],
	# pd.to_numeric(df['id'].str[3:])
	fig = px.scatter(
		df, x=df.index, y=df["heroMoneyChange"],
		color=df["heroCard"].str["nPair"], title="Playing with Fonts")
	fig.update_layout(legend=dict(
		yanchor="top",
		y=0.99,
		xanchor="left",
		x=0.01
	))
	setGraphStyle(fig)
	interactiveGraph(fig, df)


def graph6():
	# st.write(df.iloc[[0]])
	# st.plotly_chart(heroHandRank, use_container_width=True)
	st.title("bet every turn")


def Page2(df):
	graph5(df)
	graph6()
