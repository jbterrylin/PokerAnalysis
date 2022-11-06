from dash import dcc, html
from dash.dependencies import Output, Input, State

from dash.exceptions import PreventUpdate

# import seaborn as sns

from TrashFile.Css import *
from TrashFile.Component.Grid import toGrid


def compareInput(df, key):
	return html.Div([
		toGrid([
			dcc.Dropdown(
				df.columns,
				df.columns[0],
				id='input-variable-' + str(key),
			),
			dcc.Dropdown(
				["==", "!=", ">", ">=", "<", "<="],
				df.columns[0],
				id='input-compare-' + str(key),
			),
			dcc.Input(
				id="input-target-" + str(key),
				type="text",
				placeholder="",
				style=INPUT_LIKE_DD_STYLE
			),
			html.Div([
				html.Button(
					'+',
					id='add-button-' + str(key),
					style=addReplaceStyle(BUTTON_STYLE, {"width": "36px", "margin-right": "16px"})
				),
				html.Button(
					'-',
					id='delete-button-' + str(key),
					style=addReplaceStyle(BUTTON_STYLE, {"width": "36px"})
				)
			], style={'textAlign': 'center'})
		], widths=[3, 2, 5, 2])
		# dbc.RadioItems(
		# 	['Linear', 'Log'],
		# 	'Linear',
		# 	id='xaxis-type',
		# 	inline=True
		# )
	], style={'width': '33%', 'display': 'inline'})


def dynamicInput(app, cache, df):
	compareInputkeys = [0]
	if cache.get('compareInputkeys') is None:
		cache.set('compareInputkeys', compareInputkeys)
	else:
		compareInputkeys = cache.get('compareInputkeys')

	@app.callback(Output('memory', 'data'),
	    Input('add-button-'.format('memory'), 'n_clicks'),
	    State('memory', 'data'))
	def on_click(n_clicks, data):
		if n_clicks is None:
			# prevent the None callbacks is important with the store component.
			# you don't want to update the store for nothing.
			raise PreventUpdate

		# Give a default data dict with 0 clicks if there's no data.
		cache.set('compareInputkeys', cache.get('compareInputkeys') + [max(cache.get('compareInputkeys')) + 1])
		data = data or {'clicks': 0}

		data['clicks'] = data['clicks'] + 1
		return data

	def dynamicInputHelper(key):
		return compareInput(df, key)

	result = []
	for k in compareInputkeys:
		result.append(dynamicInputHelper(k))
	return result
