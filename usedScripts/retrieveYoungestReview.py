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

    youngestYear = "0000"
    youngestMonth = "00"
    youngestDay = "00"
    totalLength = len(files)
    counter = 0

    for fileName in files:
        writestatus(counter, totalLength)
        counter += 1
        filePath = path + fileName
        with open(filePath, 'r') as f:
            csvFile = csv.reader(f, delimiter=',', quotechar='|')
            next(csvFile)
            for row in csvFile:
                data = row[2].split("-")
                year = data[0]
                month = data[1]
                day = data[2]
                if int(year) > int(youngestYear):
                    youngestYear = year
                    if int(month) > int(youngestMonth):
                        youngestMonth = month
                        if int(day) > int(youngestDay):
                            youngestDay = day

    print("\n" + youngestYear + "-" + youngestMonth + "-" + youngestDay)
