from typing import List
import wave
import numpy as np
import sys
import matplotlib.pyplot as plt


class SoundWave:
    """
    Encapsulates the wave file and its associated operations.
    """

    def __init__(self, name: str, wave: wave.Wave_read, values: np.ndarray):
        """
        Default constructor. Takes in the file name and a NumPy 1-D array as input.
        """
        self.name = name
        self.wave = wave
        self.values = values


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

    return SoundWave(name=filename, wave=wav, values=vals)


def plot_waves(sound_waves: List[SoundWave], type="waveform"):
    """
    Plots all passed sound waves on a single plot with the given type.
    """
    title = f"{type.capitalize()} plot of"

    plt.ylabel("Amplitude")

    plt.xlabel("Time")

    for sw in sound_waves:
        title += f" {sw.name}.wav"
        time = np.linspace(0, len(sw.values) /
                           sw.wave.getframerate(), num=len(sw.values))
        # TODO check if okay to simply plot different times
        plt.plot(time, sw.values, label=f"{sw.name}.wav")

    plt.legend()

    plt.show()


def list_waves(d):
    """
    Lists the available sound waves from d dictionary of SoundWave objects.
    """
    if len(d.keys()) == 0:
        print("No sound waves loaded")
        return

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

    if len(cmd) == 0:
        continue

    func = cmd[0].lower()

    if func == "list":
        list_waves(sound_waves)
        continue

    elif func == "load":

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

    elif func == "plot":

        plot_type = 'waveform'

        if len(cmd) < 2:
            print("Invalid syntax:")
            print(
                "plot [waveform|spectogram|histogram] <filename> [...filenames] ::: Plots the selected wavefile on the selected type of graph. Multiple wavefiles may be plotted.")
            continue

        i = 1
        if cmd[1].lower() in ['waveform', 'spectogram', 'histogram']:
            plot_type = cmd[1].lower()
            i += 1

        to_compare = []
        br = False
        for f in cmd[i:]:
            sw = sound_waves.get(f, None)
            if sw == None:
                print(f"Sound wave {f} not loaded")
                br = True
                continue
            to_compare.append(sw)
        if br:
            continue

        plot_waves(to_compare, type=plot_type)

    elif func == "quit":
        quit()

    else:
        print("Commands:")
        print("help ::: Shows this menu.")
        print("list ::: Lists all loaded wavefiles.")
        print("load <filename> ::: Loads the file from ./input/<filename>.wav")
        print(
            "plot (waveform|spectogram|histogram) <filename> [...filenames] ::: Plots the selected wavefile on the selected type of graph. Multiple wavefiles may be plotted.")
        print("quit ::: Closes the application")
