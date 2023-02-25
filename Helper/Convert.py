import enum
from decimal import Decimal

from Helper.Compare import isArray, isDict


def strToInt(text):
	try:
		text = int(text)
	except:
		print(str(text) + "fail to convert number")
		return -1
	return text


# fake int = float * 100, to solve jibai language cannot handle float +-*/ problem
def strToFakeInt(text):
	return int(strToFloat(text) * 100)


def strToFloat(text):
	try:
		text = Decimal(text)
	except:
		print(str(text) + "fail to convert to float")
		return -1
	return text


def noneTo0(num):
	if num is None:
		return 0
	return num


def toDict(val):
	if not isDict(val):
		return val.__dict__
	return val


def flatArray(arr):
	return [item for sublist in arr for item in sublist]


def expandArrayLength(arr, leng, expandWith=None):
	length = len(arr)
	if length < leng:
		arr.extend([expandWith] * (leng - length))
	return arr


def fakeIntToBB(val, bbUnit):
	if isArray(val):
		return [v / bbUnit[i] for i, v in enumerate(val)]
	return val / bbUnit


def dictWithClassValueToDict(classes):
	return {
		key: toDict(classes.get(key)) for key in set(classes)
	}


def classesToDict(classes):
	return [toDict(c) if not isArray(c) else classesToDict(c) for c in classes]


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
