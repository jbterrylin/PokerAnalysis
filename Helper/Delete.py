from Helper.Compare import isArray


def delValInDictByKey(dicti, key):
	if dicti.get(key) is not None:
		dicti.pop(key)
	return dicti


def delValInDictsByKey(dicts, key):
	return [delValInDictByKey(d, key) if not isArray(d) else delValInDictsByKey(d, key) for d in dicts]
