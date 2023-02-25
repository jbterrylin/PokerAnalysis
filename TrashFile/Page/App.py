from dash import dash
from TrashFile.Page.Cache import cache

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PreventUpdate

from TrashFile.Css import *


def startServer(app):
	sidebar = html.Div(
		[
			html.P(id='placeholder'),
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
					dbc.Button(
						'clear cache',
						id='clear-cache',
						className="me-2",
						n_clicks=0
					)
				],
				vertical=True,
				pills=True,
			),
		],
		style=SIDEBAR_STYLE,
	)

	app.layout = html.Div([
		dcc.Store(id='memory'),
		dcc.Location(id="url"),
		sidebar,
		html.Div(dash.page_container, style=CONTENT_STYLE)
	])


@callback(
	Output("placeholder", "children"), [Input("clear-cache", "n_clicks")]
)
def clearCache(n):
	if n is None or n == 0:
		# prevent the None callbacks is important with the store component.
		# you don't want to update the store for nothing.
		raise PreventUpdate
	else:
		print("clearCache")
		cache.clear()
