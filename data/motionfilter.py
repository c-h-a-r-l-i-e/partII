import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import sys
import sync
import filtering
import data

"""
Use an adaptive filter to remove noise caused by (and hence correlating
with) referenceMotion, from signal.
"""
def adaptiveFilter(signal, referenceMotion):
    # Sample referenceMotion at signal's frequency
    freq = signal.getFrequency()
    referenceMotion = referenceMotion.resample(freq)
    referenceMotion = referenceMotion.crop(signal.size)

    M = 1000 # Num of filter taps
    step = 0.1 # Step size

    y, e, w = adf.nlms(referenceMotion.getValues(), signal.getValues(), 
            M, step, returnCoeffs=True)

    filtered = data.getSignal(y, freq)
    return filtered


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: motionfilter.py ecgFile " +
                "watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.getSync(ecgFile, watchDirectory)

    ecg, ppg = synced.getSyncedSignals()

    lowerBPM = 24
    upperBPM = 240
    butterFiltered = filtering.butter_bandpass_filter(
        ppg,lowerBPM/60, upperBPM/60).normalize()

    accelerationX = synced.getSyncedAcceleration('x')
    motionFiltered = adaptiveFilter(butterFiltered, accelerationX)

    accelerationY = synced.getSyncedAcceleration('y')
    motionFiltered = adaptiveFilter(motionFiltered, accelerationY)

    accelerationZ = synced.getSyncedAcceleration('z')
    motionFiltered = adaptiveFilter(motionFiltered, accelerationZ)

    ecg.plot("ECG")
    motionFiltered.plot("PPG Motion Filtered")
    #butterFiltered.plot("PPG Standard Filtering")
    plt.legend()
    plt.show()
