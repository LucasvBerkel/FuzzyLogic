import csv
import pickle

from content_based import main as content_based
from collabr_filter import main as collabr_filter
from content_based import mainSolo as content_based_solo
from collabr_filter import main as collabr_filter

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
		
def testeval(user, arrayofdics, movieDict, method):
	
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
    if(method == "all"):
        print("Get collaborative filtering recommendations...")
        collabrDict = collabr_filter(user, arrayofdics)
        print("Get content-based recommendations...")
        contentDict = content_based(user, movieDict, collabrDict)
    elif(method == "content_based"):
        print("Get content-based recommendations...")
        contentDict = content_based_solo(user, movieDict)
    elif(method == "collaborative_filtering"):
        print("Get collaborative filtering recommendations...")
        collabrDict = collabr_filter(user, arrayofdics)

    print("")
    confidenceMovies = []
    confidenceDict={}
    if(method == "all"):
    	for key in collabrDict:
    		if key in contentDict:
    			confidence = float(collabrDict[key])*float(contentDict[key])
    			confidenceMovies.append([key, confidence])
    			confidenceDict[key] = confidence + 1
    elif(method == "content_based"):
    	for key in contentDict:
            confidence = float(contentDict[key])
            confidenceMovies.append([key, confidence])
            confidenceDict[key] = confidence
    elif(method == "collaborative_filtering"):
    	for key in collabrDict:
            confidence = float(collabrDict[key])
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
