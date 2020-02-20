import sync
import sys
import numpy as np
import filtering
import peakfind
import motionfilter
import heartpy as hp
from scipy.signal import resample
import matplotlib.pyplot as plt

PLOTTING = False

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


if __name__ == "__main__":
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
    # FIND the PEAKS in the signal                                          #
    #########################################################################


    ppgPeaks = peakfind.find_peaks(ppgMotionFiltered)

    #########################################################################
    # Calculate Heart Rate                                                  #
    #########################################################################

    windowSize = 10 # windowSize gived periods over which we calculate HR (s)

    ppgHR = getPpgHR(ppg, ppgPeaks, windowSize)

    #########################################################################
    # Compare to ECG heart rate                                             #
    #########################################################################

    ecgHR = getEcgHR(ecg, windowSize)[:ppgHR.size]

    print("PPG HRs")
    print(ppgHR)

    print("ECG HRs")
    print(ecgHR)
    
    errors = np.abs(ppgHR - ecgHR)
    errors = errors[6:] # remove errors from start of signal

    print(errors)
    print(np.average(errors))


