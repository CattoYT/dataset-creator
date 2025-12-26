from pydub import AudioSegment


def get_good_duration():
    with open("good.txt", 'r') as good_files:

        good = [line.strip() for line in good_files.readlines()]
        seconds = 0
        for file in good:
            size = AudioSegment.from_file(file).duration_seconds
            seconds += size
        return seconds
        
def get_bad_duration():
    with open("bad.txt", 'r') as good_files:
    
        good = [line.strip() for line in good_files.readlines()]
        seconds = 0
        for file in good:
            size = AudioSegment.from_file(file).duration_seconds
            seconds += size
        return seconds