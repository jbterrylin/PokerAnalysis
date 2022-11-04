import enum
from decimal import Decimal

from Helper.Compare import isArray


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
		key: classes.get(key).__dict__ for key in set(classes)
	}


def classesToDict(classes):
	return [c.__dict__ if not isArray(c) else classesToDict(c) for c in classes]


def enumToVal(value):
	if isinstance(value, enum.Enum):
		return value.value
	return value


def allEnumInDictToVal(dicti):
	return {
		enumToVal(key): enumToVal(dicti.get(key)) for key in set(dicti)
	}


def allEnumInDictsToVal(dicts):
	return [allEnumInDictToVal(d) if not isArray(d) else allEnumInDictsToVal(d) for d in dicts]
