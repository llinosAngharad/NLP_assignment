import re
from dateutil import parser as time_parser

def tag_all(filename, text, start_time, end_time, location, speaker):
<<<<<<< HEAD
    text = tag_time(text, start_time, end_time)
=======
    print(filename)
    text = tag_start_time(text, start_time)
    text = tag_end_time(text, end_time)
>>>>>>> parent of d57c1a1... tagging update
    text = tag_location(text, location)
    text = tag_speaker(text, speaker)
    return text

def tag_start_time(text, start_time):
    time_pattern = r"((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)\s?-?\s?((?:\d{1,2}:\d{2})\s?(?:am|pm|AM|PM|a\.m\.|p\.m\.)?)?"
    times = re.findall(time_pattern, text)
    time_set = set()
    for x in times:
        if x[0] != "":
            time_set.add(x[0])
        if x[1] != "":
            time_set.add(x[1])
            
    if start_time is not None:
<<<<<<< HEAD
        start_time = time_parser.parse(start_time).time()   # Convert start time to universal datetime
        # For every time found in the text
=======
        start_time = time_parser.parse(start_time).time()

>>>>>>> parent of d57c1a1... tagging update
        for x in time_set:
            time = x.lower().replace(" ", "")
            datetime = time_parser.parse(time).time()

            if datetime == start_time:
                text = re.sub(x, "<stime>" + x + "</stime>", text)
    return text

def tag_end_time(text, end_time):
    if end_time is not None:
<<<<<<< HEAD
        end_time = time_parser.parse(end_time).time()   # Convert end time to universal datetime
        for x in time_set:
            datetime = time_parser.parse(x).time()   # Convert time found in text to universal datetime
            if datetime == end_time:
                text = re.sub(x, "<etime>" + x + "</etime>", text)  # Search and replace end time with tags
    print(text)
=======
        text = re.sub(re.escape(end_time), "<etime>"+end_time+"</etime>", text)
        end_time = end_time.replace(" ", "")
        text = re.sub(re.escape(end_time), "<etime>" + end_time + "</etime>", text)
>>>>>>> parent of d57c1a1... tagging update
    return text

def tag_location(text, location):
    if location is not None:
        text = re.sub(re.escape(location), "<location>"+location+"</location>", text)
    return text

def tag_speaker(text, speaker):
    if speaker is not None:
        text = re.sub(re.escape(speaker), "<speaker>" + speaker + "</speaker>", text)
    return text

