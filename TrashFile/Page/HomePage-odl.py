# import dash_bootstrap_components as dbc
# import pandas as pd
# from dash import Input, Output, dcc, html
# import plotly.express as px
# from dash.exceptions import PreventUpdate
#
# from Css import *
# from .App import *
# from View.Page.Page1 import Page1
# import dash.dependencies as dd
#
# # import seaborn as sns
# # sns.set_theme(style="white")
#
# @app.callback(
# 		dd.Output("standalone-radio-check-output", "children"),
# 		dd.Input("standalone-switch", "value"),
# 	)
# def on_form_change(switch_checked):
# 	print("on_form_change")
# 	return f"Toggle Switch: {switch_checked}"
#
# def setScreen(games):
#
#
# 	sidebar = html.Div(
# 		[
# 			html.P(id='placeholder'),
# 			html.H2("Sidebar", className="display-4"),
# 			html.Hr(),
# 			html.P(
# 				"A simple sidebar layout with navigation links", className="lead"
# 			),
# 			dbc.Nav(
# 				[
# 					dbc.NavLink("Home", href="/", active="exact"),
# 					dbc.NavLink("Page 1", href="/page-1", active="exact"),
# 					dbc.NavLink("Page 2", href="/page-2", active="exact"),
# 					dbc.Button(
# 						'clear cache',
# 						id='clear-cache',
# 						className="me-2",
# 						n_clicks=0
# 					)
# 				],
# 				vertical=True,
# 				pills=True,
# 			),
# 		],
# 		style=SIDEBAR_STYLE,
# 	)
#
# 	content = html.Div(id="page-content", style=CONTENT_STYLE)
#
# 	app.layout = html.Div([
# 		dcc.Store(id='memory'),
# 		dcc.Location(id="url"),
# 		sidebar,
# 		html.Div(dash.page_container, style=CONTENT_STYLE)
# 	])
#
# 	# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# 	# def render_page_content(pathname):
# 	# 	print("render_page_content")
# 	# 	if pathname == "/":
# 	# 		return Page1(games)
# 	# 	elif pathname == "/page-1":
# 	# 		return html.P("This is the content of page 1. Yay!")
# 	# 	elif pathname == "/page-2":
# 	# 		return html.P("Oh cool, this is page 2!")
# 	# 	# If the user tries to reach a different page, return a 404 message
# 	# 	return html.Div(
# 	# 		[
# 	# 			html.H1("404: Not found", className="text-danger"),
# 	# 			html.Hr(),
# 	# 			html.P(f"The pathname {pathname} was not recognised..."),
# 	# 		],
# 	# 		className="p-3 bg-light rounded-3",
# 	# 	)
#
# 	@app.callback(
# 		Output("placeholder", "children"), [Input("clear-cache", "n_clicks")]
# 	)
# 	def clearCache(n):
# 		if n is None or n == 0:
# 			# prevent the None callbacks is important with the store component.
# 			# you don't want to update the store for nothing.
# 			raise PreventUpdate
# 		else:
# 			print("clearCache")
# 			cache.clear()
#
# 	if __name__ == "View.HomePage":
# 		app.run_server(port=8888, debug=True)
