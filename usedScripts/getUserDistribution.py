import os
import csv
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile

def getpercent(currentline, totallines):
    i = (currentline / totallines) * 100
    return i

# Prints the status to stdout
def writestatus(currentline, totallines):
    i = getpercent(float(currentline), float(totallines))
    stdout.write("\r%s" % i)
    stdout.flush()

def getLargestInDict(user):
    v=list(user.values())
    k=list(user.keys())
    return k[v.index(max(v))]
	

if __name__ == "__main__":
	path = "finalTraining_Set/"
	files = os.listdir(path)

	totalLength = len(files)
	counter = 0
	user = {}

	for fileName in files:
		writestatus(counter, totalLength)
		counter += 1
		filePath = path + fileName
		with open(filePath, 'r') as f:
			csvFile = csv.reader(f, delimiter=',', quotechar='|')
			next(csvFile)
			for row in csvFile:
				if row[0] not in user:
					user[row[0]] = 0
				else:
					user[row[0]] += 1

	counter = 0
	numberReviews = []
	for key in user:
		numberReviews.append(user[key])
		counter += 1

	array = np.asarray(numberReviews)

	print("\nNumber of user: " + str(counter))
	plt.hist(array, bins=100)
	plt.title('Histogram: Number of reviews per user')
	plt.xlabel('Number of reviews')
	plt.ylabel('Number of users')
	plt.show()