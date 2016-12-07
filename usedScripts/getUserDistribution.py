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
    path = "training_set_without_old_reviews_impopular_movies/"
    newPath = ("training_set_without_old_reviews_impopular_movies" +
               "_inactive_users/")
    files = os.listdir(path)

    totalLength = len(files)
    counter = 0
    user = {}

    print("Gather user information...")
    for fileName in files:
        writestatus(counter, totalLength)
        counter += 1
        filePath = path + fileName
        with open(filePath, 'r') as f:
            csvFile = csv.reader(f, delimiter=',', quotechar='|')
            for row in csvFile:
                if row[0] not in user:
                    user[row[0]] = 1
                else:
                    user[row[0]] += 1
        f.close()

    counter = 0
    numberReviews = []
    threshold = args.t
    counterInactive = 0
    counterActive = 0
    inactiveUsers = {}

    for key in user:
        numberReviews.append(user[key])
        if user[key] < threshold:
            counterInactive += 1
            inactiveUsers[key] = True
        else:
            counterActive += 1
            inactiveUsers[key] = False
        counter += 1

    if args.d == "yes":
        print("\nDeleting users from dataset below threshold...")
        counter = 0
        for fileName in files:
            writestatus(counter, totalLength)
            counter += 1
            filePath = path + fileName
            newFilePath = newPath + fileName
            with open(filePath, 'r') as f:
                csvFile = csv.reader(f, delimiter=',', quotechar='|')
                with open(newFilePath, 'w') as w:
                    for row in csvFile:
                        if not inactiveUsers[row[0]]:
                            row[2] = row[2] + "\n"
                            w.write(",".join(row))
                w.close()
            f.close()

    array = np.asarray(numberReviews)

    print("\nNumber of users: " + str(counter))
    print("\nThreshold inactive user: " + str(threshold) + " reviews")
    print("Number of active users: " + str(counterActive))
    print("Number of inactive users: " + str(counterInactive))

    plt.hist(array, bins=100)
    plt.title('Histogram: Number of reviews per user')
    plt.xlabel('Number of reviews')
    plt.ylabel('Number of users')
    plt.show()
