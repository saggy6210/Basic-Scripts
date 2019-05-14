year = int(input("Enter a Year"))
if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0: 
	print ("Leap Year")
else:
	print ("{0} not a leap year".format(year))
