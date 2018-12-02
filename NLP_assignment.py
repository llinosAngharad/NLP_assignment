import os

mypath = os.getcwd() + "/data/training/"
directory = os.fsencode(mypath)
counter = 0
txtfiles = []
training_texts = []



for file in os.listdir(directory):
    filename = os.fsdecode(file)
    try:
        if filename.endswith(".txt"):
            txtfiles.append(str(filename))
            counter += 1

            text_file = open(mypath + filename, "r", encoding="utf8")
            text = text_file.readlines()
            training_texts.append(text)
            text_file.close()

    except Exception as e:
        raise e
        print("No files found here!")

for text in training_texts:
    