# from termios import tcflush
import os
import msvcrt


def clear_the_fucking_input():
    if os.name == "nt":
        while msvcrt.kbhit():
            msvcrt.getch()
            # windows currently and i cant test this lol
    # elif os.name == "posix":
    #     try:
    #         if sys.stdin.isatty():
    #             tcflush(sys.stdin.fileno(), TCIFLUSH)
    #     except Exception:
    #         pass


def get_wav_length(file):
    import wave

    # folder where your wav files are stored

    with wave.open(file, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        return duration


def iter_files(directory, extension):  # bro i only noticed this was here just now XDDDD
    # TODO: move this to utils and refactor
    # RECURSIVE BTW
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)
