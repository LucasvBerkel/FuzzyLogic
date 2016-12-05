import os
import argparse
import csv
import re
import json

from urllib2 import Request, urlopen, URLError
from urllib import quote

if __name__ == "__main__":
    fileName = "movie_titles.txt"
    counter = 1
    newFile = []
    with open(fileName, 'r') as f:
        with open('newMovie_Titles.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')

            for row in f:
                movieTitle = row.replace("\n", "").split(",")[2]
                print counter
                print movieTitle
                request = Request('http://www.omdbapi.com/?t=' +  quote(movieTitle) + '&y=&plot=short&r=json')
                newData = row.replace("\n", "").split(",")
                try:
                    response = urlopen(request)
                    kittens = response.read()
                    d = json.loads(kittens)
                    if d['Response'] == "True":
                        print d['Genre']
                        genres = d['Genre'].encode('UTF8')
                        newData.append(genres)
                        newFile.append(newData)
                        a.writerow(newData)
                except URLError, e:
                    print 'No kittez. Got an error code:', e
                counter += 1

    with open('newMovie_Titles2.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(newFile)



    # with open('newSmoelenboek.csv', 'w') as fp:
    #     a = csv.writer(fp, delimiter=',')
    #     a.writerows(newFile)

    # os.system("ren " + path + "\\" + file_name + " " + new_file_name)
