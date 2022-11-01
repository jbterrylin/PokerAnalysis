import os
import sys

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import Transformer.transformer as t
from Css import *
from Enum.GameType import GameType
from Helper.Definer.GameResult import setGameResult

folderName = "Resource"
gameType = GameType.OMAHA_PL

print("Python version: " + sys.version)
print("Python version should above 3.10")

games = []


def fileToGames(fpath):
	print(fpath)
	with open(fpath) as f:
		singleGame = []
		for line in f:
			if line.strip() == "" and len(singleGame) > 0:
				game = t.singleGame(singleGame)
				game.filePath = fpath
				game = setGameResult(game)
				games.append(game)
				singleGame = []
				# break
			elif line.strip() != "":
				singleGame.append(line.strip())


def init():
	for filename in os.listdir(folderName):
		fpath = os.path.join(folderName, filename)
		if os.path.isfile(fpath):
			fileToGames(fpath)


# a = [x for x in games if len(x.showDown) > 1]
# for aa in a:
#   if len(aa.showDown[0]) > 1 or len(aa.showDown[1]) > 1:
#     print(aa.Id)


init()

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
		return html.Div([html.P("This is the content of the home page!123435")])
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


if __name__ == "__main__":
	app.run_server(port=8888, debug=True)
