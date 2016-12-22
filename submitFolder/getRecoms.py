import csv
from pprint import pprint
import pickle
import numpy as np
import operator
import os
from content_based import main as content_based
from collabr_filter import main as collabr_filter
from content_based import mainSolo as content_based_solo
from collabr_filter import main as collabr_filter

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
		
#This is the function used by the evaluation method which produces a list with predictions of rating for a user
#First, the user is read from a txt file. Next, one of its ratings is separated to use as a test set
#The predictions are based on the method specified in the input of this function
#The test movie is then compared to its prediction and the output is based on whether the prediction is higher/lower than the average
#prediction and the actual rating was higher/lower than the average of the users ratings.
 
def testeval(user, arrayofdics, movieDict, method):
	
    path = "./training_set_tiny_part/"
    filePath = path + str(user) + ".txt"
    
	#The data of the user is read
	
    reader = csv.reader(open(filePath, 'r'))
    totalrating = 0
    user = {}
    for row in reader:
        movie, rating, niks = row
        totalrating  = totalrating + int(rating)
        user[movie] = rating

    avgratingUser = totalrating/len(user)
    testmovie = user.popitem()

	#Here the collaborative and the content_based methods are called to retrieve dictionaries with values for each movie
	
    if(method == "all"):
        print("Get collaborative filtering recommendations...")
        collabrDict = collabr_filter(user, arrayofdics)
        print("Get content-based recommendations...")
        contentDict = content_based(user, movieDict, collabrDict)
    elif(method == "content_based"):
        print("Get content-based recommendations...")
        contentDict = content_based_solo(user, movieDict)
    elif(method == "collaborative_filtering"):
        print("Get collaborative filtering recommendations...")
        collabrDict = collabr_filter(user, arrayofdics)

    print("")
	
	#The confidence score is calculated by the product of the two values if the combined method is chosen
	#Otherwise it is equal to the outputs of the respective methods
	
    confidenceMovies = []
    confidenceDict={}
    if(method == "all"):
    	for key in collabrDict:
    		if key in contentDict:
    			confidence = float(collabrDict[key])*float(contentDict[key])
    			confidenceMovies.append([key, confidence])
    			confidenceDict[key] = confidence + 1
    elif(method == "content_based"):
    	for key in contentDict:
            confidence = float(contentDict[key])
            confidenceMovies.append([key, confidence])
            confidenceDict[key] = confidence
    elif(method == "collaborative_filtering"):
    	for key in collabrDict:
            confidence = float(collabrDict[key])
            confidenceMovies.append([key, confidence])
            confidenceDict[key] = confidence + 1
    		
    confidenceMovies.sort(key=lambda x: x[1], reverse=True)
	print('confidence rating calculated for this many movies: ', len(confidenceMovies))
	
    movieDictNames = load_obj("movieDictNames")
	
	
	#The prediction for the test movie is compared to the actual rating here
	#If there is no prediction for the test movie 'output' will be set to 0 
	
    total = 0
    for movie in confidenceMovies:
    	total = total + movie[1]
    
    correct  = 2
    if str(int(testmovie[0])) in confidenceDict:
        output = 1
        print('the actual rating was: ', testmovie[1])
        print('the prediction was: ' , confidenceDict[str(int(testmovie[0]))])
        if (confidenceDict[str(int(testmovie[0]))] >= total/len(confidenceMovies) and int(testmovie[1]) >= avgratingUser ) or (confidenceDict[str(int(testmovie[0]))] <= total/len(confidenceMovies) and int(testmovie[1]) < avgratingUser):
            correct = 1
        else:
            correct = 0
    else:
        output = 0
    return output, correct