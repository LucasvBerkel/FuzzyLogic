import os
import csv
import argparse
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument("-t", help="Threshold for amount " +
                    "of reviews per user", type=int)
parser.add_argument("-d", help="Delete user below threshold," +
                    " yes or no", type=str)
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
    path = "training_set/"
    newPath = "training_set_users/"
    files = os.listdir(path)

    totalLength = len(files)
    counter = 0
    user = {}

    print("Cluster user information...")
    for fileName in files:
        writestatus(counter, totalLength)
        counter += 1
        filePath = path + fileName
        with open(filePath, 'r') as f:
            movieName = fileName.split("_")[1].split(".")[0]
            csvFile = csv.reader(f, delimiter=',', quotechar='|')
            for row in csvFile:
                with open(newPath + row[0] + ".txt", 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    a.writerow([movieName, row[1], row[2]])
                fp.close()
        f.close()

    print("\nDone")
