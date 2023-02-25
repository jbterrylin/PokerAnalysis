import dash_bootstrap_components as dbc
from dash import html
from TrashFile.Page.Cache import cache

import dash
print("aaaaa")
dash.register_page(__name__)

print("aaaaa")
# def Page1(games):
# 	df = pd.DataFrame([o.toDict() for o in games])
# 	removePlainDf = df.loc[((df["heroMoneyChange"] > 2) | (df["heroMoneyChange"] < -2))]

# @app.callback(
# 	dd.Output("standalone-radio-check-output", "children"),
# 	dd.Input("standalone-switch", "value"),
# )
# def on_form_change(switch_checked):
# 	print("on_form_change")
# 	return f"Toggle Switch: {switch_checked}"

# def graph1():
# 	heroMoneyChangeViolin = px.violin(removePlainDf, y="heroMoneyChange", box=True, points='all')
# 	return dcc.Graph(
# 		figure=heroMoneyChangeViolin,
# 		id="heroMoneyChangeViolin"
# 	)
#
# def graph2():
# 	heroCardScore = [max(hc["score"]) for hc in removePlainDf["heroCard"]]
# 	heroHandRank = px.scatter(x=removePlainDf["heroMoneyChange"], y=heroCardScore)
# 	return dcc.Graph(
# 		figure=heroHandRank,
# 		id="heroHandRank"
# 	)
def layout():
	print("aaaaa")
	print(cache.get("games"))
	return [
		# dbc.Switch(
		# 	id="money-unit-select",
		# 	label="Money",
		# 	value=True,
		# ),
		html.P(id='placeholder-p1'),
		dbc.Switch(
			id="standalone-switch",
			label="This is a toggle switch",
			value=False,
		),
		html.P("@!312312", id="standalone-radio-check-output"),
		html.P("((df[\"heroMoneyChange\"] > 2) | (df[\"heroMoneyChange\"] < -2)) & (df[\"blind\"] == \"$0.01/$0.02\")"),
		# graph1(),
		html.P("((df[\"heroMoneyChange\"] > 2) | (df[\"heroMoneyChange\"] < -2)) & (df[\"blind\"] == \"$0.01/$0.02\")"),
		# graph2(),
	]

# @callback(
# 	Output("placeholder-p1", "children"), [Input("placeholder-p1", "children")]
# )
# def a(n):
# 	print("reach")
# 	print(cache.get("games"))
# 	return "a"
# @app.callback(Output("standalone-radio-check-output", "children"), Input("money-unit-select", "value"))
# def on_form_change(checklist_value):
# 	print("a", checklist_value)
# 	return str(checklist_value)
# @app.callback(
# 	dd.Output("standalone-radio-check-output", "children"),
# 	[
# 		dd.Input("standalone-switch", "value"),
# 	],
# )
# def on_form_change(switch_checked):
# 	print("reach")
# 	return f"Toggle Switch: {switch_checked}"

# return html.Div(result)
