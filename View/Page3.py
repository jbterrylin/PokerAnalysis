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

def graph1Helper(df: pd.DataFrame):
  if df["flop"] == []:
    return GameTurn.PREFLOP.value
  elif df["turn"] == []:
    return GameTurn.FLOP.value
  elif df["river"] == []:
    return GameTurn.TURN.value
  else:
    return GameTurn.RIVER.value

def graph1(df: pd.DataFrame):
  st.title("Turn Reach Count")
  df["final_move_turn"] = [graph1Helper(d) for _, d in df[["flop","turn","river"]].iterrows()]
  finalMoveTurn = df["final_move_turn"].value_counts()
  finalMoveTurn.sort_index()
  print(finalMoveTurn)
  print(finalMoveTurn.loc[GameTurn.FLOP.value])
  data = dict(
    number=[
      finalMoveTurn[GameTurn.PREFLOP.value],
      finalMoveTurn[GameTurn.FLOP.value],
      finalMoveTurn[GameTurn.TURN.value],
      finalMoveTurn[GameTurn.RIVER.value]],
    stage=[GameTurn.PREFLOP.value,GameTurn.FLOP.value,GameTurn.TURN.value,GameTurn.RIVER.value])
  fig = px.funnel(data, x='number', y='stage')
  st.plotly_chart(fig)

def Page3(df: pd.DataFrame):
	graph1(df)