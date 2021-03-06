import csv
import pickle
import numpy as np

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


def main(user, movieDict, collabrDict):
    #movieDict = load_obj("movieDict")
    path = "./training_set_tiny_part/"

    filePath = path + str(user) + ".txt"
    seenMovies = {}

    #with open(filePath, 'r') as f:
    #    for row in a:
    #        key = str(int(row[0]))
     #       seenMovies[key] = [movieDict[key], float(row[1])]
   # f.close()

    for movie in user:
     key = str(int(movie))
     seenMovies[key] = [movieDict[key], float(user[movie])]
    recomMovies = {}
    for key in collabrDict:
            confidence = confidenceMovie(seenMovies, movieDict[key])
            recomMovies[key] = confidence
    
    print("content done")
    return recomMovies