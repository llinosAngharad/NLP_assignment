import re
from dateutil import parser as time_parser

def tag_all(filename, text, start_time, end_time, location, speaker):
    print(filename, start_time, end_time, location, speaker)
    text = tag_time(text, start_time, end_time)
    text = tag_location(text, location)
    text = tag_speaker(text, speaker)
    return text

# Function to tag both the start and end time
def tag_time(text, start_time, end_time):
    # Extract all instances of time from the text and add them to a set
    time_pattern = r"((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    times = re.findall(time_pattern, text)
    time_set = set()
    for x in times:
        if x[0] != "":
            time_set.add(x[0].lower().replace(" ", "").strip("\n"))
        if x[1] != "":
            time_set.add(x[1].lower().replace(" ", "").strip("\n"))

    # Tag start_time
    if start_time is not None:
        start_time = time_parser.parse(start_time).time()   # Convert start time to universal datetime
        # For every time found in the text
        print(time_set)
        for x in time_set:
            datetime = time_parser.parse(x).time()   # Convert time found in text to universal datetime
            if datetime == start_time:
                text = re.sub(x, "<stime>" + x + "</stime>", text)  # Search and replace start time with tags

    # Tag end_time, if it exists
    if end_time is not None:
        end_time = time_parser.parse(end_time).time()   # Convert end time to universal datetime
        for x in time_set:
            datetime = time_parser.parse(x).time()   # Convert time found in text to universal datetime
            if datetime == end_time:
                text = re.sub(x, "<etime>" + x + "</etime>", text)  # Search and replace end time with tags

    return text

def tag_location(text, location):
    if location is not None:
        text = re.sub(re.escape(location), "<location>"+location+"</location>", text)
    return text

def tag_speaker(text, speaker):
    if speaker is not None:
        text = re.sub(re.escape(speaker), "<speaker>" + speaker + "</speaker>", text)
    return text

