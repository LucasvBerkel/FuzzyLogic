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

if __name__ == "__main__":
    fileName = "movie_Titles_with_Genres_Final.csv"
    movieDictNames = {}
    with open(fileName, 'r') as f:
        a = csv.reader(f, delimiter=",")
        for row in a:
            movieDictNames[row[0]] = row[2]
    f.close()

    save_obj(movieDictNames, "movieDictNames")