from scipy.signal import butter, lfilter, cheby2, sosfilt
import sys
import matplotlib.pyplot as plt
import numpy as np
import sync
import data

def butter_bandpass_filter(signal, lowcut, highcut, order=4):
    freq = signal.getFrequency()
    samples = signal.getValues()
    nyq = freq / 2
    low = lowcut / nyq 
    high = highcut / nyq 
    b, a = butter(order, [low, high], btype='band')
    filtered = lfilter(b, a, samples)
    return data.getSignal(filtered, freq)


def chebyshev2_filter(signal, lowcut, highcut, order=2):
    freq = signal.getFrequency()
    samples = signal.getValues()
    sos = cheby2(order, 30, [lowcut,highcut], btype='band', 
            fs=freq, output='sos')
    filtered = sosfilt(sos, samples)
    return data.getSignal(filtered, freq)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: filtering.py ecgFile watchDataDirectory")

    ecgFilePath = sys.argv[1]
    watchDirectoryPath = sys.argv[2]

    synced = sync.getSync(ecgFilePath, watchDirectoryPath)

    ecg, ppg = synced.getSyncedSignals()

    lowerBPM = 100
    upperBPM = 200
    butterFiltered = butter_bandpass_filter(ppg, 
        0.7, 3.5).normalize()

    chebyFiltered = chebyshev2_filter(ppg, lowerBPM/60, 
            upperBPM/60).normalize()

    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Band pass filter")

    ecg.plot("ECG")
    ppg.plot("Watch PPG")
    butterFiltered.plot("Butterworth filter")
    chebyFiltered.plot("Chebyshev filter")

    plt.legend()
    plt.show()
