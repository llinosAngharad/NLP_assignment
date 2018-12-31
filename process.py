import re
import os

speaker_set = set()
location_set = set()

def clean_speaker(speaker):
    speaker = re.sub(", .*", "", speaker)
    speaker = re.sub(" / .*", "", speaker)
    speaker = re.sub("-.*", "", speaker)
    speaker = re.sub(r"\([^()]*\)", "", speaker)
    return speaker

def extract_time(header):
    time_pattern = r"(?:time:)\s*((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    time = re.search(time_pattern, header, flags=re.DOTALL)
    if time:
        start_time = time.group(1)
        end_time = time.group(2)
        return start_time, end_time
    else: return None, None

def extract_location(header_array, body):
    location = None
    body_array = body.splitlines()
    loc_pattern = r"(?:place:|location:|where:)\s*(.*)"
    # check if a location was found in the header, if it was return it
    for line in header_array:
        loc = re.search(loc_pattern, line, flags=re.DOTALL)
        if loc:
            location = loc.group(1)
    # if location was not found in header, search body using regex
    if location is None:
        for line in body_array:
            loc = re.search(loc_pattern, line, flags=re.DOTALL)
            if loc:
                location = loc.group(1)
    # if location is still not found, check for known locations in body
    if location is None:
        for loc in location_set:
            if loc in body:
                location = loc
    return location

def extract_speaker(header_array, body):
    speaker = None
    body_array = body.splitlines()
    speaker_pattern = r"(?:who:|speaker:)\s*(.*)"

    # check if a speaker was found in the header, if it was return it
    for line in header_array:
        sp = re.search(speaker_pattern, line, flags=re.DOTALL)
        if sp:
            speaker = sp.group(1)
            speaker = clean_speaker(speaker)
    # if speaker was not found in header, search body using regex
    if speaker is None:
        for line in body_array:
            sp = re.search(speaker_pattern, line, flags=re.DOTALL)
            if sp:
                speaker = sp.group(1)
                speaker = clean_speaker(speaker)
    # if speaker is still not found, check for known speakers in body
    if speaker is None:
        for sp in speaker_set:
            sp_pattern = r"(" + sp + ")"
            for line in body_array:
                sp = re.search(sp_pattern, line, flags=re.DOTALL)
                if sp:
                    speaker = sp.group(1)
                    speaker = clean_speaker(speaker)
    return speaker

# Creates a set of 'known' speakers that appear in the tagged emails
def find_known_speakers(text):
    speaker_pattern = r"<speaker>(?:Dr|Mr|Ms|Mrs|Prof|Sir|Professor)?\.?\s?([a-zA-Z ]+),?\s?(?:PhD)?<\/speaker>"
    speaker = re.findall(speaker_pattern, text, flags=re.DOTALL)
    for person in speaker:
        if speaker and len(person.split())>1:
            speaker_set.add(person)
    return speaker_set

# Creates a set of 'known' locations that appear in the tagged emails
def find_known_locations(text):
    location_pattern = r"<location>([a-zA-Z0-9 ]+)</location>"
    location = re.findall(location_pattern, text, flags=re.DOTALL)
    for place in location:
        if place: location_set.add(place)
    return location_set

def process_training():
    training_path = os.getcwd() + "/data/training/"
    training_directory = os.fsencode(training_path)
    for file in os.listdir(training_directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                text = read_data(training_path, file)
                text = text.lower()
                find_known_speakers(text)
                find_known_locations(text)

        except Exception as e:
            raise e
            return "No files found here!"

# Reads training data and creates a list of each .txt file's contents
def read_data(path, file):
    filename = os.fsdecode(file)
    text_file = open(path + filename, "r", encoding="utf8")
    text = text_file.read()
    text_file.close()
    return text

# Splits texts into header and body
def split_text(text):
    if "abstract:" in text:
        i = text.index("abstract:")
        header = text[:i]
        body = text[i:]
        return header, body
    else:
        header = text
        body = text
        return header, body