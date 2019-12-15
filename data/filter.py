from scipy.signal import butter, lfilter
import sys
import matplotlib.pyplot as plt
import numpy as np
import sync

def butter_bandpass_filter(signal, lowcut, highcut, freq, order=6):
    nyq = freq / 2
    low = lowcut / nyq 
    high = highcut / nyq 
    b, a = butter(order, [low, high], btype='band')
    filtered = lfilter(b, a, signal)
    return filtered

def plot_signal(signal, freq, colour, label):
    xs = np.arange(0, signal.size/freq, 1/freq)
    plt.plot(xs, signal, color=colour, label=label)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.sync(ecgFile, watchDirectory)

    ecg, ppg, freq = synced.getSyncedSignals()

    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Band pass filter")

    print(freq)

    filtered = (butter_bandpass_filter(ppg, 0.5, 5, freq))
    print(filtered)


    plot_signal(ecg, freq, 'green', 'ECG')
    plot_signal(ppg, freq, 'blue', 'Watch PPG')
    plot_signal(filtered, freq, 'orange', 'Band-pass filter')
    plt.legend()
    plt.show()
