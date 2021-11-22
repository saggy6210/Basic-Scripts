import re

mylist = []

with open('email_list.txt', mode='r') as csv_file:
	for line in csv_file:
		if re.match("(.*)title(.*)", line):
			#print line,
			mylist.append(line)
	
for i in mylist:
		print (i)
