import sys
import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import sync
import filter

def find_peaks(signal):
    peaks, _ = scipy.signal.find_peaks(signal)
    return peaks

"""
Use continuous wavelet transformations in order to detect peaks.
"""
def find_peaks_cwt(signal):
    peaks = scipy.signal.find_peaks_cwt(signal, np.arange(1,20))
    return peaks


def plot_peaks(peaks, signal, freq, color="red"):
    xs = np.arange(0, signal.size/freq, 1/freq)
    plt.plot(xs[peaks], signal[peaks], "x")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: peakfind.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.sync(ecgFile, watchDirectory)

    ecg, ppg, freq = synced.getSyncedSignals()

    ppgOriginal, ppgFreq = synced.getSyncedPpgOriginalFreq()
    lowerBPM = 100
    upperBPM = 200

    butterFiltered = synced.normalize(filter.butter_bandpass_filter(
        ppgOriginal,lowerBPM/60, upperBPM/60, ppgFreq))

    butterPeaks = find_peaks(butterFiltered)
    butterPeaksCwt = find_peaks_cwt(butterFiltered)

    chebyFiltered = synced.normalize(filter.chebyshev2_filter(ppgOriginal,
        lowerBPM/60, upperBPM/60, ppgFreq))

    chebyPeaks = find_peaks(chebyFiltered)
    chebyPeaksCwt = find_peaks_cwt(chebyFiltered)


    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Band pass filter")

    #filtered = (butter_bandpass_filter(ppg, 1, 20, freq))

    filter.plot_signal(ecg, freq, 'green', 'ECG')
    filter.plot_signal(ppg, freq, 'blue', 'Watch PPG')
#    filter.plot_signal(butterFiltered, ppgFreq, 'orange', 
#            'Butterworth filter')
#    plot_peaks(butterPeaks, butterFiltered, ppgFreq)
#    plot_peaks(butterPeaksCwt, butterFiltered+0.1, 
#            ppgFreq, color="orange") #Plot CWT above


    filter.plot_signal(chebyFiltered, ppgFreq, 'purple', 'Chebyshev filter')
    plot_peaks(chebyPeaks, chebyFiltered, ppgFreq)
    plot_peaks(chebyPeaksCwt, chebyFiltered+0.1, ppgFreq, color="orange") #Plot CWT above

    plt.legend()
    plt.show()
