def strToInt(text):
	try:
		text = int(text)
	except:
		print(text + " fail to convert number")
		return -1
	return text


def strToFloat(text):
	try:
		text = float(text)
	except:
		print(text + " fail to convert to float")
		return -1
	return text
