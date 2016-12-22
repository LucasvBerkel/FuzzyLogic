import csv
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    fileName = "movie_Titles_with_Genres.csv"
    genreDict = {}
    counter = 0
    with open(fileName, 'r') as f:
        a = csv.reader(f, delimiter=",")
        for row in a:
            genres = row[3].replace(" ", "")
            genres = genres.split(",")
            for genre in genres:
                if genre not in genreDict:
                    genreDict[genre] = counter
                    counter += 1
    f.close()

    save_obj(movieDict, "genreIndex")