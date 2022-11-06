from flask_caching import Cache
from TrashFile.Page.App import *
import dash_bootstrap_components as dbc
from dash import dcc, html
from Css import *
app = dash.Dash(
	__name__,
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	suppress_callback_exceptions=True,
	use_pages=True,
	pages_folder=""
)

cache = Cache(app.server, config={
		'CACHE_TYPE': 'filesystem',
		'CACHE_DIR': 'cache-directory'
	})
TIMEOUT = 7200

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

