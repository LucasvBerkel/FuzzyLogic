import os
import csv

files = os.listdir("training_set_with_old_reviews")
fileName = "movie_Titles_with_Genres.csv"

counterM = 0
counterA = 0

filesA = []

with open(fileName, 'r') as f:
	csvFile = csv.reader(f, delimiter=',', quotechar='|')	
	for row in csvFile:
		name = "mv_" + row[0].zfill(7) + ".txt"
		filesA.append(name)
	for fileName in files:
		if fileName in filesA:
			counterA += 1
		else:
			counterM += 1
			os.remove("training_set/" + fileName)

print ("Missing files: " + str(counterM))
print ("Attended files: " + str(counterA))	