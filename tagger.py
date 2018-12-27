import re
from dateutil import parser as time_parser

def tag_all(filename, text, start_time, end_time, location, speaker):
    print(filename)
    text = tag_start_time(text, start_time)
    text = tag_end_time(text, end_time)
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
        start_time = time_parser.parse(start_time).time()

        for x in time_set:
            time = x.lower().replace(" ", "")
            datetime = time_parser.parse(time).time()

            if datetime == start_time:
                text = re.sub(x, "<stime>" + x + "</stime>", text)
    return text

def tag_end_time(text, end_time):
    if end_time is not None:
        text = re.sub(re.escape(end_time), "<etime>"+end_time+"</etime>", text)
        end_time = end_time.replace(" ", "")
        text = re.sub(re.escape(end_time), "<etime>" + end_time + "</etime>", text)
    return text

def tag_location(text, location):
    if location is not None:
        text = re.sub(re.escape(location), "<location>"+location+"</location>", text)
    return text

def tag_speaker(text, speaker):
    if speaker is not None:
        text = re.sub(re.escape(speaker), "<speaker>" + speaker + "</speaker>", text)
    return text

