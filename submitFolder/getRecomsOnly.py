import csv
from pprint import pprint
import pickle
import numpy as np
import argparse
import operator
import os

from content_based import mainSolo as content_based
from collabr_filter import main as collabr_filter

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="Give userId to " +
                               "calculate best options", type=str)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    N = 20
    user = args.u

    path = "./training_set_tiny_part/"
    files = os.listdir(path)

    reader = csv.reader(open(path + user + ".txt", 'r'))

    user = {}
    for row in reader:
        movie, rating, niks = row
        user[movie] = rating

    arrayofdics = []
    for filename in files:
        filePath = path + filename
        reader = csv.reader(open(filePath, 'r'))
        userdic = {}
        for row in reader:
              movie, rating, niks = row
              userdic[movie] = int(rating)
        arrayofdics.append(userdic)

    movieDict = load_obj("movieDict")
    print("Get content-based recommendations...")
    contentDict = content_based(user, movieDict)
    print("Get collaborative filtering recommendations...")
    collabrDict = collabr_filter(user, arrayofdics)
    print("")
    confidenceMovies = []

    for key in collabrDict:
        if key in contentDict:
            confidence = float(collabrDict[key])*float(contentDict[key])
            confidenceMovies.append([key, confidence])

    confidenceMovies.sort(key=lambda x: x[1], reverse=True)

    movieDictNames = load_obj("movieDictNames")
    for x in range(0, N):
        print(str(movieDictNames[confidenceMovies[x][0]]) + ": " +
              str(confidenceMovies[x][1]))
