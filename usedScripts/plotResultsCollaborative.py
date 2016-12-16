import getTopNCollaborative
import os
path = "C:\\Users\\Joris\\Dropbox\\fuzzy\\training_set_tiny_part/"
files = os.listdir(path)

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 17770, 0, 100])
plt.ion()
topratings = {}
for filename in files:
	dict = getTopNCollaborative.main(filename)
	dict = list(dict.keys())
	movie = int(dict[0])
	if movie in topratings:
		topratings[movie] = topratings[movie] + 1
	else:
		topratings[movie] = 1
	plt.bar(movie, topratings[movie])
	plt.pause(0.05)