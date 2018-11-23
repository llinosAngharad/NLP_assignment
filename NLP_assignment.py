from os import listdir
from os.path import isfile, join
import nltk
import nltk.data

my_path = "/Users/AppleUser/Documents/uni/comp_sci/Year2/NLP1/assignment/data/training"
corpus_root = "/Users/AppleUser/nltk_data/corpora/NLP_assignment"
onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
directory = os.fsencode(my_path)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        print(filename)

