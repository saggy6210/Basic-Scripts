#Find list of users from <"USER_EMAILID"> and remove duplication 

import re

mylist = []
with open('email_list.txt', mode='r') as csv_file:
	for line in csv_file:
		#print (line)
		result = [x.strip() for x in line.split(';')]
		for id in result:
			mylist.append(id)
			r1 = re.findall(r'<.*>',id)
			print(r1)

#print (mylist)
a = set(mylist)

seen = set()
result = []
for item in a:
    if item not in seen:
        seen.add(item)
        result.append(item)
		
print (result)
for i in result:
	print (i)
