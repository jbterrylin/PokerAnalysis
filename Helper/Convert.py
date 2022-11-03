from decimal import Decimal


def strToInt(text):
	try:
		text = int(text)
	except:
		print(text + " fail to convert number")
		return -1
	return text


# fake int = float * 100, to solve jibai language cannot handle float +-*/ problem
def strToFakeInt(text):
	return int(strToFloat(text) * 100)


def strToFloat(text):
	try:
		text = Decimal(text)
	except:
		print(text + " fail to convert to float")
		return -1
	return text


def noneTo0(num):
	if num is None:
		return 0
	return num
