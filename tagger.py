import re
import os.path
from dateutil import parser as time_parser


def tag_all(filename, text, start_time, end_time, location, speaker):
    print(filename, start_time, end_time, location, speaker)
    text = tag_time(text, start_time, end_time)
    text = tag_location(text, location)
    text = tag_speaker(text, speaker)
    tag_paragraphs(text)
    write_file(filename, text)
    return text

# Tags location every time it is found in text
def tag_location(text, location):
    new_text = text
    if location is not None:
        new_text = re.sub(re.escape(location), "<location>"+location+"</location>", text)
    return new_text

def tag_paragraphs(text):
    text = "\n\n{}\n\n".format(text.split("\n"))
    print(text)

# Tags speaker every time it is found in text
def tag_speaker(text, speaker):
    new_text = text
    if speaker is not None:
        new_text = re.sub(re.escape(speaker), "<speaker>" + speaker + "</speaker>", text)
    return new_text

# Tags both the start and end time every time they're found in text
def tag_time(text, start_time, end_time):
    new_text = text
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
                new_text = re.sub(item, "<stime>" + item + "</stime>", text)  # Search and replace start time with tags

    # Tag end_time, if it exists
    if end_time is not None:
        end_time = time_parser.parse(end_time).time()   # Convert end time to universal datetime
        for x in time_set:
            datetime = time_parser.parse(x).time()   # Convert time found in text to universal datetime
            if datetime == end_time:
                new_text = re.sub(x, "<etime>" + x + "</etime>", new_text)  # Search and replace end time with tags
    return new_text

# Writes text to a .txt file
def write_file(filename, text):
    save_path = "/Users/AppleUser/Documents/gitHub/NLP_assignment/out/"
    complete_filename = os.path.join(save_path, filename)

    file = open(complete_filename, "w")
    file.write(text)

    file.close()

