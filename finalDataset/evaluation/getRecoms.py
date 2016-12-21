import csv
from pprint import pprint
import pickle
import numpy as np
import argparse
import operator

from content_based import main as content_based
from collabr_filter import main as collabr_filter

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="Give userId to " + "calculate best options", type=int)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
		
def testeval(user):
	N = 20
	print("Get content-based recommendations...")
	contentDict = content_based(user)
	print("Get collaborative filtering recommendations...")
	collabrDict, testmovie = collabr_filter(user)
	print("")
	confidenceMovies = []
	confidenceDict={}
	for key in collabrDict:
		if key in contentDict:
			confidence = float(collabrDict[key])*float(contentDict[key])
			confidenceMovies.append([key, confidence])
			confidenceDict[key] = confidence
			
	confidenceMovies.sort(key=lambda x: x[1], reverse=True)

	movieDictNames = load_obj("movieDictNames")
	print('confidence rating calculated for this many movies: ', len(confidenceMovies))
	print("highest: ", confidenceMovies[0][1], "lowest; ", confidenceMovies[len(confidenceMovies)-1][1])
	total = 0
	for movie in confidenceMovies:
		total = total + movie[1]
	print('average is: ', total/len(confidenceMovies))
	
	print('testid: ' , str(int(testmovie[0])))

	if str(int(testmovie[0])) in confidenceDict:
		print('ja')
		output = 1
	else:
		print('nee')
		output = 0
	return output
	
	#for x in range(0, N):
		#print(str(movieDictNames[confidenceMovies[x][0]]) + ": " +
		#str(confidenceMovies[x][1]))
		
if __name__ == "__main__":
	N = 20
	user = args.u
	print("Get content-based recommendations...")
	contentDict = content_based(user)
	print("Get collaborative filtering recommendations...")
	collabrDict, testmovie = collabr_filter(user)
	print("")
	confidenceMovies = []
	confidenceDict={}
	for key in collabrDict:
		if key in contentDict:
			confidence = float(collabrDict[key])*float(contentDict[key])
			confidenceMovies.append([key, confidence])
			confidenceDict[key] = confidence
			
	confidenceMovies.sort(key=lambda x: x[1], reverse=True)

	movieDictNames = load_obj("movieDictNames")
	print('confidence rating calculated for this many movies: ', len(confidenceMovies))
	print("highest: ", confidenceMovies[0][1], "lowest; ", confidenceMovies[len(confidenceMovies)-1][1])
	total = 0
	for movie in confidenceMovies:
		total = total + movie[1]
	print('average is: ', total/len(confidenceMovies))
	
	print('testid: ' , str(int(testmovie[0])))
	
	print(confidenceDict[str(int(testmovie[0]))])
	if str(int(testmovie[0])) in confidenceDict:
		print('ja')
	else:
		print('nee')
	#for x in range(0, N):
		#print(str(movieDictNames[confidenceMovies[x][0]]) + ": " +
		#str(confidenceMovies[x][1]))