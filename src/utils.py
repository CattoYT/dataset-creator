# from termios import tcflush
import os


def clear_the_fucking_input():
    if os.name == "nt":
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()
            # windows currently and i cant test this lol
    # elif os.name == "posix":
    #     import sys
    #     import termios

    #     try:
    #         if sys.stdin.isatty():
    #             termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
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
    # RECURSIVE BTW
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)
