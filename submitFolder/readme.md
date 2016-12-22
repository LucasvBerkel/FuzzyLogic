# The great fuzzy binge watch helper

This is a program to get, given user rating history and that history of similar users, movie/serie recommendations.
The basic idea behind the program is to combine a collaborative filtering method with a content-based method.

### The collaborative filtering method

The collaborative filtering method is a method that calculates similarity between users and uses users that are close to the original user as important hint if the user
likes an unseen movie. Because this is a program made in a fuzzy logic course, every users is weighted to the closest neighbour. If the second neighbour is double the distance
from the original user as the closest neighbour, then the rating of that user is considered as half important. This is adaption of fuzzy k-nearest neighbour. From the 
average rating retrieved from the neighbours, an estimation is made for the original user.

### The content-based method

The content-based method is a method that fills in the object of movies, giving it characteristics. This way, if a user structurally dislikes movies of the dramactic genre,
you can filter movies that would other way be recommended by the collaborative filtering method. In this program, the movie objects are filled in with genres retrieved from
the online imdb api. Following the sequence of genres, every genre is given an importance(or membership) to that movie. This way, not only which genres are selected are important,
also the sequence of those genres. From there the program compares the unseen movie with previous rated movies, if the user liked a similar movie, it would return a favourable
confidence for this unseen movie.

### Combining them

Studies have shown that collaborative filtering produces the best recommendations. Given this fact, our program retrieves the recommendations of this method and cross validates
them with the confidence scores retrieved from the content-based method. If the content-based method did not give a high confidence score for the unseen movie, the recommendation
is heavily penatilized.

### Folder overview

This folder containes multiple files with each a own purpose, a quick overview:
- collabr_filter.py: python script to calculate recommendation list using collaborative filtering.
- content_based.py: python script to calculate recommendation confidence scores using the content-based method
- eval.py: python script which evaluates the overall scores of both methods and the combination of both
- getRecomsOnly.py: python script to get a top 20 recommendation list using the combinated method(most practical script).
- getRecoms.py: python script which get individual recommendation lists queried in eval.py, used for evaluating the program.
- movieDictNames.pkl: pickle file which stores a python dictionary which has the movie-id's as key, with the corresponding name as value
- movieDict.pkl: pickle file which stores a python dictionary which has the movie-id's as key, with the corresponding fuzzy genre array as value