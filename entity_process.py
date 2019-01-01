import re
import os
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize

speaker_set = set()
location_set = set()

def clean_speaker(speaker):
    """
    Remove punctuation and symbols from speaker name
    :param speaker: name of speaker
    :return: clean speaker name
    """
    speaker = re.sub(", .*", "", speaker)
    speaker = re.sub(" / .*", "", speaker)
    speaker = re.sub("-.*", "", speaker)
    speaker = re.sub(r"\([^()]*\)", "", speaker)
    return speaker

def extract_time(header):
    """
    Finds and extracts a start time and end time (if it exists) from a text
    :param header: header of the text
    :return: start time and end time
    """
    time_pattern = r"(?:time:)\s*((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    time = re.search(time_pattern, header, flags=re.DOTALL)
    if time:
        start_time = time.group(1)
        end_time = time.group(2)
        return start_time, end_time
    else: return None, None

def extract_location(header_array, body):
    """
    Finds and extracts location from a text
    :param header_array: array of each line in the text header
    :param body: body of the text
    :return: location
    """
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
    # otherwise use NER to find
    if location is None:
        for line in body_array:
            for sent in sent_tokenize(line):
                for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                    if hasattr(chunk, 'label'):
                        if chunk.label() == "GPE":
                            loc = ' '.join(c[0] for c in chunk)
                            location = loc
    return location

def extract_speaker(header_array, body):
    """
    Finds and extracts a speaker from a text
    :param header_array: array of each line in the text header
    :param body: body of the text
    :return: speaker
    """
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
    if speaker is None:
        for line in body_array:
            for sent in sent_tokenize(line):
                for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                    if hasattr(chunk, 'label'):
                        if chunk.label() == "PERSON":
                            sp = ' '.join(c[0] for c in chunk)
                            speaker = clean_speaker(sp)
    return speaker

def find_known_speakers(text):
    """
    Creates a set of 'known' speakers that appear in the tagged emails
    :param text: text to extract speakers from
    :return: set of speakers
    """
    speaker_pattern = r"<speaker>(?:Dr|Mr|Ms|Mrs|Prof|Sir|Professor)?\.?\s?([a-zA-Z ]+),?\s?(?:PhD)?<\/speaker>"
    speaker = re.findall(speaker_pattern, text, flags=re.DOTALL)
    for person in speaker:
        if speaker and len(person.split())>1:
            speaker_set.add(person)
    return speaker_set

def find_known_locations(text):
    """
    Creates a set of 'known' locations that appear in the tagged emails
    :param text: text to extract locations from
    :return: set of locations
    """
    location_pattern = r"<location>([a-zA-Z0-9 ]+)</location>"
    location = re.findall(location_pattern, text, flags=re.DOTALL)
    for place in location:
        if place: location_set.add(place)
    return location_set

def process_training():
    """
    Process the training data to extract known speakers and locations
    """
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

def read_data(path, file):
    """
    Reads data and creates a list of each .txt file's contents
    :param path: path of the data
    :param file: file that contains the data
    :return: the file's content
    """
    filename = os.fsdecode(file)
    text_file = open(path + filename, "r", encoding="utf8")
    text = text_file.read()
    text_file.close()
    return text

def split_text(text):
    """
    Splits texts into header and body
    :param text: text to split
    :return: header and body of text
    """
    if "abstract:" in text:
        i = text.index("abstract:")
        header = text[:i]
        body = text[i:]
        return header, body
    else:
        header = text
        body = text
        return header, body