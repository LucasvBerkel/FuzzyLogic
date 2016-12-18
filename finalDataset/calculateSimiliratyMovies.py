import csv
from pprint import pprint
import pickle
import numpy as np
import argparse
import operator

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="Give userId to calculate best options", type=int)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def similarityMovies(array1, array2):
    sumMin = np.sum(np.minimum(array1, array2))
    sumMax = np.sum(np.maximum(array1, array2))
    return sumMin/sumMax

def confidenceMovie(seenMovie, array1):
    confidence = []
    for key in seenMovie:
        similarity = similarityMovies(seenMovie[key][0], array1)
        likeble = seenMovie[key][1]/5
        if similarity < likeble:
            confidence.append(similarity)
        else:
            confidence.append(likeble)
    return max(confidence)


if __name__ == "__main__":
    N = 20
    
    movieDict = load_obj("movieDict")

    path = "training_set_tiny_part/"

    user = args.u

    filePath = path + str(user) + ".txt"
    seenMovies = {}

    with open(filePath, 'r') as f:
        a = csv.reader(f, delimiter=",")
        for row in a:
            key = str(int(row[0]))
            seenMovies[key] = [movieDict[key], float(row[1])]
    f.close()

    confidenceMovies = []

    for key in movieDict:
        if key not in seenMovies:
            confidence = confidenceMovie(seenMovies, movieDict[key])
            confidenceMovies.append([key, confidence])

    confidenceMovies.sort(key=lambda x: x[0], reverse=True)

    movieDictNames = load_obj("movieDictNames")
    for x in range(0, N):
        print(movieDictNames[confidenceMovies[x][0]], ": ", confidenceMovies[x])