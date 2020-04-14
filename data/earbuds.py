import heartrate
import numpy as np
import matplotlib.pyplot as plt
import pandas
import sys
import sync
import os
import data

class EarbudData:
    def __init__(self, directory, old_style = False):
        """
        old_style means ear recordings are in their own directory, with new 
        style, they're bundled in the watch files
        """
        if not os.path.isdir(directory):
            raise IOError("Directory {} does not exist".format(directory))
        self.directory = directory
        self.old_style = old_style
        self.file_name = "hr.csv" if old_style else "ear.csv"


    @property
    def times(self):
        df = pandas.read_csv(os.path.join(self.directory, self.file_name))
        time = df['time'].to_numpy()
        return time
    
    
    def get_hr(self):
        """
        Get heart-rate as a start time and a numpy array of the heart-rate
        """
        df = pandas.read_csv(os.path.join(self.directory, self.file_name))
        hr = df['value'].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = time.size / ((time[time.size-1] - time[0]) / 1000)
        assert(np.abs(freq - 1) < 0.01)

        return time[0], hr


class Sync(sync.Sync):
    def __init__(self, ecgFile, watchDirectory, earbudDirectory=None):
        """
        Parameters
        ------------------
         - earbudDirectory = None means the ear files are in the watch directory
         - hr - True if using the HR, false if using PPG
        """
        if earbudDirectory is None:
            self.ear_data = EarbudData(watchDirectory,False)
        else:
            self.ear_data = EarbudData(earbudDirectory,True)

        super().__init__(ecgFile, watchDirectory)
        super().setStartCrop(0)
        super().setEndCrop(1)
        try:
            super().getSyncedPPG()
            self._ecg, self._ppg, self._ear = self.get_synced_signals()
            self._hr = None

        except:
            self._ecg = self.getSyncedECG()
            self._ear = data.getSignal(self.ear_data.get_hr()[1], 1)
            self._hr = self.getSyncedHR()
            self._ppg = None

            time_diff = self.getTimeDifference()
            delta = int(abs(time_diff))

            if time_diff < 0:
                self._ear = self._ear[delta:]



            
        

    @property
    def ecg(self):
        return self._ecg
        
    @property
    def ppg(self):
        return self._ppg

    @property
    def ear(self):
        return self._ear

    def get_synced_signals(self):
        ecg = self.getSyncedECG()
        ppg = self.getSyncedPPG()
        ear = data.getSignal(self.ear_data.get_hr()[1], 1)

        ppg_times = self.watchData.times
        ear_times = self.ear_data.times

        # starting times for PPG signal and earbud signal, given in ms
        ppg_start = ppg_times[0]
        ear_start = ear_times[0]

        if ear_start < ppg_start:
            # Find first ear_time which is over the start time of the ppg, then find the closest ppg
            # time to that. Crop all signals.
            crop_ear = None
            crop_ppg = None
            for i, t in enumerate(ear_times):
                if t > ppg_start:
                    crop_ear = i

                    # Find the amount to crop the PPG by looking at where the start times are closest
                    crop_ppg = np.argmin(np.abs(ppg_times[:int(ppg.frequency)] - t))
                    break

            if crop_ppg is None:
                raise ValueError("Couldn't sync, ensure recordings happened at the same time.")

            crop_ecg = int(crop_ppg * ecg.frequency / ppg.frequency)
            ppg = ppg[crop_ppg:]
            ecg = ecg[crop_ecg:]
            ear = ear[crop_ear:]

        else:
            # Find smaple number in ppg which is closest to ear_start, and crop both ppg and ecg
            crop = None

            for i, t in enumerate(ppg_times):
                if t > ear_start:
                    crop = i
                    print(crop)
                    break

            if crop is None:
                raise ValueError("Couldn't sync, ensure recordings happened at the same time.")

            ppg_crop = crop
            ecg_crop = int(crop * ecg.frequency / ppg.frequency)

            ppg = ppg[ppg_crop:]
            ecg = ecg[ecg_crop:]

        return ecg, ppg, ear



def plot_ppg(signal, label="PPG"):
    hr = heartrate.get_ppg_hr(signal)
    plt.plot(np.arange(0, hr.size, 1), hr, label=label)


def plot_ecg(signal, label="ECG"):
    hr = heartrate.get_ecg_hr(signal, ave_size=40)
    plt.plot(np.arange(0, hr.size, 1), hr, label=label)
    
def plot_earbud(hr, label="Earbuds"):
    plt.plot(hr, label=label)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        earbud_dir = sys.argv[3]
    elif len(sys.argv) == 3:
        earbud_dir = None
    else:
        raise ValueError("Expected usage: sync.py ecgFile watchDir (earbudDir)")

    ecgfile = sys.argv[1]
    watchdir= sys.argv[2]
    sync = Sync(ecgfile, watchdir, earbud_dir)
    plot_ecg(sync.ecg)
    sync.ear.plot("Earbud")
    sync.hr.plot("Watch HR")
    plt.legend()
    plt.show()

