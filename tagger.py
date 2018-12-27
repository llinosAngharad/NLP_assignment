import re


def tag_all(filename, text, start_time, end_time, location, speaker):
    print(location)
    text = tag_start_time(text, start_time)
    text = tag_end_time(text, end_time)
    text = tag_location(text, location)
    # tag_speaker(speaker)
    return text

def tag_start_time(text, start_time):
    if start_time is not None:
        text = re.sub(start_time, "<stime>"+start_time+"</stime>", text)
    return text

def tag_end_time(text, end_time):
    if end_time is not None:
        text = re.sub(end_time, "<etime>"+end_time+"</etime>", text)
    return text

def tag_location(text, location):
    if location is not None:
        text = re.sub(location, "<location>"+location+"</location>", text)
    return text