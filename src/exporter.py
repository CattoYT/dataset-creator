from pathlib import Path
import os
import shutil
import utils
from session import session
from huggingface_format import create_parquet


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


class Exporter:
    def __init__(self, export_type="Parquet"):
        self.dataset_name = session["Dataset name"]
        self.export_type = export_type  # Accept "Parquet", "LJSpeech", "VCTK", "Multi-Speaker-HF" idk #TODO Check chatterbox format, gptsovits format, and whatever the chinese are using rn idfk lmao
        self.dataset_format = session["Dataset format"]
        self.data_path = session["Path"]

    def move_for_processing(self):
        with open(
            f"{self.dataset_name}/good.txt", "r"
        ) as f:  # todo: manage processed.txt whenever i get round to that
            data = f.readlines()

            if self.export_type == "Parquet" and self.dataset_format == "Ai Hobbyist":
                os.mkdir(f"output/{self.dataset_name}")
                for file_path in data:
                    file_path = file_path.strip()

                    shutil.copyfile(
                        file_path,
                        f"output/{self.dataset_name}/{os.path.basename(file_path)}",
                    )  # copy wav
                    shutil.copyfile(
                        file_path.replace(".wav", ".lab"),
                        f"output/{self.dataset_name}/{os.path.basename(file_path.replace('.wav', '.lab'))}",
                    )  # TODO: test if i should leave it as .lab or .txt, its both rawtext just naming convention sdhit

    def export_as_parquet(self):
        self.generate_list_file()
        create_parquet(f"output/{self.dataset_name}.list")

    """
    ok so basically all of the list files will be saved to "output/" and the datasets actual formatted data will be in output/{character}
    the final datasets ig can be saved to exports/ which is where the legacy code saves it and i cba to change it
    only for this format tho
    for like ljspee
    """

    def generate_list_file(self):
        print("creating list")
        language = session["Language"]
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
        for file in iter_files(f"output/{self.dataset_name}", ".lab"):
            text = open(file, "r").read()
            if "{" in text or "}" in text:  # cehck if placehgoldewers are presnet
                continue

            # if text.count(" ") < 2:  # check if its long enough to be ok
            #     continue

            wav_path = file.replace(".lab", ".wav")
            print(wav_path)
            total_duration += utils.get_wav_length(wav_path)

            data_lines.append(
                Data(
                    Path("output/" + wav_path).as_posix(),
                    self.dataset_name,
                    language,
                    text,
                )
            )

        with open(f"output/{self.dataset_name.lower()}.list", "w") as f:
            for i in data_lines:
                f.write(i.output() + "\n")

        print(f"Total duration: {total_duration:.2f} seconds")
