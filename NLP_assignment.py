import os
import re

training_path = os.getcwd() + "/data/training/"
training_directory = os.fsencode(training_path)

test_tagged_path = os.getcwd() + "/data/test/test_tagged"
test_untagged_path = os.getcwd() + "/data/test/test_untagged"

txtfiles = []
training_texts = []


# Reads training data and creates a list of each .txt file's contents
def read_training_data(path, directory):
    counter = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                txtfiles.append(str(filename))
                counter += 1

                text_file = open(path + filename, "r", encoding="utf8")
                text = text_file.read()
                training_texts.append(text)
                text_file.close()

        except Exception as e:
            raise e
            print("No files found here!")


# Creates a set of 'known' speakers that appear in the tagged emails
def find_known_speakers():
    speaker_set = set()
    speaker_pattern = r"<speaker>(?:Dr|Mr|Ms|Mrs|Prof|Sir|Professor)?\.?\s?([a-zA-Z ]+),?\s?(?:PhD)?<\/speaker>"
    for text in training_texts:
        for line in text:
            line = line.lower()
            speaker = re.findall(speaker_pattern, line, flags=re.DOTALL)
            for person in speaker:
                if speaker: speaker_set.add(person)
    return speaker_set

# Creates a set of 'known' locations that appear in the tagged emails
def find_known_locations():
    location_set = set()
    location_pattern = r"<location>([a-zA-Z0-9 ]+)</location>"
    for text in training_texts:
        for line in text:
            line = line.lower()
            location = re.findall(location_pattern, line, flags=re.DOTALL)
            for place in location:
                if place: location_set.add(place)
    return location_set

# Splits texts into header and body
def split_text(text_list):
    for text in text_list:
        text = text.lower()

        i = text.index("abstract:")
        body = text[i:]
        header = text[:i]

        new_header = "~~~~~~~~~~~~~~~~~~~~~~\nHEADER\n"
        new_header += header

        new_body = "\nBODY\n"
        new_body += body

        new_text = new_header + new_body
        print(new_text)

def main():
    read_training_data(training_path, training_directory)
    # print(find_known_speakers())
    # print(find_known_locations())
    split_text(training_texts)

main()