def strToInt(str):
  try:
    str = int(str)
  except:
    print(str + " fail to convert number")
    return -1
  return str

def strTofFloat(str):
  try:
    str = float(str)
  except:
    print(str + " fail to convert to float")
    return -1
  return str
