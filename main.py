from typing import Dict, List
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
        self.cleaned = False

    def find_endpoints(self, p: int, r: int):
        """
        Finds the endpoints of speech on the sound wave. Returns noise mask and borders.
        """

        # Get the number of frames for the first 100ms.
        initial_t = 100
        initial_t = round((self.wave.getframerate()) * initial_t / 1000)
        initial_f = np.absolute(self.values[:initial_t])

        # Noise limit.
        noise_l = np.average(initial_f) + 2 * initial_f.std()
        noise_mask = np.zeros(self.values.shape)

        # Window width (ms) for noise detection.
        window_w = 10
        window_w = round(self.wave.getframerate() * window_w / 100)

        i = 0
        while i < len(self.values):
            # TODO pitati jel treba i ovde abs
            window_avg = np.average(np.absolute(self.values[i:(i+window_w)]))
            j = 1 if window_avg > noise_l else 0
            noise_mask[i:(i+window_w)] = j
            i += window_w

        # TODO pitati sto mi ovo skoro nista ne menja???
        # TODO da li se ovo moze zameniti vektorskim racunom?
        length = 0
        start = -1
        curr = 0
        while curr < len(noise_mask):
            if noise_mask[curr] == 1:
                if length < p:
                    noise_mask[start+1:start+1+length] = 1
                start = curr
                length = 0
            curr += 1
            length += 1

        length = 0
        start = -1
        curr = 0
        while curr < len(noise_mask):
            if noise_mask[curr] == 0:
                if length < r:
                    noise_mask[start+1:start+1+length] = 0
                start = curr
                length = 0
            curr += 1
            length += 1

        # Find borders of noise.
        shift_l = noise_mask.tolist().copy()
        shift_l.pop(0)
        shift_l.append(0)
        shift_r = noise_mask.tolist().copy()
        shift_r.pop()
        shift_r.insert(0, 0)
        noise_borders = ((noise_mask - np.array(shift_l) >
                          0) | (noise_mask - np.array(shift_r) > 0)).astype(int)
        noise_borders = (np.array(np.nonzero(noise_borders)) /
                         self.wave.getframerate())[0].tolist()

        return (noise_mask, noise_borders)

    def clean(self, p: int, r: int):
        """
        Removes non-speech parts of the wave. Finds speech endpoints first with given values P and R.
        """
        noise_mask, _ = self.find_endpoints(p, r)
        self.values = np.delete(self.values, ~noise_mask.astype(bool))
        self.cleaned = True


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
        _, noise_borders = sw.find_endpoints(500, 5000)
        time = np.linspace(0, len(sw.values) /
                           sw.wave.getframerate(), num=len(sw.values))
        # TODO check if okay to simply plot different times
        plt.plot(time, sw.values, label=f"{sw.name}.wav")
        clr = np.random.rand(3,)
        if not sw.cleaned:
            for xc in noise_borders:
                plt.axvline(x=xc, color=clr)

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


sound_waves: Dict[str, SoundWave] = {}
p = 500
r = 5000

while True:

    cmd = input("> ").strip().split(" ")
    cmd = [x.strip() for x in cmd if x.strip() != ""]

    if len(cmd) == 0:
        continue

    func = cmd[0].lower()

    if func == "clean":

        if len(cmd) == 1:
            to_clean = sound_waves.values()
        else:
            to_clean = []
            br = False
            for f in cmd[i:]:
                sw = sound_waves.get(f, None)
                if sw == None:
                    print(f"Sound wave {f} not loaded")
                    br = True
                    continue
                to_clean.append(sw)
            if br:
                continue

        for sw in to_clean:
            sw.clean(p, r)
            print(f"Sound wave {sw.name} cleaned")

    elif func == "list":
        list_waves(sound_waves)
        continue

    elif func == "load":

        if len(cmd) < 2:
            print("Invalid syntax:")
            print("load <filename> ::: Loads the file from ./input/<filename>.wav")
            continue

        for fn in cmd[1:]:
            if sound_waves.get(fn, None) != None:
                print(f"File already loaded: {fn}")
                continue

            w = load_wave(fn)
            if w != None:
                sound_waves[fn] = w
                print(f"Sound wave loaded: {fn}")

    elif func == "plot":

        plot_type = 'waveform'

        i = 1
        if len(cmd) > 1:
            if cmd[1].lower() in ['waveform', 'spectogram', 'histogram']:
                plot_type = cmd[1].lower()
                i += 1

        if len(cmd) == 1:
            to_compare = sound_waves.values()
        else:
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
        print(
            "clean <filename> [...filenames] ::: Removes non-speech parts of the selected soundwaves")
        print("help ::: Shows this menu.")
        print("list ::: Lists all loaded wavefiles.")
        print(
            "load <filename> [...filenames] ::: Loads each specified file from ./input/<filename>.wav")
        print(
            "plot [waveform|spectogram|histogram] [...filenames] ::: Plots the selected wavefile on the selected type of graph. Multiple wavefiles may be plotted. If no file is specified, plots all loaded.")
        print("quit ::: Closes the application")
