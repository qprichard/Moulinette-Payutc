import csv 
import sys

fundation = sys.argv[1]


with open('new.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if(row[2]!=''):
			sys.argv=["test.py",fundation, row[2], row[3]]
			print (sys.argv)
			execfile("test.py")


			print(row[2])
