#Read CSV file
import csv

with open('data.csv', mode='r') as csv_file:
 csv_reader = csv.DictReader(csv_file)
 for row in csv_reader:
   print (row)
   role=row['role']
   PersonName=row['name']
   GID=row['gid']
