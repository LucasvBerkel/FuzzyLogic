import os
import csv
import argparse
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="Copy files, yes or no", type=str)
parser.add_argument("-t", help="Threshold for amount of reviews per movie", type=int)
args = parser.parse_args()

def getpercent(currentline, totallines):
    i = (currentline / totallines) * 100
    return i

# Prints the status to stdout
def writestatus(currentline, totallines):
    i = getpercent(float(currentline), float(totallines))
    stdout.write("\r%s" % i)
    stdout.flush()

if __name__ == "__main__":
	path = "training_set_without_old_reviews/"
	newPath = "training_set_without_old_reviews_impopular_movies/"
	files = os.listdir(path)

	totalLength = len(files)
	counter = 0
	vector = []
	
	threshold = args.t

	counterUnder = 0
	counterOver = 0
	counterTotal = 0

	counterOverMovies = 0
	counterUnderMovies = 0
	for fileName in files:
		writestatus(counter, totalLength)
		counter += 1
		filePath = path + fileName
		newFilePath = newPath + fileName
		with open(filePath, 'r') as f:
			csvFile = csv.reader(f, delimiter=',', quotechar='|')
			data = list(csvFile)
    		row_count = len(data)
    		vector.append(row_count)
    		if row_count > threshold:
    			counterOver += row_count
    			counterOverMovies += 1
    			if args.c == "yes":
    				copyfile(filePath, newFilePath)
    		else:
    			counterUnder += row_count
    			counterUnderMovies += 1
    		counterTotal += row_count
	
	array = np.asarray(vector)
	print "\nMaximum: " + str(array.max())
	print "Minimum: " + str(array.min())

	print ("\nNumber of valid reviews: " + str(counterOver))
	print ("Number of invalid reviews: " + str(counterUnder))
	print ("Total of reviews: " + str(counterTotal))

	print ("\nNumber of valid movies: " + str(counterOverMovies))
	print ("Number of invalid movies: " + str(counterUnderMovies))
	print ("Total of movies: " + str(totalLength))

	plt.hist(array, bins=100)
	plt.title('Histogram: Number of reviews per movie')
	plt.xlabel('Number of reviews')
	plt.ylabel('Number of movies')
	plt.show()