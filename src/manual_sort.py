import os
import subprocess
import threading
import time
import keyboard  # pip install keyboard
import utils
import math
import editor


class ManualSorter:  # honestly have no idea if this is the best way to do it, then again havent written python in ages soooo
    def status(self, file_path):
        print(
            f"Remaining files: {self.progress_max - int(len(self.good) + len(self.bad))} files ({self.progress}% Completed)"
        )

        print(
            f"Total duration of good files: {self.total_good_length:.2f}s + {self.current_wav_length:.2f}s"
        )
        print(
            f"Total duration of bad files: {self.total_bad_length:.2f}s + {self.current_wav_length:.2f}s"
        )
        print("W -> Good\nE -> Bad\nR -> Edit Transcription\nX -> Quit\n")

        try:
            transcription = open(file_path.replace(".wav", ".lab")).read()
        except FileNotFoundError:
            try:
                transcription = open(file_path.replace(".wav", ".txt")).read()
            except FileNotFoundError:
                match input(
                    "Transcript couldn't be found! Would you like to run parkeet/whisper on this file? <y/n>"
                ):
                    case "y":
                        # TODO: Run parkeet
                        raise NotImplementedError
                    case "n":
                        transcription = "Missing transcription"  # TODO: idk if i should terminate or just continue but il figure that out later

        print(f'Transcription:\n"{transcription}"')

    def prompt_new_wav(self, file_path: str):
        stop_flag = {"stop": False}

        self.current_wav_length = utils.get_wav_length(file_path)
        self.progress = round(
            int((len(self.good)) + len(self.bad)) / self.progress_max, 2
        )

        self.status(file_path)

        def check_keys():
            import sys

            if os.name == "nt":
                import msvcrt

                def _get_key():
                    if msvcrt.kbhit():
                        return msvcrt.getwch()
                    return None

                def _restore():
                    pass

            # TODO: Unix stuff + this func is cgpt'd, no clue how this shit works
            # else:
            #     import tty
            #     import termios
            #     import select

            #     fd = sys.stdin.fileno()
            #     old_attrs = termios.tcgetattr(fd)
            #     tty.setcbreak(fd)

            #     def _get_key():
            #         dr, _, _ = select.select([sys.stdin], [], [], 0)
            #         if dr:
            #             return sys.stdin.read(1)
            #         return None

            #     def _restore():
            #         termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)

            try:
                while not stop_flag["stop"] and not self.exit_flag["exit"]:
                    key = _get_key()
                    if key:
                        key = key.lower()
                        if key == "w":
                            self.good.append(file_path)
                            self.good_files.write(f"{file_path}\n")
                            self.good_files.flush()
                            self.total_good_length += self.current_wav_length
                            stop_flag["stop"] = True
                            # wait until released
                            while _get_key() == "w":
                                time.sleep(0.1)

                        elif key == "e":
                            self.bad.append(file_path)
                            self.bad_files.write(f"{file_path}\n")
                            self.bad_files.flush()
                            self.total_bad_length += self.current_wav_length
                            stop_flag["stop"] = True
                            while _get_key() == "e":
                                time.sleep(0.1)

                        elif key == "r":
                            editor.edit_prompt(file_path.replace(".wav", ".lab"))
                            os.system("cls")
                            self.status(file_path)
                            while _get_key() == "r":
                                time.sleep(0.1)

                        elif key == "x":
                            self.exit_flag["exit"] = True
                            stop_flag["stop"] = True

                    time.sleep(0.01)
            finally:
                _restore()

        listener_thread = threading.Thread(target=check_keys)
        listener_thread.start()

        proc = subprocess.Popen(
            ["ffplay", "-autoexit", "-nodisp", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        while (
            proc.poll() is None and not stop_flag["stop"] and not self.exit_flag["exit"]
        ):
            time.sleep(0.01)

        if proc.poll() is None:
            proc.terminate()

        listener_thread.join()

    def main_sort_loop(self):
        from settings import settings

        self.progress_max = 0
        for _, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith(".wav"):
                    self.progress_max += 1

        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if not settings["Show History"]:
                    os.system("cls")
                if self.exit_flag["exit"]:
                    return "Requested Exit"
                if file.lower().endswith(".wav"):
                    file_path = os.path.normpath(os.path.join(root, file))
                    if file_path in self.good:
                        print(f"Skipping {file_path}")
                        self.total_good_length += utils.get_wav_length(file_path)
                        continue
                    elif file_path in self.bad:
                        print(f"Skipping {file_path}")
                        self.total_bad_length += utils.get_wav_length(file_path)
                        continue

                    print(f"Playing: {file_path}")

                    self.prompt_new_wav(file_path)
        self.good_files.close()
        self.bad_files.close()
        return "Completed"

    def __init__(self):
        self.total_good_length = 0.0
        self.total_bad_length = 0.0
        self.good = []
        self.bad = []
        from session import session

        self.directory = session["Path"]

        # Open files for appending and reading
        self.good_files = open(f"{session['Dataset name']}/good.txt", "a+")
        self.bad_files = open(f"{session['Dataset name']}/bad.txt", "a+")

        # Read existing lines into lists
        self.good_files.seek(0)
        self.good = [line.strip() for line in self.good_files.readlines()]

        self.bad_files.seek(0)
        self.bad = [line.strip() for line in self.bad_files.readlines()]

        self.exit_flag = {"exit": False}  # global exit flag

    # C:\Users\Hikari\Downloads\maybe\Cyrene 3-7
