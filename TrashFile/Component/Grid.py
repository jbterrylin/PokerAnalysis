import dash_bootstrap_components as dbc

from Helper.Compare import isArray


def toGrid(components, rowStyle=None, colStyle=None, widths=None):
	return dbc.Row(
		[
			dbc.Col(
				[c],
				style=(colStyle if not isArray(colStyle) else colStyle[i]),
				width=(widths if not isArray(widths) else widths[i])
			)
			for i, c in enumerate(components)
		],
		style=rowStyle
	)
