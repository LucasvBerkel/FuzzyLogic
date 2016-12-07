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
    newPath = "newTraining_Set/"
    files = os.listdir(path)

    referenceYear = "2005"
    referenceMonth = "03"
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
        newFilePath = newPath + fileName
        with open(filePath, 'r') as f:
            csvFile = csv.reader(f, delimiter=',', quotechar='|')
            next(csvFile)
            with open(newFilePath, 'w') as w:
                for row in csvFile:
                    counterTotal += 1
                    data = row[2].split("-")
                    year = data[0]
                    month = data[1]
                    day = data[2]
                    if int(year) > int(referenceYear):
                        counterValid += 1
                        row[2] = row[2] + "\n"
                        w.write(",".join(row))
                    elif int(year) == int(referenceYear):
                        if int(month) > int(referenceMonth):
                            counterValid += 1
                            row[2] = row[2] + "\n"
                            w.write(",".join(row))
                        elif int(month) == int(referenceMonth):
                            if int(day) > int(referenceDay):
                                counterValid += 1
                                row[2] = row[2] + "\n"
                                w.write(",".join(row))
                            else:
                                counterInvalid += 1
                        else:
                            counterInvalid += 1
                    else:
                        counterInvalid += 1
            w.close()

    print("\nNumber of valid reviews: " + str(counterValid))
    print("Number of invalid reviews: " + str(counterInvalid))
    print("Total of reviews: " + str(counterTotal))
