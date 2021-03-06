import sync
import sys
import numpy as np
import filtering
import peakfind
import data
import motionfilter
import heartpy as hp
from scipy.signal import resample
import matplotlib.pyplot as plt

PLOTTING = True
HEARTPY_SEGS = True


def get_ecg_hr(signal, ave_size = 16):
    """
    Get a numpy array containing the second by second HR value from the signal, based on averaging
    over the last ave_size seconds.
    """
    vals = signal.getValues()
    freq = signal.getFrequency()


    length = int(vals.size / freq)

    if HEARTPY_SEGS:
        filtered = hp.remove_baseline_wander(hp.scale_data(vals), freq)
        overlap = 1 - (1/ave_size)
        wd, m = hp.process_segmentwise(filtered, sample_rate=freq, segment_width=ave_size, 
                segment_overlap=overlap, bpmmax=220, mode='fast', 
                outlier_method='z-score', replace_outliers=False)
        bpm = np.array(m['bpm'])
        hr = np.zeros(len(bpm) + ave_size//2)
        hr[(ave_size//2):] = bpm


    else:
        hr = np.zeros(length)
        for i in range(ave_size, length - 1, 1):
            window = vals[freq * (i - ave_size) : freq * i]
            filtered = hp.remove_baseline_wander(hp.scale_data(window), freq)

            wd, m = hp.process(hp.scale_data(filtered), freq, bpmmax=220, windowsize=0.1)
            hr[i] = m["bpm"]
            if hr[i] > 210 and PLOTTING:
                hp.plotter(wd, m)
        
        for i in range(ave_size):
            hr[i] = hr[ave_size]


    return hr

def get_ppg_hr(signal, ave_size = 30, method = 'sd'):
    vals = signal.getValues()
    freq = signal.getFrequency()
    length = int(vals.size / freq)
    hr = np.zeros(length)

    for i in range(ave_size, length - 1, 1):
        window = vals[int(freq * (i - ave_size)) : int(freq * i)]
        if method == 'sd':
            hr[i] = peakfind.get_rate_min_sd(data.getSignal(window, freq))
        elif method == 'naive':
            hr[i] = peakfind.get_rate_naive(data.getSignal(window, freq))
        else:
            raise ValueError("Invalid argument for method, valid arguments are 'sd' or 'naive'")

    
    for i in range(ave_size):
        hr[i] = hr[ave_size]

    return hr


if False and __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: heartrate.py",
                "ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    #########################################################################
    # SYNC the signals using the accelerometer                              #
    #########################################################################

    synced = sync.getSync(ecgFile, watchDirectory)
    ecg, ppg = synced.getSyncedSignals()

    #########################################################################
    # FILTER the signals                                                    #
    #########################################################################

    lowerBPM = 40
    upperBPM = 220
    ppgFiltered = filtering.butter_bandpass_filter(
            ppg, lowerBPM/60, upperBPM/60).normalize()

    #########################################################################
    # Remove MOTION from the signals                                        #
    #########################################################################

    # Get the acceleration in each axis, and run each through a band pass
    # filter
    accelerationX = synced.getSyncedAcceleration('x')
    accelerationY = synced.getSyncedAcceleration('y')
    accelerationZ = synced.getSyncedAcceleration('z')

    accelerationX = filtering.butter_bandpass_filter(
            accelerationX, lowerBPM/60, upperBPM/60).normalize()
    accelerationY = filtering.butter_bandpass_filter(
            accelerationY, lowerBPM/60, upperBPM/60).normalize()
    accelerationZ = filtering.butter_bandpass_filter(
            accelerationZ, lowerBPM/60, upperBPM/60).normalize()

    # Run adaptive motion filters on each axis to remove motion from signals
    ppgMotionFiltered = motionfilter.adaptiveFilter(
            ppgFiltered, accelerationX)
    ppgMotionFiltered = motionfilter.adaptiveFilter(
            ppgMotionFiltered, accelerationY)
    ppgMotionFiltered = motionfilter.adaptiveFilter(
            ppgMotionFiltered, accelerationZ)

    #########################################################################
    # Calculate Heart Rate                                                  #
    #########################################################################

    ppghr = get_ppg_hr(ppgFiltered)

    #########################################################################
    # Compare to ECG heart rate                                             #
    #########################################################################

    ecghr = get_ecg_hr(ecg)

    plt.plot(ppghr, label="PPG")
    plt.plot(ecghr, label="ECG")
    plt.legend()
    plt.show()

    print("PPG HRs")
    print(ppgHR)

    print("ECG HRs")
    print(ecgHR)
    
    errors = np.abs(ppgHR - ecgHR)
    errors = errors[6:] # remove errors from start of signal

    print(errors)
    print(np.average(errors))


# Calculate the heartrate from the ECG. Algorithm works by splitting the
# signal into windows (of length window seconds) and calculating the HR
# in each window. Returns a numpy array, of HR values.
def getEcgHR(signal, window):
    vals = signal.getValues()
    freq = signal.getFrequency()
    windowSize = window * freq
    heartrates = np.zeros((vals.size // windowSize))

    for i in range(vals.size // windowSize):
        filtered = hp.remove_baseline_wander(vals[:windowSize], freq)
        wd, m = hp.process(hp.scale_data(filtered), freq, bpmmax=220)
        heartrates[i] = m["bpm"]
        vals = vals[windowSize:]

    return heartrates


def getPpgHR(signal, peaks, window):
    freq = signal.getFrequency()
    vals = signal.getValues()
    windowSize = int(window * freq)
    heartrates = np.zeros((int(vals.size // windowSize)))

    for i in range((int(vals.size // windowSize))):
#        # Find range
#        lower = windowSize * i
#        upper = windowSize * (i + 1)
#
#        # Find number of peaks in that range
#        count = np.count_nonzero((lower <= peaks) & (peaks <= upper))
#
#        #Calculate bpm
#        bpm = count / window * 60
#        heartrates[i] = bpm
        data = vals[:windowSize]

        filtered = hp.remove_baseline_wander(vals[:windowSize], freq)

        try:
            wd, m = hp.process(hp.scale_data(data), freq, bpmmax=220)
            heartrates[i] = m["bpm"]
            if PLOTTING:
                hp.plotter(wd, m, title='Heart Beat Detection on Noisy Signal')

        except:
            if PLOTTING:
                plt.figure()
                plt.plot(data)
                plt.title("Data before baseline")

                plt.figure()
                plt.plot(filtered)
                plt.title("Data after baseline")
                plt.show()

            # Find range
            lower = windowSize * i
            upper = windowSize * (i + 1)

            # Find number of peaks in that range
            count = np.count_nonzero((lower <= peaks) & (peaks <= upper))

            #Calculate bpm
            bpm = count / window * 60
            heartrates[i] = bpm

        vals = vals[windowSize:]

    return heartrates


def plot_ppg(signal, label="PPG", method="sd"):
    signal = filtering.butter_bandpass_filter(signal, 20/60, 220/60, order=6)
    hr = get_ppg_hr(signal, ave_size=30, method=method)
    plt.plot(np.arange(0, hr.size, 1), hr, label=label)


def plot_ecg(signal, label="ECG"):
    hr = get_ecg_hr(signal, ave_size=15)
    plt.plot(np.arange(0, hr.size, 1), hr, label=label)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: heartrate.py ecgFile watchDir")

    ecgfile = sys.argv[1]
    watchdir= sys.argv[2]
    sync = sync.Sync(ecgfile, watchdir)

    plot_ecg(sync.getSyncedECG())
    plot_ppg(sync.getSyncedPPG(), label="Naive PPG", method='naive')
    plot_ppg(sync.getSyncedPPG(), label="SD Minimization PPG", method='sd')
    plt.legend()
    plt.show()

