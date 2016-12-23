import csv
import pickle
import argparse
import os
from sys import stdin

from content_based import mainSolo as content_based
from collabr_filter import main as collabr_filter

# This method is used to get the top 20 recommendations using the combined method
# User can give a user id from which the best recommendations are calculated.

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="Give userId to " +
                               "calculate best options", type=str)
args = parser.parse_args()

# Method to load pickle file to python dictionary
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    # Number of recommendations
    N = 20
    user = args.u

    movieDictNames = load_obj("movieDictNames")

    # Path to training set
    path = "./training_set_tiny_part/"
    files = os.listdir(path)

    if user == "make":
        movieList = ["12338", "11283", "14691", "1905", "2782", "4306", "5345", "10820", "12918", "14185", "4266", "5775", "6720", "9628", "11521"]
        user = {}
        counter = 5
        for movie in movieList:
            print(str(counter) + " movies to rate")
            print(movieDictNames[movie] + ":")
            userinput = stdin.readline()
            if(userinput == "" or userinput == "\n"):
                continue
            elif(int(userinput) > 0  and int(userinput) < 6):
                user[movie.zfill(7)] = userinput
                counter -= 1
            if counter == 0:
                break


        
    else:
        reader = csv.reader(open(path + user + ".txt", 'r'))

        # Filling dicts and array of dicts so collabr_filter and content_based can handle them
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

    # Loading moviedict(id corresponding to array of membership of genres)
    movieDict = load_obj("movieDict")
    print("Get content-based recommendations...")
    contentDict = content_based(user, movieDict)
    print("Get collaborative filtering recommendations...")
    collabrDict = collabr_filter(user, arrayofdics)
    print("")

    confidenceMovies = []
    # Transport dict to array for sorting purposes
    for key in collabrDict:
        if key in contentDict:
            confidence = float(collabrDict[key])*float(contentDict[key])
            confidenceMovies.append([key, confidence])

    confidenceCollr = []
    # Transport dict to array for sorting purposes
    for key in collabrDict:
        confidenceCollr.append([key, collabrDict[key]])

    confidenceCont = []
    # Transport dict to array for sorting purposes
    for key in contentDict:
        confidenceCont.append([key, contentDict[key]])

    confidenceMovies.sort(key=lambda x: x[1], reverse=True)
    confidenceCollr.sort(key=lambda x: x[1], reverse=True)
    confidenceCont.sort(key=lambda x: x[1], reverse=True)

    movieDictNames = load_obj("movieDictNames")

    print("Recommendations through combination method:")
    for x in range(0, N):
        print(str(movieDictNames[confidenceMovies[x][0]]) + ": " +
              str(confidenceMovies[x][1]))
    print("")

    print("Recommendations through collaborative filtering method:")
    for x in range(0, N):
        print(str(movieDictNames[confidenceCollr[x][0]]) + ": " +
              str(confidenceCollr[x][1]))
    print("")

    print("Recommendations through content-based method:")
    for x in range(0, N):
        print(str(movieDictNames[confidenceCont[x][0]]) + ": " +
              str(confidenceCont[x][1]))
