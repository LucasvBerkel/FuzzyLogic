import os
import csv
import sys
import math
import numpy as np
import operator
import pandas
import pickle

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#Reads the data of a user and puts it in a dictionary.
def readInputUser(fileName):
	reader = csv.reader(open(fileName, 'r'))
	user = {}
	for row in reader:
	   movie, rating, niks = row
	   user[movie] = rating
	return user
 
#Reads all the data in the given path and puts that in a List of dictionaries, 
#each dictionarie represents one user.
def readAllUsers(path):
	files = os.listdir(path)
	arrayofdics = []
	for filename in files:
		filePath = path + filename
		reader = csv.reader(open(filePath, 'r'))
		userdic = {}
		for row in reader:
		   movie, rating, niks = row
		   userdic[movie] = int(rating)
		arrayofdics.append(userdic)
	return arrayofdics

#Compares each user to the input user to see if they have rated a least number of movies
#which the input user also rated and stores them in a new array.
def getAllValids(user, arrayofdics, leastNrOfSameMovies):
	valids = 0
	arrayofvalid = []
	total = 0
	for otheruser in arrayofdics:
		NrOfSame = 0
		for movie, rating in user.items():
			if movie in otheruser:
				NrOfSame = NrOfSame + 1
		if(NrOfSame >= leastNrOfSameMovies):
			valids = valids+ 1
			arrayofvalid.append(otheruser)
		total = total + 1
	
	return(arrayofvalid)

#To compare users to each other two vectors need to be made representing the ratings for the movies
#that both users watched. This function finds the movies that both the user and all other users watched
#and returns to vectors which indices represents each movie
def getRatingVectors(user, arrayofvalid):

	AlluserRatings = []
	AllOtheruserRatings = []
	
	for otheruser in arrayofvalid:
		userRatings = []
		otherUserRatings = []
		for movie, rating in user.items():
			if movie in otheruser:
				userRatings.append(int(rating))
				otherUserRatings.append(int(otheruser[movie]))
				
		AlluserRatings.append(np.asarray(userRatings))
		AllOtheruserRatings.append(np.asarray(otherUserRatings))
	
	#print('for the first user the ratings were ', AlluserRatings[0])
	#print('for the first other user the ratings were ', AllOtheruserRatings[0])
	return AlluserRatings, AllOtheruserRatings

#This function calculates the distance between two vectors and returns the K closest ones in a array
def getKMostsimilarUsers(arrayofvalid, AlluserRatings, AllOtheruserRatings, K):
	i = 0
	for otheruser in arrayofvalid:
		dist = np.linalg.norm(AlluserRatings[i]-AllOtheruserRatings[i])
		arrayofvalid[i]['distance'] = dist
		i = i + 1
	arrayofvalid.sort(key=operator.itemgetter('distance'))
	return arrayofvalid[1:K+1]

#This function scrolls over all the movies that the K most similar users have watched and gives each of them
#a weighed rating, this rating is based on the average rating for that movie, how many times it has been rated and the average
#rating of all the movies in the database. This returns a true Bayesian estimate.
def computeWeighedRatings( KMostsimilarUsers, C):
	dataframe = pandas.DataFrame(KMostsimilarUsers)
	meanratings = dict(dataframe.mean())
	averagerating = 3 # needs to be average of all rating in database, a constant
	weighedratings = {}
	for movie in dataframe:
		R = meanratings[movie]
		v = dataframe[movie].count()
		weighedRating = (v / (v +C)) * R + (C / (v+C)) * averagerating
		weighedratings[movie] = weighedRating
	return weighedratings

#This function returns the movies with the top N weighed ratings that the input user has not already rated
def getTopReccomendations(weighedRatings, user):
	sortedWeighedRatings = sorted(weighedRatings, key=weighedRatings.get, reverse = True)
	finalDic = {}
	counter =0

	for movie in sortedWeighedRatings:
		if not movie in user:
			finalDic[str(int(movie)) ] = weighedRatings[movie]
			counter = counter + 1
		else:
			print('this movie was in user', movie)
	return finalDic

def main(user):
    path = "./training_set_tiny_part/"

    filePath = path + str(user) + ".txt"
    
    #The percentage of movies that another user must have seen in the list of movies of the input user
    PercentageOfSameMovies = 0.1    

    #The K nearest neighbours are considered as the similar users which are used to base the recommendation on
    #K = 6
    K =  6
    #The least number of ratings needed for a movie to be considered for the weighed ratings (note: the maximum is K)
    #C = 0.5 * K 
    C = 3
    user = readInputUser(filePath)
	
	#grabbing a random rating
    testmovie = user.popitem()
	
    arrayofdics = readAllUsers(path)
    leastNrOfSameMovies = math.floor(PercentageOfSameMovies * len(user))
    
    arrayofvalid = getAllValids(user, arrayofdics, leastNrOfSameMovies )
    del arrayofdics
    
    AlluserRatings, AllOtheruserRatings = getRatingVectors(user, arrayofvalid)
    KMostsimilarUsers = getKMostsimilarUsers(arrayofvalid, AlluserRatings, AllOtheruserRatings, K)
    weighedRatings =  computeWeighedRatings( KMostsimilarUsers, C)
    del weighedRatings['distance']
    
    finalDict = getTopReccomendations(weighedRatings, user)

    return finalDict, testmovie
