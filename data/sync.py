"""
Class designed to synchronize data collected from a smart watch and data collected from a portable
ECG.
"""
import pyedflib
import watchdata
import ecgdata
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import data
from spectrum import Periodogram

def correlate(f, g):
    """
    Calculate cross correlation c of two numpy arrays, as defined by c[k] = sum_n (f[n+k] * g[n])

    Parameters
    ----------
    f, g : numpy array
        Input signals.


    Returns
    -------
    c : numpy array
        Cross correlation of f and g.
    """
    if f.size < g.size:
        raise ValueError("Array f must be larger than g")

    length = f.size - g.size

    c = np.zeros((length))
    for k in range(length):
        # Vectorized solution to sum_n(f[n+k] * g[n])
        c[k] = np.sum(f[k : k + g.size] * g)

    return c


def getSync(ecgFilePath, watchDirectoryPath):
    sync = Sync(ecgFilePath, watchDirectoryPath)
    return sync


class Sync:
    """
    Initialize synchronization class, provided the EDF file from the portable ECG and the directory
    containing the data from a smart watch.
    """
    def __init__(self, ecgFile, watchDirectory):
        self.ecgData = ecgdata.getEcgData(ecgFile)
        self.watchData = watchdata.getWatchData(watchDirectory)


    def getECG_x(self):
        signal = self.watchData.getAcceleration("x")
        return signal.getValues()

    def getECG_freq(self):
        signal = self.watchData.getAcceleration("x")
        return signal.getFrequency()


    """
    Resample a given numpy array signal from currentFreq (hz) to newFreq (hz).
    """
    def resample(self, signal, currentFreq, newFreq):
        resampled = np.interp(np.arange(0, signal.size, currentFreq/newFreq),
                np.arange(0, signal.size, 1), signal)

        return resampled

    def normalize(self, signal):
        if False: # TODO: pretty self explanitory
            newsignal = signal.copy()
            amplitude = np.absolute(newsignal).max()
            newsignal /= amplitude
            print("normalize doesn't loose accuracy: {}".format(np.all(signal == newsignal*amplitude)))

            print(signal[0])
            print(newsignal[0]*amplitude)
        
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
        watchY = self.watchData.getAcceleration('y').getValues()
        watchFreq = self.watchData.getAcceleration('y').getFrequency()
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
    Returns two values (ecg,ppg) containing the signals, synchronized 
    and at their original frequency.
    ppgSensor describes which light sensor we use to get the signal (can 
    be 1 or 2)
    """
    def getSyncedSignals(self, ppgSensor=1):
        # Get ECG signal and frequency
        ecg = self.ecgData.getECG()
        ecgFreq = ecg.getFrequency()
        ecgSignal = ecg.getValues()

        ppg = self.watchData.getPPG(sensor=ppgSensor)
        ppgFreq = ppg.getFrequency()
        ppgSignal = ppg.getValues()

        ppgSignal = self.normalize(ppgSignal)
        ecgSignal = self.normalize(ecgSignal)

        timeDiff = self.getTimeDifference()

        # timeDiff > 0 means ecg started sooner
        if timeDiff > 0:
            delta = int(abs(timeDiff) * ecgFreq)
            ecgSignal = ecgSignal[delta:]
        else:
            delta = int(abs(timeDiff) * ppgFreq)
            ppgSignal = ppgSignal[delta:]

        ecg = data.getSignal(ecgSignal, ecgFreq)
        ppg = data.getSignal(ppgSignal, ppgFreq)
            
        return ecg, ppg

    """
    Returns two values (ecg,ppg) containing the signals, synchronized 
    and at frequency of ECG. 
    ppgSensor describes which light sensor we use to get the signal (can be 
    1 or 2)
    """
    def getSyncedSignalsHighFrequency(self, ppgSensor=1):
        # Get ECG signal and frequency
        ecg = self.ecgData.getECG()
        ecgFreq = ecg.getFrequency()
        ecgSignal = ecg.getValues()

        # Get PPG signal resampled at ECG's frequency
        ppg = self.watchData.getPPG(sensor=ppgSensor)
        ppgFreq = ppg.getFrequency()
        ppgSignal = ppg.getValues()
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

        ecg = data.getSignal(ecgSignal, ecgFreq)
        ppg = data.getSignal(ppgSignal, ecgFreq)
            
        return ecg, ppg


    """
    Return the synced ppgSignal, at it's original frequency
    """ 
    def getSyncedPPG(self, ppgSensor=1):
        ppg = self.watchData.getPPG(sensor=ppgSensor)
        ppgFreq = ppg.getFrequency()
        ppgSignal = ppg.getValues()
        ppgSignal = self.normalize(ppgSignal)

        timeDiff = self.getTimeDifference()
        delta = int(abs(timeDiff) * ppgFreq)

        # timeDiff < 0 means ppg started sooner
        if timeDiff < 0:
            ppgSignal = ppgSignal[delta:]

        ppg = data.getSignal(ppgSignal, ppgFreq)
            
        return ppg


    """
    Return the synced acceleration of the wristwatch, along parameter axis.
    """
    def getSyncedAcceleration(self, axis):
        acc = self.watchData.getAcceleration(axis)
        acc = acc.normalize()
        accFreq = acc.getFrequency()
        accValues = acc.getValues()

        timeDiff = self.getTimeDifference()
        delta = int(abs(timeDiff) * accFreq)

        # timeDiff < 0 means ppg started sooner
        if timeDiff < 0:
            accValues = accValues[delta:]

        synced = data.getSignal(accValues, accFreq)
        return synced


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


def plotSyncedHeart(data):
    ecg, ppg = data.getSyncedSignals()

    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("heart-rate sensors after syncing")

    ppg.plot("Watch PPG")
    ecg.plot("ECG")
    plt.legend()


def plotSyncedHeart_twoSensors(data):
    ecg, ppg = data.getSyncedSignals()
    ppg2 = data.getSyncedPPG(ppgSensor=2)

    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("heart-rate sensors after syncing")

    ppg.plot("Watch PPG sensor 1")
    ppg2.plot("Watch PPG sensor 2")
    ecg.plot("ECG sensor")
    plt.legend()

def plotSpectrum(signal):
    signal.plot()
    plt.show()
    fs = signal.getFrequency()
    vals = signal.getValues()

    f, t, Sxx = scipy.signal.spectrogram(vals, fs, nfft=1000)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    watchData = watchdata.getWatchData(watchDirectory)

    sync = getSync(ecgFile, watchDirectory)

    plotSpectrum(sync.getSyncedPPG())
    plt.show()


    plotSyncedAccelerometer(sync)
    plt.show()
    plotSyncedHeart_twoSensors(sync)
    plt.show()
