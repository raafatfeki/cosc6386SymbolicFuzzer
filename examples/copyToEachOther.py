
def copyToEachOther(a: float, b: float, abc: float) -> int:
	c: int = a
	a = b
	b = c
	if (a == b):
		if(abc == b and (abc == a)):
			if(abc == a):
				print("Impossible")
				return -2
		return -1
	elif (a < b):
		if (c < a):
			print ("impossible")
			return -2
		return b - a
	else:
		return a - b