n = int(input("Enter a number"))

if n > 1: 
	for i in range(2, n):
		if n % i == 0:
			print ("Not a prime")
			break
	else:
		print ("prime No", n)
else:
	print("Not a prime")
