def isEmptyString(string):
	if string is None or string == "":
		return True
	return False


def isArray(val):
	if type(val) not in (tuple, list):
		return False
	return True


def isDict(val):
	if type(val) is not dict:
		return False
	return True
