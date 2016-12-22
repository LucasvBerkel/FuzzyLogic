import csv
import pickle
import numpy as np

# This method calculates the confidence scores of every unseen movie for a user.
# It receives either the reduced collabrDict(for evaulating purposes) or not(for just recommending purposes)
# This method is always called from another file, so no option is given for users to directly call this method.
# That needs to be done from either eval.py or getRecomsOnly.py

# Function to retrieve dictionary from pickle file
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Similiraty measure between two movies, array1 and array2 represent the genres array of both movies
def similarityMovies(array1, array2):
    sumMin = np.sum(np.minimum(array1, array2))
    sumMax = np.sum(np.maximum(array1, array2))
    return sumMin/sumMax

# Method to calculate confidence between unseenmovie and seenmovies
def confidenceMovie(seenMovies, array1):
    confidence = []
    for key in seenMovies:
        similarity = similarityMovies(seenMovies[key][0], array1)
        likeble = seenMovies[key][1]/5
        if similarity < likeble:
            confidence.append(similarity)
        else:
            confidence.append(likeble)
    return max(confidence)

# Main method, receives the user, moviedict and collabrDict, so both methods have same information
def main(user, movieDict, collabrDict):
    seenMovies = {}

    for movie in user:
        key = str(int(movie))
        seenMovies[key] = [movieDict[key], float(user[movie])]
    recomMovies = {}
    for key in collabrDict:
            confidence = confidenceMovie(seenMovies, movieDict[key])
            recomMovies[key] = confidence
    
    print("Content done")
    return recomMovies

# Same method as above, only if content_based method is used alone
def mainSolo(user, movieDict):
    seenMovies = {}

    for movie in user:
        key = str(int(movie))
        seenMovies[key] = [movieDict[key], float(user[movie])]
    recomMovies = {}
    for key in movieDict:
        if key not in seenMovies:
            confidence = confidenceMovie(seenMovies, movieDict[key])
            recomMovies[key] = confidence
    
    print("Content done")
    return recomMovies