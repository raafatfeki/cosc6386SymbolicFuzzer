def boolOnly(a: bool, b: bool) -> bool:
	if (a and b):
		print(" both True")
	elif (a and (not b)):
		print("Only a")
	elif (not a and b):
		print ("only b")
	else:
		print("none")
	return True