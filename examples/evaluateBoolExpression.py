def evaluateBoolExpression(a: int, b: int) -> int:
	c: bool = (a < b)
	if(c):
		print("hello")
	else:
		if (a == b):
			print("s")
		elif (a < b):
			print("impossible")
		else:
			print("yes")

