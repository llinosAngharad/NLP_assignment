import os
import re
import tagger
import ner
import process

def process_test_tagged():
    test_tagged_path = os.getcwd() + "/data/test/test_tagged/"
    test_tagged_directory = os.fsencode(test_tagged_path)

    for file in os.listdir(test_tagged_directory):
        text = process.read_data(test_tagged_path, file)

def extract_and_tag_test():
    test_untagged_path = os.getcwd() + "/data/test/test_untagged/"
    test_untagged_directory = os.fsencode(test_untagged_path)

    for file in os.listdir(test_untagged_directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                text = process.read_data(test_untagged_path, file)
                text = text.lower()
                header,body = process.split_text(text)
                header_array = header.splitlines()

                start_time, end_time = process.extract_time(header)
                location = process.extract_location(header_array, body)
                speaker = process.extract_speaker(header_array, body)

                tagger.tag_all(filename, text, start_time, end_time, location, speaker)

        except Exception as e:
            raise e
            return "No files found here!"

process.process_training()
extract_and_tag_test()