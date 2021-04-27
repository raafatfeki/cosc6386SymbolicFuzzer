def realValues(a: float, b: float, kx: float) -> int:
	if ((a == 0.1) and (kx == 0.001)):
		print("Example of real values")
		if((a - kx) == b):
			print("Example of operations within condition")
			return 1
	if (a != b and a != kx):
		if (b == kx):
			print("equals")
		else:
			print ("Not Equals")
	return 0