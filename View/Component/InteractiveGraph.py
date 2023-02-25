import streamlit as st
from streamlit_plotly_events import plotly_events

from Helper.Delete import delValInDictsByKey


def interactiveGraph(fig, df, click_event=True):
	# concern:
	# may come out error if fig's data is filter in graph function,
	# because when filtered in graph function length and index may be not same with ori df
	selected_points = plotly_events(fig, click_event=click_event)
	if len(selected_points) != 0:
		index = selected_points[0]["pointIndex"]
		st.session_state.selectedDataIndex = index
		# need to move evaluator before show entire df row
		# tmp = df.iloc[[index]].copy()
		# tmp["heroHand"] = delValInDictsByKey(tmp["heroHand"], "evaluator")
		st.write(df.iloc[[index]]["id"])
