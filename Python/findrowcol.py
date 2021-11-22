Find row and column number based on house number

hno = int(input())

for i in range(1, 6):
	col = i * i
	print (col)
	if hno % col == 0:
		row = hno / col
		
print ("Row:", row, "Coloumn : ", i)
