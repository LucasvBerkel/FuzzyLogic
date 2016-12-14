import os
import argparse
import csv
import re
import json

if __name__ == "__main__":
    fileName = "movie_Titles_with_Genres.csv"
    newFileName = "movie_Titles_with_Genres_Fixed.csv"
    files = os.listdir("../newDataset/training_set")
    counter = 1
    genreList = []
    with open(fileName, 'r') as f:
        a = csv.reader(f, delimiter=",")
        with open(newFileName, 'w') as fw:
            b = csv.writer(fw, delimiter=",")
            for row in a:
                name = "mv_" + row[0].zfill(7) + ".txt"
                if(name in files):
                    if len(row)>4:
                        row = [row[0], row[1], ",".join(row[2:-1]),row[-1]]
                    b.writerow(row)
        fw.close()
    f.close()
            # with open('newMovie_Titles.csv', 'w') as fp:
        #     a = csv.writer(fp, delimiter=',')

        #     for row in f:
        #         movieTitle = row.replace("\n", "").split(",")[2]
        #         print counter
        #         print movieTitle
        #         request = Request('http://www.omdbapi.com/?t=' +
        #                           quote(movieTitle) +
        #                           '&y=&plot=short&r=json')
        #         newData = row.replace("\n", "").split(",")
        #         try:
        #             response = urlopen(request)
        #             kittens = response.read()
        #             d = json.loads(kittens)
        #             if d['Response'] == "True":
        #                 print d['Genre']
        #                 genres = d['Genre'].encode('UTF8')
        #                 newData.append(genres)
        #                 newFile.append(newData)
        #                 a.writerow(newData)
        #         except URLError, e:
        #             print 'No kittez. Got an error code:', e
        #         counter += 1

    # with open('newMovie_Titles2.csv', 'w') as fp:
    #     a = csv.writer(fp, delimiter=',')
    #     a.writerows(newFile)    