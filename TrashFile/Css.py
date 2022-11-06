def addReplaceStyle(oriStyle, additionalStyle):
	return {
		key: additionalStyle.get(key) if additionalStyle.get(key) is not None else oriStyle.get(key)
		for key in set(oriStyle) | set(additionalStyle)
	}


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
	"position": "fixed",
	"top": 0,
	"left": 0,
	"bottom": 0,
	"width": "16rem",
	"padding": "2rem 1rem",
	"background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
	"margin-left": "18rem",
	"margin-right": "18rem",
	"padding": "2rem 2rem",
}

# input that look like dropdown
INPUT_LIKE_DD_STYLE = {
	"border": "1px solid #ccc",
	"border-radius": "4px",
	"height": "36px",
	"width": "100%"
}


BUTTON_STYLE = {
	"border": "1px solid #ccc",
	"height": "36px"
}
