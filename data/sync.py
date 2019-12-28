"""
Class designed to synchronize data collected from a smart watch and data collected from a portable
ECG.
"""
import pyedflib
import watchdata
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
from heartplot import plot_signal


def getSync(ecgFilePath, watchDirectoryPath):
    sync = Sync(ecgFilePath, watchDirectoryPath)
    return sync

class Sync:
    """
    Initialize synchronization class, provided the EDF file from the portable ECG and the directory
    containing the data from a smart watch.
    """
    def __init__(self, ecgFile, watchDirectory):
        self.ecgFile = pyedflib.EdfReader(ecgFile)
        self.watchData = watchdata.getWatchData(watchDirectory)


    def getECG_x(self):
        labels = self.ecgFile.getSignalLabels()
        pos = labels.index("Accelerometer_X")
        data = self.ecgFile.readSignal(pos) 
        return data

    def getECG_freq(self):
        labels = self.ecgFile.getSignalLabels()
        pos = labels.index("Accelerometer_X")
        freq = self.ecgFile.getSampleFrequency(pos)
        return freq


    """
    Resample a given numpy array signal from currentFreq (hz) to newFreq (hz).
    """
    def resample(self, signal, currentFreq, newFreq):
        resampled = np.interp(np.arange(0, signal.size, currentFreq/newFreq), np.arange(0, signal.size, 1), signal)

        return resampled

    def normalize(self, signal):
        mean = np.mean(signal)
        signal -= mean
        amplitude = np.absolute(signal).max()
        signal /= amplitude
        return signal

    """
    The two methods below return a numpy array containing acceleration along 
    the appropriate up axis, sampled at the same rate (the ECG rate).
    """
    def getWatchAccelUp(self):
        ecgFreq = self.getECG_freq()
        watchY, watchFreq = self.watchData.getAcceleration('y')
        watchY = self.resample(watchY, watchFreq, ecgFreq)
        watchY = self.normalize(watchY)
        return watchY

    def getECGAccelUp(self):
        ecgX = self.normalize(self.getECG_x())
        return ecgX

    def getFrequency(self):
        return self.getECG_freq()


    """
    Calculate cross correlation of the signals.
    Parameters:
        - watchFirst = which signal (watch or ecg) is assumed to have started earlier. 
        - timeLimit = the time in which you expect to be able to sync data. E.g. the time in which three jumps happen.
    """
    def getCrossCorrelation(self, watchFirst=True, timeLimit=120):
        watch = self.getWatchAccelUp()
        ecg = self.getECGAccelUp()
        numSamples = int(timeLimit * self.getFrequency())
        if watchFirst:
            correlation = np.correlate(ecg[:numSamples*2], watch[:numSamples], mode='valid')
        else:
            correlation = np.correlate(watch[:numSamples*2], ecg[:numSamples], mode='valid')
        return correlation

    """
    Calculate time difference (in seconds) between ecg starting and watch starting. If time difference 
    is positive, the watch started first, if negative the ECG started first.
    """
    def getTimeDifference(self):
        # Take absolute values of cross correlation, as signals may be inverted so cross correlation negative. We take
        # cross correlation assuming both watch started recording first and ecg started recording first in order to find
        # the maximum cross correlation between them.
        watchCorrelation = np.absolute(self.getCrossCorrelation(watchFirst=True))
        ecgCorrelation = np.absolute(self.getCrossCorrelation(watchFirst=False))

        if watchCorrelation.max() > ecgCorrelation.max():
            delta = np.argmax(watchCorrelation)
        else:
            delta = -np.argmax(ecgCorrelation)

        timeDiff = delta / self.getFrequency()
        return timeDiff

    """
    Returns three values (ecg,ppg,fs) containing the signals, synchronized and at frequency fs
    ppgSensor describes which light sensor we use to get the signal (can be 1 or 2)
    """
    def getSyncedSignals(self, ppgSensor=1):
        # Get ECG signal and frequency
        labels = self.ecgFile.getSignalLabels()
        pos = labels.index("ECG")
        ecgFreq = self.ecgFile.getSampleFrequency(pos)
        ecgSignal = self.ecgFile.readSignal(pos)

        # Get PPG signal resampled at the ECG signal's rate
        ppgSignal, ppgFreq = self.watchData.getPPG(sensor=ppgSensor)
        ppgSignal = self.resample(ppgSignal, ppgFreq, ecgFreq)

        ppgSignal = self.normalize(ppgSignal)
        ecgSignal = self.normalize(ecgSignal)

        timeDiff = self.getTimeDifference()
        delta = int(abs(timeDiff) * ecgFreq)

        # timeDiff > 0 means ecg started sooner
        if timeDiff > 0:
            ecgSignal = ecgSignal[delta:]
        else:
            ppgSignal = ppgSignal[delta:]
            
        return ecgSignal, ppgSignal, ecgFreq

    """
    Return the synced ppgSignal, at it's original frequency
    """ 
    def getSyncedPpgOriginalFreq(self, ppgSensor=1):
        ppgSignal, ppgFreq = self.watchData.getPPG(sensor=ppgSensor)

        timeDiff = self.getTimeDifference()
        delta = int(abs(timeDiff) * ppgFreq)

        # timeDiff < 0 means ppg started sooner
        if timeDiff < 0:
            ppgSignal = ppgSignal[delta:]
            
        return ppgSignal, ppgFreq


def plotCrossCorrelation(data):
    watchCorrelation = (data.getCrossCorrelation(watchFirst=True))
    ecgCorrelation = (data.getCrossCorrelation(watchFirst=False))

    xs = np.linspace(0,120,watchCorrelation.size)
    plt.subplot(1,2,1)
    plt.plot(xs, watchCorrelation)
    plt.xlabel("Time (s)")
    plt.ylabel("Cross-correlation")
    plt.title("Cross-correlation moving ECG acceleration")
    plt.axis([0,120,-6,65])
    plt.subplot(1,2,2)
    plt.plot(xs, ecgCorrelation)
    plt.xlabel("Time (s)")
    plt.ylabel("Cross-correlation")
    plt.axis([0,120,-6,65])
    plt.title("Cross-correlation moving watch acceleration")
    plt.show()

def plotSyncedAccelerometer(data):
    delta = int(data.getTimeDifference() * data.getFrequency())
    watch = data.getWatchAccelUp()
    ecg = data.getECGAccelUp()
    if delta > 0:
        ecg = ecg[delta:]
    else:
        watch = watch[-delta:]

    xs = np.arange(0,watch.size/data.getFrequency(),1/data.getFrequency())
    plt.plot(xs, watch, label="Watch")
    xs = np.arange(0,ecg.size/data.getFrequency(),1/data.getFrequency())
    plt.plot(xs, ecg, label="ECG", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration")
    plt.title("Acceleration after syncing")
    plt.legend()


def plotsyncedheart(data):
    ecg, ppg, freq = data.getsyncedsignals()

    xs = np.arange(0, ppg.size/freq, 1/freq)
    plt.plot(xs, ppg, label="watch ppg")
    xs = np.arange(0, ecg.size/freq, 1/freq)
    plt.plot(xs, ecg, label="ecg", color='orange')
    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("heart-rate sensors after syncing")
    plt.legend()

def plotsyncedheart_twoSensors(data):
    ecg, ppg, freq = data.getsyncedsignals()
    _, ppg2, _ = data.getsyncedsignals(ppgSensor=2)

    xs = np.arange(0, ppg.size/freq, 1/freq)
    plt.plot(xs, ppg, label="watch ppg sensor 1")
    xs = np.arange(0, ppg2.size/freq, 1/freq)
    plt.plot(xs, ppg2, label="watch ppg sensor 2")
    xs = np.arange(0, ecg.size/freq, 1/freq)
    plt.plot(xs, ecg, label="ecg", color='orange')
    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("heart-rate sensors after syncing")
    plt.legend()

def plotTwoPpg(watchData):
    ppg1, freq1 = watchData.getPPG(sensor=1)
    ppg2, freq2 = watchData.getPPG(sensor=2)

    plot_signal(ppg1, freq1, "blue", "PPG Sensor 1")
    plot_signal(ppg2, freq2, "orange", "PPG Sensor 2")

    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("Comparison of PPG sensors")
    plt.legend()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    watchData = watchdata.getWatchData(watchDirectory)
    plotTwoPpg(watchData)
    plt.show()

    sync = getSync(ecgFile, watchDirectory)
    plotSyncedAccelerometer(sync)
    plt.show()
    plotSyncedHeart(sync)
    plt.show()
