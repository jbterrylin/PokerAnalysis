import pandas as pd
import streamlit as st
import plotly.express as px
from View.Css import setGraphStyle


def graph5(df, heroMoneyChange):
	st.title("bet every turn")
	# size = df["heroCard"].str["straightDraw"],
	# symbol = df["heroCard"].str["flushDraw"],
	fig = px.scatter(
		df, x=pd.to_numeric(df['id'].str[3:]), y=heroMoneyChange,
		color=df["heroCard"].str["nPair"], title="Playing with Fonts",
		template="plotly_white")
	fig.update_layout(legend=dict(
		yanchor="top",
		y=0.99,
		xanchor="left",
		x=0.01
	))
	setGraphStyle(fig)
	st.plotly_chart(fig, use_container_width=True)


def graph6():
	# st.write(df.iloc[[0]])
	# st.plotly_chart(heroHandRank, use_container_width=True)
	st.title("bet every turn")


def Page2(df, heroMoneyChange):
	graph5(df, heroMoneyChange)
	graph6()
