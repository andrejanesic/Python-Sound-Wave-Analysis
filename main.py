import wave
import numpy as np
import sys
import matplotlib.pyplot as plt


class SoundWave:
    """
    Encapsulates the wave file and its associated operations.
    """

    def __init__(self, name, wave):
        """
        Default constructor. Takes in the file name and a NumPy 1-D array as input.
        """
        self.name = name
        self.wave = wave


def load_wave(filename):
    """
    Reads the wave file from ./input/<filename>.wav. Returns the file as a SoundWave.
    """

    fpath = f"./input/{filename}.wav"

    # This would normally go into a try-except clause but IO errors are not important for this program.
    try:
        wav = wave.open(fpath, "r")
    except FileNotFoundError:
        print(f"File does not exist: {fpath}")
        return None

    vals = np.frombuffer(wav.readframes(-1), np.int16)

    # Average of two channels if stereo file.
    if wav.getnchannels() > 1:
        ch1 = vals[0::2]
        ch2 = vals[1::2]

        # TODO this might be an SPOF, because we're averaging the two channels with floor division.
        vals = (ch1 + ch2) // 2

    return SoundWave(name=filename, wave=vals)


def list_waves(d):
    """
    Lists the available sound waves from d dictionary of SoundWave objects.
    """
    print("Sound waves available:")
    for key in d:
        print(f"\t{key}")


def quit():
    """
    Called for graceful app exit.
    """
    print("Bye")
    sys.exit(0)


sound_waves = {}

while True:

    cmd = input("> ").split(" ")

    if cmd[0].lower() == "load":

        if len(cmd) != 2 or cmd[1] == "":
            print("Invalid syntax:")
            print("load <filename> ::: Loads the file from ./input/<filename>.wav")
            continue

        filename = cmd[1]
        if sound_waves.get(filename, None) != None:
            print(f"File already loaded: {filename}")
            continue

        w = load_wave(filename)
        if w != None:
            sound_waves[filename] = w
            print(f"Sound wave loaded: {filename}")

    elif cmd[0].lower() == "list":
        list_waves(sound_waves)
        continue

    elif cmd[0].lower() == "quit":
        quit()

    else:
        print("Commands:")
        print("load <filename> ::: Loads the file from ./input/<filename>.wav")
        print("quit ::: Closes the application")
