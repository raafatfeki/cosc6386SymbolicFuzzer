def realValues(a: float, b: float, k: float) -> int:
	if ((a == 0.1) and (k == 0.001)):
		print("Example of real values")
		if((a - k) == b):
			print("Example of operations within condition")
			return 1
	if (a != b and a != k):
		if (b == k):
			print("equals")
		else:
			print ("Not Equals")
	return 0