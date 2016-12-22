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
    path = "./"
    files = os.listdir(path)
    counter = 0
    totalRating = 0
    ratingCounter = 0
    totalLength = len(files)

    for fileName in files:
        writestatus(counter, totalLength)
        counter += 1
        filePath = path + fileName
        if(fileName != "averageRating.py"):
            with open(filePath, 'r') as f:
                csvFile = csv.reader(f, delimiter=',', quotechar='|')
                for row in csvFile:
                    totalRating += int(row[1])
                    ratingCounter += 1

    print("\n" + "Average rating is: " + str(float(totalRating)/float(ratingCounter)))
