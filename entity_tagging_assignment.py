import os
import entity_tagger
import entity_process

def process_test_tagged():
    test_tagged_path = os.getcwd() + "/data/test/test_tagged/"
    test_tagged_directory = os.fsencode(test_tagged_path)

    for file in os.listdir(test_tagged_directory):
        text = entity_process.read_data(test_tagged_path, file)

def extract_and_tag_test():
    """
    Extract times, speaker & location from text. Tag these & sentences/paragraphs
    """
    test_untagged_path = os.getcwd() + "/data/test/test_untagged/"
    test_untagged_directory = os.fsencode(test_untagged_path)

    print("Tagging text. Please wait...")
    for file in os.listdir(test_untagged_directory):
        filename = os.fsdecode(file)
        try:
            if filename.endswith(".txt"):
                text = entity_process.read_data(test_untagged_path, file)
                text = text.lower()
                header,body = entity_process.split_text(text)
                header_array = header.splitlines()


                start_time, end_time = entity_process.extract_time(header)
                location = entity_process.extract_location(header_array, body)
                speaker = entity_process.extract_speaker(header_array, body)

                entity_tagger.tag_all(filename, text, start_time, end_time, location, speaker)
        except Exception as e:
            raise e
            return "No files found here!"
    print("Tagging complete! Text saved to" + os.getcwd() + "/out")

entity_process.process_training()
extract_and_tag_test()