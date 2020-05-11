import sys
import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import sync
import filtering
import data

def find_peaks(signal):
    """
    Find peaks using the naive local maxima solution

    Inputs
    ----------------------
     - signal: 1D numpy array
       Heartbeat signal we want to find peaks from


    Returns
    ----------------------
     - out: 1D numpy array
       The position of peaks in the data (their x positons)

    """
    values = signal.getValues()
    peaks, _ = scipy.signal.find_peaks(values)
    return peaks



def moving_average(signal, window_size):
    """
    Calculates the moving average of signal

    Inputs
    ----------------------
     - signal: 1D numpy array
       The signal to take the average of

     - window_size: int or float
       Size of the window we average over in seconds

    Returns
    ---------------------
     - out: 1D numpy array
       The moving average of the signal
    """
    window = int(window_size * signal.getFrequency())
    kernel = np.array([1/window for _ in range(window)])
    mov_average = np.convolve(signal.getValues(), kernel, mode='valid')

    # Pad the missing values with the average of the signal
    average = np.mean(signal.getValues())
    missing = np.array([average for _ in range(int((signal.getValues().size - mov_average.size)/2))])
    mov_average = np.insert(mov_average, 0, missing)
    mov_average = np.append(mov_average, missing)

    return data.getSignal(mov_average, signal.getFrequency())
    

def plot_moving_average(signal, window_size=0.75):
    mov_average = moving_average(signal, window_size)
    signal.plot("signal")
    mov_average.plot("average")
    plt.show()


def find_peaks_min_sd(signal, window_size=0.75):
    """
    Finds the peaks based on which set of peaks gives the least standard deviation.
    Starts by finding positions where the signal increases above the moving average, then at each step
    increase the moving average. The resulting peaks are the peaks which minimise the peak-peak
    interval's standard deviation.

    Inputs
    ----------------------
     - signal: 1D numpy array
       Heartbeat signal we want to find peaks from


    Returns
    ----------------------
     - out: 1D numpy array
       The position of peaks in the data (their x positons)

    """
    percs = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 200, 300]
    mov_ave = moving_average(signal, window_size)
    mov_ave = mov_ave.getValues()
    signal_vals = signal.getValues()

    min_sd = np.inf
    current_peaks = []

    for perc in percs:
        threshold = mov_ave + mov_ave * perc / 100

        #Find points above current moving average 
        x_peaks = (signal_vals > threshold).nonzero()[0]
        y_peaks = signal_vals[x_peaks]
        peak_edges = (np.diff(x_peaks) > 1).nonzero()[0] + 1

        # find the maximum between the peak edges. 
        peaks = []
        for i in range(len(peak_edges) - 1):
            ys = y_peaks[peak_edges[i]:peak_edges[i+1]].tolist()
            if len(ys) > 0:
                peaks.append(x_peaks[peak_edges[i] + ys.index(max(ys))])

        # Calculate standard deviation of the peak peak intervals
        intervals = np.diff(peaks) / signal.getFrequency()
        sd = np.std(intervals)

        if sd < min_sd and check_valid_hr(signal, peaks):
            min_sd = sd
            current_peaks = peaks

    return np.array(current_peaks)

def check_valid_hr(signal, peaks):
    """
    Validate that the peaks given provide a heart-rate within a reasonable
    range (between 40 and 240 bpm).
    """
    rate = len(peaks)/ (signal.getValues().size / signal.getFrequency()) * 60
    valid =  rate >= 40 and rate <= 240
    return valid


def get_rate_min_sd(signal):
    peaks = find_peaks_min_sd(signal)
    rate = peaks.size / (signal.getValues().size / signal.getFrequency()) * 60
    return rate

def get_rate_naive(signal):
    peaks = find_peaks(signal)
    rate = peaks.size / (signal.getValues().size / signal.getFrequency()) * 60
    return rate

def plot_peaks_min_sd(signal): 
    peaks = find_peaks_min_sd(signal)
    signal.plot("signal")
    plot_peaks(peaks, signal, "Min-SD peaks")
    plt.show()


def plot_peaks(peaks, signal, label):
    values = signal.getValues()
    freq = signal.getFrequency()
    xs = np.arange(0, values.size/freq, 1/freq)
    plt.plot(xs[peaks], values[peaks], "x", label=label)

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

    ecg, whole_ppg = synced.getSyncedSignals()
    
    for i in range(10, 20, 1):
        ppg = whole_ppg[i * 20 * 20 : (i * 20 + 20) * 20]

        lowerBPM = 40
        upperBPM = 240
        #butterFiltered = filtering.butter_bandpass_filter(
        #    ppg,lowerBPM/60, upperBPM/60, order=4).normalize()

        plt.subplot(121)
        plt.title("Local Maxima Peaks")
        local_peaks = find_peaks(ppg)
        plot_peaks(local_peaks, ppg, label="Local Maxima Peaks")
        ppg.plot("PPG Signal")

        plt.subplot(122)
        plt.title("Standard Dev. Min. Peaks")
        sd_peaks = find_peaks_min_sd(ppg)
        plot_peaks(sd_peaks, ppg, label="Standard Dev. Min. Peaks")
        ppg.plot("PPG Signal")
        plt.show()

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
