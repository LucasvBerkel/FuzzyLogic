import getRecoms
import os
path = "C:\\Users\\Joris\\Dropbox\\fuzzy\\fuzzycomb\\training_set_tiny_part/"
files = os.listdir(path)

import numpy as np


counter = 0
for filename in files:
	counter = counter + getRecoms.testeval(filename.split('.')[0])
	print('total is ', counter)