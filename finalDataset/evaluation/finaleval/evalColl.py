import getRecomsColl
import os
import csv
import pickle
path = "C:\\Users\\Joris\\Dropbox\\fuzzy\\fuzzycomb\\training_set_tiny_part/"
files = os.listdir(path)

import numpy as np


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

movieDict = load_obj("movieDict")
counter = 0
right = 0
wrong = 0
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
		
i = 0
for filename in files:
	i = i + 1
	output, correct = getRecomsColl.testeval(filename.split('.')[0], arrayofdics, movieDict)
	if correct == 1:
		right = right + 1
	if correct == 0: 
		wrong = wrong + 1
	counter = counter + output
	print('total is ', counter, ' out of ', i)
	if counter != 0:
		print('accuracy so far is: ', (right/counter) * 100)