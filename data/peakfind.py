import sys
import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import sync
import filtering
import data

def find_peaks(signal):
    values = signal.getValues()
    peaks, _ = scipy.signal.find_peaks(values)
    return peaks

"""
Use continuous wavelet transformations in order to detect peaks.
"""
def find_peaks_cwt(signal):
    values = signal.getValues()
    peaks = scipy.signal.find_peaks_cwt(values, np.arange(1,20))
    return peaks


def plot_peaks(peaks, signal, color="red"):
    values = signal.getValues()
    freq = signal.getFrequency()
    xs = np.arange(0, values.size/freq, 1/freq)
    plt.plot(xs[peaks], values[peaks], "x")

def get_rate(peaks, signal):
    freq = signal.getFrequency()

    # Iterate through peaks, calculating heart rate for each one
    rate = np.zeros(peaks.shape)
    for i in range(1, peaks.size):
        delta = peaks[i] - peaks[i-1]
        rate[i] = freq/delta * 60 # HR in bpm

    # Create a function which interpolates between each heart rate
    interp = scipy.interpolate.interp1d(peaks/freq, rate, "next", 
            fill_value="extrapolate")
    
    xs = np.arange(peaks[1], signal.getValues().size/freq, 1/freq)
    interpolated = interp(xs)
    rateSignal = data.getSignal(interpolated, freq)

    return rateSignal

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: peakfind.py ecgFile",
                "watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.getSync(ecgFile, watchDirectory)

    ecg, ppg = synced.getSyncedSignals()

    lowerBPM = 100
    upperBPM = 200
    butterFiltered = filtering.butter_bandpass_filter(
        ppg,lowerBPM/60, upperBPM/60).normalize()

    butterPeaks = find_peaks(butterFiltered)
    #butterPeaksCwt = find_peaks_cwt(butterFiltered)

    chebyFiltered = filtering.chebyshev2_filter(ppg,
        lowerBPM/60, upperBPM/60).normalize()

    chebyPeaks = find_peaks(chebyFiltered)
    #chebyPeaksCwt = find_peaks_cwt(chebyFiltered)

#    plt.xlabel("Time (s)")
#    plt.ylabel("Value")
#    plt.title("Peak detection")
#
#    ecg.plot("ECG")
#    ppg.plot("Watch PPG")
#    butterFiltered.plot("Butterworth filter")
#
#    plot_peaks(butterPeaks, butterFiltered)
#
#    plt.legend()
#    plt.show()

    rate = get_rate(butterPeaks, butterFiltered)
    plot_peaks(butterPeaks, butterFiltered)
    rate.plot()
    plt.show()
