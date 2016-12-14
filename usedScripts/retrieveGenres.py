import csv
from pprint import pprint
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    fileName = "movie_Titles_with_Genres_Final.csv"
    genreDict = {}
    counter = 0
    with open(fileName, 'r') as f:
        a = csv.reader(f, delimiter=",")
        for row in a:
            genres = row[3].split(",")
            for genre in genres:
                genre = genre.replace(" ", "")
                if genre not in genreDict:
                    genreDict[genre] = 1
                else:
                    genreDict[genre] += 1
    f.close()

    pprint(genreDict)

    genreIndexDict = {}
    counter = 0
    for key in genreDict:
        genreIndexDict[key] = counter
        counter += 1

    pprint(genreIndexDict)

    save_obj(genreIndexDict, "genreIndex")
