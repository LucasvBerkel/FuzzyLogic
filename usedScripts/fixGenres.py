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