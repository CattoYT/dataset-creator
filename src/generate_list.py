import utils
import os

# this is used for huggingface format


class Data:
    def __init__(self, path, character, language, text):
        self.path = path
        self.character = character
        self.language = language
        self.text = text

    def output(self):
        return f"{self.path}|{self.character}|{self.language}|{self.text}"


def iter_files(directory, extension):  # bro i only noticed this was here just now XDDDD
    # TODO: move this to utils and refactor
    # RECURSIVE BTW
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)


def generate_list_file(character=None, language=None):
    if character is None:
        character = input("Character pls: ")  # legacy jargon, too lazy to do properly

    if language is None:
        language = input("""Provide language
        'zh': Chinese
        'ja': Japanese
        'en': English
        'ko': Korean
        'yue': Cantonese
        > """)
    if language not in ["zh", "ja", "en", "ko", "yue"]:
        print("Invalid language code.")
        exit(1)

    data_lines = []
    total_duration = 0.0

    # TODO: fix this entire file honeslty
    for file in iter_files(f"output/{character}", ".lab"):
        text = open(file, "r").read()
        if "{" in text or "}" in text:  # cehck if placehgoldewers are presnet
            continue

        # if text.count(" ") < 2:  # check if its long enough to be ok
        #     continue

        wav_path = file.replace(".lab", ".wav")
        total_duration += utils.get_wav_length(wav_path)
        data_lines.append(Data(wav_path, character, language, text))

    with open(f"{character.lower()}.list", "w") as f:
        for i in data_lines:
            f.write(i.output() + "\n")
    print(f"Total duration: {total_duration:.2f} seconds")
