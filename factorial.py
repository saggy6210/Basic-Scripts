n = int(input())
def fact(num):
	if num == 1:
		return num
	else:
		return num * fact(num -1)

if __name__=='__main__':
	if n < 0:
		print ("No factorial")
	elif n == 0: 
		print ("factorial is ", n)
	else:
		print ("factorial is ", fact(n))
