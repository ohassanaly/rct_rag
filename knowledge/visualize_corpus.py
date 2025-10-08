import json
from config import *
import pickle
import re

with open(corpus_path, "rb") as fp:
    corpus = pickle.load(fp)

print(len(corpus))
print(corpus)

