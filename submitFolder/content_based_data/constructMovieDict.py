import csv
from pprint import pprint
import pickle
import numpy as np

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def fuzzy_math(genres):
    length = len(genres)
    alpha = 1.2
    weights = []
    for x in range(1, length+1):
        exponent = np.sqrt(alpha*length*(x-1))
        weights.append(x/np.power(2, exponent))
    return weights


if __name__ == "__main__":
    fileName = "movie_Titles_with_Genres.csv"
    movieDict = {}
    movieIndexDict = load_obj("genreIndex")
    with open(fileName, 'r') as f:
        a = csv.reader(f, delimiter=",")
        for row in a:
            genres = row[3].replace(" ", "")
            genres = genres.split(",")
            weights = fuzzy_math(genres)
            arrayMovie = np.zeros(25)
            for x in range(0, len(genres)):
                arrayMovie[movieIndexDict[genres[x]]] = weights[x]
            movieDict[row[0]] = arrayMovie
    f.close()

    save_obj(movieDict, "movieDict")