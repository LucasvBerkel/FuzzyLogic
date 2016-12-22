import getRecoms
import getRecomsColl
import getRecomsCont
import os
import csv
import pickle

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-m", help="Method to evaluate(all, content_based or collaborative_filtering)", type=str)
args = parser.parse_args()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
	method = args.m

	path = "C:\\Users\\Joris\\Dropbox\\fuzzy\\fuzzycomb\\training_set_tiny_part/"
	files = os.listdir(path)

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
		if(method == "all"):
			output, correct = getRecoms.testeval(filename.split('.')[0], arrayofdics, movieDict)
		elif(method == "content_based"):
			output, correct = getRecomsCont.testeval(filename.split('.')[0], arrayofdics, movieDict)
		elif(method == "collaborative_filtering"):
			output, correct = getRecomsColl.testeval(filename.split('.')[0], arrayofdics, movieDict)
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