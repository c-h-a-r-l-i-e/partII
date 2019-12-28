from scipy.signal import butter, lfilter, cheby2, sosfilt
import sys
import matplotlib.pyplot as plt
import numpy as np
import sync

def butter_bandpass_filter(signal, lowcut, highcut, freq, order=4):
    nyq = freq / 2
    low = lowcut / nyq 
    high = highcut / nyq 
    b, a = butter(order, [low, high], btype='band')
    filtered = lfilter(b, a, signal)
    return filtered


def chebyshev2_filter(signal, lowcut, highcut, freq, order=2):
    sos = cheby2(order, 30, [lowcut,highcut], btype='band', fs=freq, output='sos')
    filtered = sosfilt(sos, signal)
    return filtered


def plot_signal(signal, freq, colour, label):
    xs = np.arange(0, signal.size/freq, 1/freq)
    xs = xs[0:signal.size]
    plt.plot(xs, signal, color=colour, label=label)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.sync(ecgFile, watchDirectory)

    ecg, ppg, freq = synced.getSyncedSignals()

    ppgOriginal, ppgFreq = synced.getSyncedPpgOriginalFreq()
    lowerBPM = 100
    upperBPM = 200
    butterFiltered = synced.normalize(butter_bandpass_filter(ppgOriginal, 
        0.7, 3.5, ppgFreq))

    chebyFiltered = synced.normalize(chebyshev2_filter(ppgOriginal, 
        lowerBPM/60, upperBPM/60, ppgFreq))


    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Band pass filter")


    plot_signal(ecg, freq, 'green', 'ECG')
    plot_signal(ppg, freq, 'blue', 'Watch PPG')
    plot_signal(butterFiltered, ppgFreq, 'orange', 'Butterworth filter')
    plot_signal(chebyFiltered, ppgFreq, 'purple', 'Chebyshev filter')
    plt.legend()
    plt.show()
