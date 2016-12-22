import csv
from pprint import pprint
import pickle
import numpy as np
import argparse
import operator
import os
from content_based import main as content_based
from collabr_filter import main as collabr_filter

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="Give userId to " + "calculate best options", type=int)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
		
def testeval(user, arrayofdics, movieDict):
	
	path = "./training_set_tiny_part/"

	filePath = path + str(user) + ".txt"
	
	reader = csv.reader(open(filePath, 'r'))
	
	totalrating = 0
	user = {}
	for row in reader:
	   movie, rating, niks = row
	   totalrating  = totalrating + int(rating)
	   user[movie] = rating
	   
	avgratingUser = totalrating/len(user)
	testmovie = user.popitem()
	
	
	N = 20
	print("Get collaborative filtering recommendations...")
	collabrDict = collabr_filter(user, arrayofdics)
	print("Get content-based recommendations...")
	contentDict = content_based(user, movieDict, collabrDict)

	print("")
	confidenceMovies = []
	confidenceDict={}
	for key in collabrDict:
		if key in contentDict:
			confidence = float(collabrDict[key])*float(contentDict[key])
			confidenceMovies.append([key, confidence])
			confidenceDict[key] = confidence + 1
			
	confidenceMovies.sort(key=lambda x: x[1], reverse=True)

	movieDictNames = load_obj("movieDictNames")
	print('confidence rating calculated for this many movies: ', len(confidenceMovies))
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
