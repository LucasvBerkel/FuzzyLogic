import os
import csv
import argparse
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="Percentage of dataset", type=int)
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
    path = "training_set_users/"
    newPath = "training_set_tiny_part/"
    files = os.listdir(path)

    totalLength = len(files)
    referenceLength = int(totalLength*(float(args.p)/100))
    counter = 0
    print("Cluster user information...")
    for fileName in files:
        writestatus(counter, referenceLength)
        counter += 1
        src = path + fileName
        dst = newPath + fileName
        copyfile(src, dst)
        if(counter == referenceLength):
            break

    print("\nDone")
