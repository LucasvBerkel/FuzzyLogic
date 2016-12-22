from getRecoms import testeval as recoms
import os
import csv
import pickle
import numpy as np
import argparse

#This function is used to evaluate the different methods used to recommend movies to users
#As input, it is required to specify which method should be used - 'all', 'content_based' or 'collaborative_filtering'
#This function iterates over every user file in the specified path and uses the getRecoms functions to see whether a good prediction has been made
#The accuracy is printed after every user iteration

parser = argparse.ArgumentParser()
parser.add_argument("-m", help="Method to evaluate(all, content_based or collaborative_filtering", type=str)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
	
	method = args.m
	
	#First all the data in the given path is stored in an array of dictionaries
	#Each dictionary represents one user, the dictionaries contain the movie id's and the ratings of those movies
	#This array is used by the collaborative_filtering method to compare a user to all others
	
	path = "./training_set_tiny_part/"
	files = os.listdir(path)
	arrayOfDics = []
	
	for filename in files:
		filePath = path + filename
		reader = csv.reader(open(filePath, 'r'))
		userdic = {}
		for row in reader:
			  movie, rating, nothing = row
			  userdic[movie] = int(rating)
		arrayOfDics.append(userdic)
	
	
	#Here the algorithm is run on every user in the training data
	#the getRecoms function returns two values, 'output' and 'correct'
	#Because the collaborative_filtering method only provides predictions for all the movies rated by the K nearest
	#neighbours, it does not always have a prediction for the test_movie
	#In case of no output: output = 0 and correct = 2
	#In case of a prediction: output  = 1 and correct = 0 or 1
	
	movieDict = load_obj("movieDict")
	counter = 0
	right = 0
	wrong = 0
	i = 0
	
	for filename in files:
		i = i + 1
		if(method in  ["all", "content_based", "collaborative_filtering"]):
			output, correct = recoms(filename.split('.')[0], arrayOfDics, movieDict, method)
		else:
			print("Undefined method")
			break
		if correct == 1:
			right = right + 1
		if correct == 0: 
			wrong = wrong + 1
		counter = counter + output
		print('total is ', counter, ' out of ', i)
		if counter != 0:
			print('accuracy so far is: ', (right/counter) * 100)