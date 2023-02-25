def setGraphStyle(fig):
	# return fig.update_layout(paper_bgcolor="rgb(14, 17, 23)", plot_bgcolor="rgb(39, 39, 49)", font_color="white")
	fig.update_xaxes(showgrid=True, gridcolor="rgb(235, 240, 248)")
	fig.update_yaxes(showgrid=True, gridcolor="rgb(235, 240, 248)")
	return fig.update_layout(paper_bgcolor="#FFF", plot_bgcolor="#FFF", font_color="black")
