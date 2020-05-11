import sync
import sys
import matplotlib.pyplot as plt
import filtering
import os
import peakfind


def demo_sync(data):
    """
    Show sync works by showing two accelereometers before, and after syncing
    """
    print("Sync demo")
    plt.subplot(121)
    sync.plotAccelerometer(data)
    plt.subplot(122)
    sync.plotSyncedAccelerometer(data)
    plt.show()


def demo_filter(data):
    """
    Show filtering works by showing noisy-ish signal before and after butterworth
    """
    print("Filter demo")
    ppg = data.getSyncedPPG()
    ppg.plot("PPG before filtering")

    filtered = filtering.butter_bandpass_filter(ppg, 0.4, 4, order=6)
    filtered.plot("PPG after filtering")
    plt.legend()
    plt.show()


def demo_ma(data):
    """
    Show JOSS in action.
    """
    print("MA filter demo")
    os.system("python3.6 joss.py ecg-files/DATA/20200228/18-25-25.EDF files/recordings/2020-02-28/18.33.06.101/")


def demo_hr(data):
    """
    Demonstrate my HR finding algorithm
    """
    print("HR finding demo")
    ppg = data.getSyncedPPG()[:1300]
    filtered = filtering.butter_bandpass_filter(ppg, 0.4, 4, order=6)
    peakfind.plot_peaks_min_sd(filtered)


def demo_kalman():
    """
    Show kalman filter improving the operation of earbuds + watch combination
    """
    print("kalman filter demo")
    os.system("python3 kalmanfilter.py ecg-files/DATA/20200413/12-13-29.EDF files/recordings/2020-04-13/12.36.35.034/")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        watch_dir = ""
        ecg_file = ""

    elif len(sys.argv) == 3:
        ecg_file = sys.argv[1]
        watch_dir = sys.argv[2]

    else:
        raise ValueError("Expected usage: sync.py (ecgFile watchDataDirectory)")

    data = sync.getSync(ecg_file, watch_dir)

    demo_sync(data)
    demo_filter(data)
    if False:
        demo_ma(data)
    demo_hr(data)
    demo_kalman()

