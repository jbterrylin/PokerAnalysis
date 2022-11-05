# https://bobbyhadz.com/blog/python-merge-and-sum-two-dictionaries
from Helper.Convert import noneTo0


def combineDictWithSum(dict1, dict2):
	return {
		key: dict1.get(key, 0) + dict2.get(key, 0) for key in set(dict1) | set(dict2)
	}


def addIfNotExistInDict1(dict1, dict2):
	return {
		key: dict2.get(key, 0) if dict1.get(key, 0) is None else dict1.get(key, 0) for key in set(dict1) | set(dict2)
	}


def combineMultiDictWithSum(dicts):
	result = dicts.pop()
	for d in dicts:
		result = combineDictWithSum(result, d)
	return result
