import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
import seaborn as sns

from Css import *
from Enum.Common import WIN

sns.set_theme(style="white")


def setScreen(games):
	df = pd.DataFrame([o.toDict() for o in games])
	df.to_csv("data.csv")
	print(df)
	app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


	sidebar = html.Div(
		[
			html.H2("Sidebar", className="display-4"),
			html.Hr(),
			html.P(
				"A simple sidebar layout with navigation links", className="lead"
			),
			dbc.Nav(
				[
					dbc.NavLink("Home", href="/", active="exact"),
					dbc.NavLink("Page 1", href="/page-1", active="exact"),
					dbc.NavLink("Page 2", href="/page-2", active="exact"),
				],
				vertical=True,
				pills=True,
			),
		],
		style=SIDEBAR_STYLE,
	)

	content = html.Div(id="page-content", style=CONTENT_STYLE)

	app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

	@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
	def render_page_content(pathname):
		if pathname == "/":
			return html.Div([html.P("This is the content of the home page!")])
		elif pathname == "/page-1":
			return html.P("This is the content of page 1. Yay!")
		elif pathname == "/page-2":
			return html.P("Oh cool, this is page 2!")
		# If the user tries to reach a different page, return a 404 message
		return html.Div(
			[
				html.H1("404: Not found", className="text-danger"),
				html.Hr(),
				html.P(f"The pathname {pathname} was not recognised..."),
			],
			className="p-3 bg-light rounded-3",
		)

	if __name__ == "View.HomePage":
		app.run_server(port=8888)
