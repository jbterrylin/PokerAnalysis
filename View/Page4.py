import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter

import Enum
from Enum.GameTurn import GameTurn
from Enum.GameType import GameType
from Enum.Common import HERO
from Helper.Combine import extractValFromDictArr
from Helper.Convert import flatArray, expandArrayLength
from View.Component.InteractiveGraph import interactiveGraph
from View.Css import setGraphStyle

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

def graph1Helper(moves: pd.Series):
  heroMoves = []
  villianAllIn = []
  heroCallAllIn = []
  # TODO: villian all in and hero call (need to think about 3 people pool situation, hero may call first people all in and fold to third people allin)
  # for i, move in enumerate(moves):
  #   if move["player"] != HERO and "isAllIn" in move:
  #     villianAllIn.append(i)
  
  for i, move in enumerate(moves):
    if move["player"] == HERO:
      heroMoves.append(move["move"])
      if "isAllIn" in move:
        heroMoves[-1] = heroMoves[-1] + "(AllIn)"
  return "-".join(heroMoves)
    

def graph1(df: pd.DataFrame):
  st.title("Turn Reach Count")
  df["preFlop_Hero_Moves"] = [GameTurn.PREFLOP.value+"_"+graph1Helper(d) if graph1Helper(d) != "" else GameTurn.PREFLOP.value+"_END" for d in df["preFlop"]]
  df["flop_Hero_Moves"] = [GameTurn.FLOP.value+"_"+graph1Helper(d) if graph1Helper(d) != "" else GameTurn.FLOP.value+"_END" for d in df["flop"]]
  df["turn_Hero_Moves"] = [GameTurn.TURN.value+"_"+graph1Helper(d) if graph1Helper(d) != "" else GameTurn.TURN.value+"_END" for d in df["turn"]]
  df["river_Hero_Moves"] = [GameTurn.RIVER.value+"_"+graph1Helper(d) if graph1Helper(d) != "" else GameTurn.RIVER.value+"_END" for d in df["river"]]
  
  selection = pd.concat([df["preFlop_Hero_Moves"],df["flop_Hero_Moves"],df["turn_Hero_Moves"],df["river_Hero_Moves"]]).to_list()
  selection.insert(0, "DEFAULT")
  showBy = st.selectbox('Filter: ', Counter(selection))
  if showBy != "DEFAULT":
    if GameTurn.PREFLOP.value in showBy:
      df = df[df["preFlop_Hero_Moves"] == showBy]
    elif GameTurn.FLOP.value in showBy:
      df = df[df["flop_Hero_Moves"] == showBy]
    elif GameTurn.TURN.value in showBy:
      df = df[df["turn_Hero_Moves"] == showBy]
    else:
      df = df[df["river_Hero_Moves"] == showBy]

  df["count"] = [1 for d in df["river"]]
  fig = genSankey(df,cat_cols=['preFlop_Hero_Moves','flop_Hero_Moves','turn_Hero_Moves','river_Hero_Moves'],value_cols='count',title='Word Etymology')
  st.plotly_chart(fig, use_container_width=True)

def Page4(df: pd.DataFrame):
  tmp = df
  graph1(tmp)