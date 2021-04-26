
def copyToEachOther(a: float, b: float, k: float) -> int:
	c: int = a
	a = b
	b = c
	if (a == b):
		if(k == b and (k == a)):
			if(k == a):
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