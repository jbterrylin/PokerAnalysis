import enum
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


def dictWithClassValueToDict(classes):
	return {
		key: classes.get(key, 0).__dict__ for key in set(classes)
	}


def classesToDict(classes):
	return [c.__dict__ if type(c) not in (tuple, list) else classesToDict(c) for c in classes]


def enumToVal(value):
	if isinstance(value, enum.Enum):
		return value.value
	return value


def allEnumInDictToVal(dicti):
	return {
		enumToVal(key): enumToVal(dicti.get(key, 0)) for key in set(dicti)
	}


def allEnumInDictsToVal(dicts):
	return [allEnumInDictToVal(d) if type(d) not in (tuple, list) else allEnumInDictsToVal(d) for d in dicts]
