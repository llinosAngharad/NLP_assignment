import re
import os.path
from dateutil import parser as time_parser
from nltk import sent_tokenize


def tag_all(filename, text, start_time, end_time, location, speaker):
    """
    Calls all tagging methods
    :param filename: name of the file
    :param text: text to be tagged
    :param start_time: start time to tag
    :param end_time: end time to tag
    :param location: location to tag
    :param speaker: speaker to tag
    :return: tagged text
    """
    text = tag_time(text, start_time, end_time)
    text = tag_location(text, location)
    text = tag_speaker(text, speaker)
    text = tag_paragraphs(text)
    text = tag_sentences(text)
    write_file(filename, text)
    return text

def tag_location(text, location):
    """
    Tags location every time it is found in text
    :param text: text to be tagged
    :param location: location to tag
    :return: tagged text
    """
    if location is not None:
        # Add the tags
        text = re.sub(re.escape(location), "<location>"+location+"</location>", text)
    return text

def tag_paragraphs(text):
    """
    Tags paragraphs in text
    :param text: text to be tagged
    :return: tagged text
    """
    text = "\n\n{}\n\n".format(text.strip("\n"))
    paragraph_regex = r"(?<=\n\n)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\n\n)"

    for match in re.finditer(paragraph_regex, text):
        paragraph = match.group(1)
        if paragraph:
            # Add the tags
            text = re.sub(re.escape(paragraph), "<paragraph>"+paragraph+"</paragraph>", text)
    return text.strip()

def tag_sentences(text):
    """
    Tags sentences in text
    :param text: text to be tagged
    :return: tagged text
    """
    # Create a list of paragraphs found in text
    text_paragraphs = re.split(r"</?paragraph>", text)
    sentences_list = []

    # For every paragraph in text, find the sentences and add them to the list of sentences
    for para in text_paragraphs:
        para = para.strip()
        sentences_list.extend(sent_tokenize(para))

    # Filter out everything that's not a sentence
    not_sentence_regex = r"^[A_Za-z0-9](?:.|\n)+(?:\.|\?|!|:)$"
    sentences_list = list(filter(lambda x: re.match(not_sentence_regex, x), sentences_list))
    # Add the tags
    for sent in sentences_list:
        text = re.sub(re.escape(sent), "<sentence>"+sent+"</sentence>", text)
    return  text

def tag_speaker(text, speaker):
    """
    Tags speaker every time it is found in text
    :param text: text to be tagged
    :param speaker: speaker to tag in text
    :return: tagged text
    """
    if speaker is not None:
        # Add the tags
        text = re.sub(re.escape(speaker), "<speaker>" + speaker + "</speaker>", text)
    return text

def tag_time(text, start_time, end_time):
    """
    Tags both the start and end time every time they're found in text
    :param text: text to be tagged
    :param start_time: start time to tag
    :param end_time: end time to tag
    :return: tagged text
    """
    # Extract all instances of time from the text and add them to a set
    time_pattern = r"((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    times = re.findall(time_pattern, text)
    time_set = set()
    for x in times:
        if x[0] != "":
            time_set.add(x[0].strip("\n"))
        if x[1] != "":
            time_set.add(x[1].strip("\n"))

    # Tag start_time
    if start_time is not None:
        start_time = time_parser.parse(start_time).time()   # Convert start time to universal datetime
        # For every time found in the text
        for item in time_set:
            datetime = time_parser.parse(item).time()   # Convert time found in text to universal datetime
            if datetime == start_time:
                text = re.sub(item, "<stime>" + item + "</stime>", text)  # Search and replace start time with tags

    # Tag end_time, if it exists
    if end_time is not None:
        end_time = time_parser.parse(end_time).time()   # Convert end time to universal datetime
        for x in time_set:
            datetime = time_parser.parse(x).time()   # Convert time found in text to universal datetime
            if datetime == end_time:
                text = re.sub(x, "<etime>" + x + "</etime>", text)  # Search and replace end time with tags
    return text

def write_file(filename, text):
    """
    Writes text to a .txt file
    :param filename: name of the file to be written
    :param text: text to be written to file
    """
    save_path = "/Users/AppleUser/Documents/gitHub/NLP_assignment/out/"
    complete_filename = os.path.join(save_path, filename)

    file = open(complete_filename, "w")
    file.write(text)

    file.close()

