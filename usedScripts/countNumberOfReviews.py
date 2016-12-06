import os
import csv
from sys import stdout

def getpercent(currentline, totallines):
    i = (currentline / totallines) * 100
    return i

# Prints the status to stdout
def writestatus(currentline, totallines):
    i = getpercent(float(currentline), float(totallines))
    stdout.write("\r%s" % i)
    stdout.flush()

if __name__ == "__main__":
	path = "training_set/"
	files = os.listdir(path)

	referenceYear = "2004"
	referenceMonth = "09"
	referenceDay = "14"
	totalLength = len(files)
	counter = 0
	counterValid = 0
	counterInvalid = 0
	counterTotal = 0

	for fileName in files:
		writestatus(counter, totalLength)
		counter += 1
		filePath = path + fileName
		with open(filePath, 'r') as f:
			csvFile = csv.reader(f, delimiter=',', quotechar='|')
			next(csvFile)
			for row in csvFile:
				counterTotal += 1
				data = row[2].split("-")
				year = data[0]
				month = data[1]
				day = data[2]
				if int(year) > int(referenceYear):
					counterValid +=1
				elif int(year) == int(referenceYear):
					if int(month) > int(referenceMonth):
						counterValid += 1
					elif int(month) == int(referenceMonth):
						if int(day) > int(referenceDay):
							counterValid+= 1
						else:
							counterInvalid += 1
					else:
						counterInvalid += 1
				else: counterInvalid += 1
	
	print ("\nNumber of valid reviews: " + str(counterValid))
	print ("Number of invalid reviews: " + str(counterInvalid))
	print ("Total of reviews: " + str(counterTotal))
