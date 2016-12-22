import os
import csv
import sys
import math
import numpy as np
import operator
import pandas
import pickle

# This function applies the collaborative filter algorithm.  It uses the data of an input user and the data of all other users to create
# a list of recommendation values for each of the movies seen by the K nearest neighbours of the input user.

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Reads the data of a user and puts it in a dictionary.

def readInputUser(fileName):
	reader = csv.reader(open(fileName, 'r'))
	user = {}
	for row in reader:
	   movie, rating, niks = row
	   user[movie] = rating
	return user
 
# Reads all the data in the given path and puts that in a List of dictionaries, 
# each dictionary represents one user and contains its ratings and corresponding movie id's 

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

# Compares each user to the input user to see if they have rated a least number of movies
# which the input user also rated and stores them in a new array.

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

# To compare users to each other two vectors need to be made representing the ratings for the movies
# that both users watched. This function finds the movies that both the user and all other users watched
# and returns to vectors which indices represents each movie

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
	
	# These two lines can be uncommented to get a better understanding of what is happening here
	# print('for the input user the ratings were ', AlluserRatings[0])
	# print('for the first other user the ratings were ', AllOtheruserRatings[0])
	
	return AlluserRatings, AllOtheruserRatings

# This function calculates the distance between two vectors and returns the K closest ones in an array
# The first element in the output list is ignored because that is always the input user itself with 0 distance

def getKMostsimilarUsers(arrayofvalid, AlluserRatings, AllOtheruserRatings, K):
	i = 0
	for otheruser in arrayofvalid:
		dist = np.linalg.norm(AlluserRatings[i]-AllOtheruserRatings[i])
		arrayofvalid[i]['distance'] = dist
		i = i + 1
	arrayofvalid.sort(key=operator.itemgetter('distance'))
	return arrayofvalid[1:K+1]

# This function scrolls over all the movies that the K most similar users have watched and gives each of them
# a weighed rating, this rating is based on the average rating for that movie, how many times it has been rated and the average
# rating of all the movies in the database. This returns a true Bayesian estimate.

def computeWeighedRatings( KMostsimilarUsers, m):

	# First the K nearest neighbours given a weight based on their distance in order to fuzzify the KNN algorithm
	
	# Set minimum distance
	minDistance = KMostsimilarUsers[0]['distance']
	# Normalise all users to minimum distance
	for user in KMostsimilarUsers:
		user['distance'] = float(minDistance) / (float(user['distance'] + 0.0001)) #0.0001 is for prevention of division by 0
	# Init mean ratings
	meanratings = {}
	# Loop through all users
	for user in KMostsimilarUsers:
		# Loop through all movies of those users
		for key in user:
			# Because of the double loop, check if movie is already handled
			if key not in meanratings:
				# Init sums
				totalRating = 0
				totalFuzzyDistance = 0
				# Loop through all users for calculating meanrating
				for user2 in KMostsimilarUsers:
					if key in user2:
						totalRating += user2[key]*user2['distance']
						totalFuzzyDistance += user2['distance']
				# Retrieve fuzzy rating
				if totalFuzzyDistance > 0:
					meanratings[key] = (float(totalRating)/float(totalFuzzyDistance))
				else: 
					# Should not happen but prevents division by 0
					meanratings[key] = 0

				
	dataframe = pandas.DataFrame(KMostsimilarUsers)
	averagerating = 3.55 # needs to be average of all ratings in the database, a constant
	weighedratings = {}
	for movie in dataframe:
		R = meanratings[movie]
		v = dataframe[movie].count()
		weighedRating = (v / (v +m)) * R + (m / (v+m)) * averagerating
		weighedratings[movie] = weighedRating
	return weighedratings

# This function returns the weighed ratings of the movies that the input user has not already seen.

def getTopReccomendations(weighedRatings, user):
	sortedWeighedRatings = sorted(weighedRatings, key=weighedRatings.get, reverse = True)
	finalDic = {}
	counter =0

	for movie in sortedWeighedRatings:
		if not movie in user:
			finalDic[str(int(movie)) ] = weighedRatings[movie]
			counter = counter + 1
	return finalDic

def main(user, arrayofdics):
    path = "./training_set_tiny_part/"

    filePath = path + str(user) + ".txt"
    
    # The percentage of movies that another user must have seen in the list of movies of the input user
    PercentageOfSameMovies = 0.6 

    # The K nearest neighbours are considered as the similar users which are used to base the recommendation on
    K =  7
    # The least number of ratings needed for a movie to be considered for a high rating in the weighed ratings (note: the maximum is K)
    m = 0.5 * K 
	   
    leastNrOfSameMovies = math.floor(PercentageOfSameMovies * len(user))
    
    arrayofvalid = getAllValids(user, arrayofdics, leastNrOfSameMovies )
    del arrayofdics
    
    AlluserRatings, AllOtheruserRatings = getRatingVectors(user, arrayofvalid)
    KMostsimilarUsers = getKMostsimilarUsers(arrayofvalid, AlluserRatings, AllOtheruserRatings, K)
    weighedRatings =  computeWeighedRatings( KMostsimilarUsers, m)
    del weighedRatings['distance']
    
    finalDict = getTopReccomendations(weighedRatings, user)

    return finalDict
