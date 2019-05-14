first = 0
last = 1
n = int(input())
for i in range (0, n):
	if i == 0 or i == 1:
		print(i)
	else:
		curr= first +last
		print (curr)
		first = last
		last = curr 
