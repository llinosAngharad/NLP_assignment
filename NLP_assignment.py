import os
import re

# Reads training data and creates a list of each .txt file's contents
def read_data(path, file):
    filename = os.fsdecode(file)
    text_file = open(path + filename, "r", encoding="utf8")
    text = text_file.read()
    text_file.close()
    return text


# Creates a set of 'known' speakers that appear in the tagged emails
def find_known_speakers(text, speaker_set):
    speaker_pattern = r"<speaker>(?:Dr|Mr|Ms|Mrs|Prof|Sir|Professor)?\.?\s?([a-zA-Z ]+),?\s?(?:PhD)?<\/speaker>"
    speaker = re.findall(speaker_pattern, text, flags=re.DOTALL)
    for person in speaker:
        if speaker: speaker_set.add(person)
    return speaker_set

# Creates a set of 'known' locations that appear in the tagged emails
def find_known_locations(text, location_set):
    location_pattern = r"<location>([a-zA-Z0-9 ]+)</location>"
    location = re.findall(location_pattern, text, flags=re.DOTALL)
    for place in location:
        if place: location_set.add(place)
    return location_set

# Splits texts into header and body
def split_text(text):
    if "abstract:" in text:
        i = text.index("abstract:")
        header = text[:i]
        body = text[i:]
        return header, body
    else:
        return "abstract not in text", text

def extract_time(header):
    time_pattern = r"(?:time:)\s*((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    time = re.search(time_pattern, header, flags=re.DOTALL)
    if time:
        start_time = time.group(1)
        end_time = time.group(2)
        return start_time, end_time
    else: return None, None

def extract_location(header_array, body_array):
    location = None
    # check if a location was found in the header, if it was return it
    for line in header_array:
        loc_pattern = r"(?:place:)\s*(.*)"
        loc = re.search(loc_pattern, line, flags=re.DOTALL)
        if loc:
            location = loc.group(1)
            return location
    if location is None:
        for line in body_array:
            loc_pattern = r"(?:place:|)\s*(.*)"
            loc = re.search(loc_pattern, line, flags=re.DOTALL)
            if loc:
                location = loc.group(1)
                return location






def out(txt_files):
    for file in txt_files:
        print(file)
        complete_name = os.path.join(os.getcwd() + "/out/", file)
        w_file = open(complete_name, "w")
        w_file.write("Hello testing!\n" + complete_name)
        w_file.write()
        w_file.close()

def process_training():
    training_path = os.getcwd() + "/data/training/"
    training_directory = os.fsencode(training_path)
    speaker_set = set()
    location_set = set()

    for file in os.listdir(training_directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                text = read_data(training_path, file)
                text = text.lower()
                speaker_set = find_known_speakers(text, speaker_set)
                location_set = find_known_locations(text, location_set)
                header,body = split_text(text)
        except Exception as e:
            raise e
            return "No files found here!"

def process_test_tagged():
    test_tagged_path = os.getcwd() + "/data/test/test_tagged/"
    test_tagged_directory = os.fsencode(test_tagged_path)

    for file in os.listdir(test_tagged_directory):
        text = read_data(test_tagged_path, file)

def process_test_untagged():
    test_untagged_path = os.getcwd() + "/data/test/test_untagged/"
    test_untagged_directory = os.fsencode(test_untagged_path)

    for file in os.listdir(test_untagged_directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                text = read_data(test_untagged_path, file)
                text = text.lower()
                header,body = split_text(text)
                header_array = header.splitlines()
                body_array = body.splitlines()

                start_time, end_time = extract_time(header)

                location = extract_location(header_array, body_array)
                print(header_array)
                print(location)

        except Exception as e:
            raise e
            return "No files found here!"

process_test_untagged()