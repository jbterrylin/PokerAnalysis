import pandas as pd
import streamlit as st
import plotly.express as px

from Enum.GameTurn import GameTurn
from View.Component.InteractiveGraph import interactiveGraph
from View.Css import setGraphStyle


def graph1():
	# st.write(df.iloc[[0]])
	# st.plotly_chart(heroHandRank, use_container_width=True)
	st.title("bet every turn")


def graph2():
	st.title("bet every turn")


def Page2(df):
	graph1()
	graph2()
