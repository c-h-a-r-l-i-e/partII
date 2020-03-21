import heartrate
import numpy as np
import matplotlib.pyplot as plt
import pandas
import sys
import sync
import os

class EarbudData:
    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError("Directory {} does not exist".format(directory))
        self.directory = directory
    
    
    def get_hr(self):
        """
        Get heart-rate as a start time and a numpy array of the heart-rate
        """
        df = pandas.read_csv(os.path.join(self.directory, "hr.csv"))
        hr = df['value'].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = time.size / ((time[time.size-1] - time[0]) / 1000)
        assert(np.abs(freq - 1) < 0.01)


        return time[0], hr

def plot_ppg(signal, label="PPG"):
    hr = heartrate.get_ppg_hr(signal)
    plt.plot(np.arange(140, 140 + hr.size, 1), hr, label=label)



def plot_ecg(signal, label="ECG"):
    hr = heartrate.get_ecg_hr(signal)
    plt.plot(np.arange(140, 140 + hr.size, 1), hr, label=label)
    
def plot_earbud(hr, label="Earbuds"):
    plt.plot(hr, label=label)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("Expected usage: sync.py ecgFile watchDir earbudDir")
    ecgfile = sys.argv[1]
    watchdir= sys.argv[2]
    earbud_dir = sys.argv[3]
    sync = sync.getSync(ecgfile, watchdir)
    earbud_data = EarbudData(earbud_dir)
    ecg, ppg = sync.getSyncedSignals()
    plot_ppg(ppg)
    
    plot_ecg(sync.getSyncedECG())
    earbudtime, earbudhr = earbud_data.get_hr()
    plot_earbud(earbudhr)
    plt.legend()
    plt.show()

