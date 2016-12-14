import csv
from pprint import pprint
import pickle
import numpy as np

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    asdfasdf = load_obj("movieDict")
    pprint(asdfasdf)