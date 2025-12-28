import time
import subprocess
import threading
import os
import utils
from audio_separator.separator import Separator
from session import session


class AudioProcessor:
    def __init__(self):
        print("Will copy files, then process")
        self.preserve_original = True
        self.separator = Separator()
        # self.separator.load_model(
        #     model_filename="Reverb_HQ_By_FoxJoy.onnx"
        # )  # we need this as well as de-echo

        while True:
            match input("Do you want to: \n1. edit the files\n2. Use a copy?"):
                case "1":
                    self.preserve_original = False
                    self.separator = Separator()
                    break

                case "2":
                    self.preserve_original = True
                    self.separator = Separator(
                        output_dir=f"output/{session['Dataset']}/processed_files/"
                    )
                    break
        self.separator.load_model("UVR-DeEcho-DeReverb.pth")
        from settings import settings

        if settings["Play after processing"] is None:
            while True:
                match input(
                    "Do you want to play each file after processing? <y/n> "
                ).lower():
                    case "y":
                        settings["Play after processing"] = True
                        break
                    case "n":
                        settings["Play after processing"] = False
                        break
                    case _:
                        pass

    def prompt_for_bad_processing(self):
        # start with vad, then uvr, then possibly audiosr?
        from session import session
        from settings import settings

        print(session)

        with open(f"{session['Dataset']}/bad.txt") as f:
            files = f.readlines()
            with open(f"{session['Dataset']}/processed.txt", "a+") as processed_txt:
                for file in files:
                    input(f"Will process {file}. Press enter to continue")
                    processed_file = self.uvr(file)

                    if settings["Play after processing"]:
                        if self.prompt_new_wav(processed_file):
                            processed_txt.write(processed_file + "\n")
                            print("Recorded good")
                        else:
                            print("File still bad. Not adding to processed list.")
                    else:
                        processed_txt.write(processed_file + "\n")

    def format(self, file):
        # save this for ffmpeg
        pass

    def uvr(self, file, agressive=False, de_echo=True):
        # file = self.separator.separate(file)
        # self.separator.load_model("UVR-DeEcho-DeReverb.pth")
        file = self.separator.separate(file)
        # TODO: find the processed one, rename, then move

    # pasted from manual sort, praying for it to work lol
    def prompt_new_wav(self, file_path: str):
        flags = {"exit": False, "good": None}  # global exit flag

        def check_keys():
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
                while not flags["exit"]:
                    key = _get_key()
                    if key:
                        key = key.lower()
                        if key == "w":
                            flags["good"] = True
                            return True

                        elif key == "e":
                            flags["good"] = False
                            return False

            finally:
                _restore()

        listener_thread = threading.Thread(target=check_keys)
        listener_thread.start()

        proc = subprocess.Popen(
            ["ffplay", "-autoexit", "-nodisp", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        while proc.poll() is None and not flags["exit"]:
            time.sleep(0.01)

        if proc.poll() is None:
            proc.terminate()

        listener_thread.join()
        return flags["good"]
