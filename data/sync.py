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
import matplotlib as mpl
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
    k : int
        k is the time at which we think the signals are synced, given in terms of the number of samples through f we are.
        i.e. the value of k which maximizes c[k]

    v : float
        the value of cross correlation at that point (c[k])
    """
    if f.size < g.size:
        raise ValueError("Array f must be larger than g")

    length = f.size - g.size

    c = np.zeros((length))
    for k in range(length):
        # Vectorized solution to sum_n(f[n+k] * g[n])
        c[k] = np.sum(f[k : k + g.size] * g)

    k = np.argmax(c)
    v = c[k]

    return (k, v)

def fastCorrelate(f, g, freq, initTimeGap = 0.25, searchBound = 3):
    """
    Calculate cross correlation c of two numpy arrays, as defined by c[k] = sum_n (f[n+k] * g[n])
    using optimized method which does an initial correlation at a lower resolution and then hones in on the solution.

    Parameters
    ----------
    f, g : numpy arrays
        Input signals.

    freq : float
        The frequency of the signals.

    initTimeGap : float
        Interval at which to perform correlation intially in seconds. 

    searchBound : float
        Bound wihtin which we search for the solution once we have made an initial pass.
        

    Returns
    -------
    k : int
        k is the time at which we think the signals are synced, given in terms of the number of samples through f we are.
        i.e. the value of k which maximizes c[k]

    v : float
        the value of cross correlation at that point (c[k])
    """
    if f.size < g.size:
        raise ValueError("Array f must be larger than g")

    length = f.size - g.size

    gap = int(initTimeGap * freq)

    c = np.zeros((length))
    for k in range(0, length, gap):
        c[k] = np.sum(f[k : k + g.size] * g)

    maxPos = np.argmax(c)
    bound = searchBound * freq
    lowerBound = max(maxPos - bound, 0)
    upperBound = min(maxPos + bound, length)
    for k in range(lowerBound, upperBound, 1):
        c[k] = np.sum(f[k : k + g.size] * g)


    k = np.argmax(c)
    v = c[k]

    return (k, v)


def testCorrelation():

    ecgFile = "ecg-files/DATA/20200118/13-55-42.EDF"
    watchDirectory = "files/recordings/2020-01-18/14.07.45.306/"

    sync = getSync(ecgFile, watchDirectory)
    
    freq = sync.getECG_freq()

    f = sync._getWatchAccelUp()

    g = sync._getECGAccelUp()

    print(correlate(f[:120*freq], g))

    print(fastCorrelate(f[:120*freq], g, freq))





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
        self.startCrop = 120
        self.endCrop = 30

    def setStartCrop(self, crop):
        self.startCrop = crop

    def setEndCrop(self, crop):
        self.endCrop = crop

    def getECG_x(self):
        signal = self.ecgData.getAcceleration("x")
        return signal.getValues()

    def getECG_freq(self):
        signal = self.ecgData.getAcceleration("x")
        return signal.getFrequency()

    def getPPGLength(self):
        """
        Get length in seconds of PPG data
        """
        return self.watchData.getPPG().getValues().size / self.watchData.getPPG().getFrequency()
        
        


    """
    Resample a given numpy array signal from currentFreq (hz) to newFreq (hz).
    """
    def resample(self, signal, currentFreq, newFreq):
        resampled = np.interp(np.arange(0, signal.size, currentFreq/newFreq),
                np.arange(0, signal.size, 1), signal)

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
    def _getWatchAccelUp(self):
        ecgFreq = self.getECG_freq()
        watchY = self.watchData.getAcceleration('y').getValues()
        watchFreq = self.watchData.getAcceleration('y').getFrequency()
        watchY = self.resample(watchY, watchFreq, ecgFreq)
        watchY = self.normalize(watchY)
        freq = self.watchData.getAcceleration('y').getFrequency()
        return watchY

    def _getECGAccelUp(self):
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
        watch = self._getWatchAccelUp()
        ecg = self._getECGAccelUp()
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


    def crop(self, signal):
        """
        Crops signal to between startCrop seconds from the start and endCrop from the end.

        Parameters
        -------------
         - signal: data.Signal
           The signal we want to crop 
           
        Returns
        -------------
         - out: data.Signal
           Cropped signal
        """
        values = signal.getValues()
        freq = signal.getFrequency()

        values = values[int(freq*self.startCrop) : -int(freq*self.endCrop)]
        return data.getSignal(values, freq)



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

        # timeDiff > 0 means ecg started earlier than watch
        if timeDiff > 0:
            delta = int(abs(timeDiff) * ecgFreq)
            ecgSignal = ecgSignal[delta:]
        else:
            delta = int(abs(timeDiff) * ppgFreq)
            ppgSignal = ppgSignal[delta:]

        ecg = self.crop(data.getSignal(ecgSignal, ecgFreq))
        ppg = self.crop(data.getSignal(ppgSignal, ppgFreq))
            
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

        ecg = self.crop(data.getSignal(ecgSignal, ecgFreq))
        ppg = self.crop(data.getSignal(ppgSignal, ecgFreq))
            
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

        # timeDiff < 0 means watch started sooner
        if timeDiff < 0:
            ppgSignal = ppgSignal[delta:]

        ppg = self.crop(data.getSignal(ppgSignal, ppgFreq))
            
        return ppg


    def getSyncedECG(self):
        """
        Return the synced ECG signal

        Returns
        -------
        ecg : Signal object
            The ECG signal, after being synced with the wristwatch
        """
        # Get ECG signal and frequency
        ecg = self.ecgData.getECG()
        ecgFreq = ecg.getFrequency()
        ecgSignal = ecg.getValues()
        ecgSignal = self.normalize(ecgSignal)

        timeDiff = self.getTimeDifference()
        delta = int(abs(timeDiff) * ecgFreq)

        # timeDiff > 0 means ecg started sooner
        if timeDiff > 0:
            ecgSignal = ecgSignal[delta:]

        ecg = self.crop(data.getSignal(ecgSignal, ecgFreq))
            
        return ecg


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

        # timeDiff < 0 means watch started sooner
        if timeDiff < 0:
            accValues = accValues[delta:]

        synced = self.crop(data.getSignal(accValues, accFreq))
        return synced


def plotCrossCorrelation(data):
    watchCorrelation = np.abs(data.getCrossCorrelation(watchFirst=True))
    ecgCorrelation = np.abs(data.getCrossCorrelation(watchFirst=False))

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
    watch = data._getWatchAccelUp()
    ecg = -data._getECGAccelUp()
    if delta > 0:
        ecg = ecg[delta:]
    else:
        watch = watch[-delta:]

    xs = np.arange(0,watch.size/data.getFrequency(),1/data.getFrequency())[:watch.size]
    plt.plot(xs, watch, label="Watch")
    xs = np.arange(0,ecg.size/data.getFrequency(),1/data.getFrequency())[:ecg.size]
    plt.plot(xs, ecg, label="ECG", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration")
    plt.title("Acceleration after syncing")
    plt.legend()

def plotAccelerometer(data):
    watch = data._getWatchAccelUp()
    ecg = -data._getECGAccelUp()

    xs = np.arange(0,watch.size/data.getFrequency(),1/data.getFrequency())[:watch.size]
    plt.plot(xs, watch, label="Watch", color="orange")
    xs = np.arange(0,ecg.size/data.getFrequency(),1/data.getFrequency())[:ecg.size]
    plt.plot(xs, ecg, label="ECG", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration")
    plt.title("Acceleration before syncing")
    plt.legend()


def plotSyncedHeart(data):
    ecg, ppg = data.getSyncedSignals()

    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("Heart-rate sensors")

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
    signal = signal.normalize()
    fs = signal.getFrequency()
    vals = signal.getValues()

    fig, ax = plt.subplots() 
    f, t, Sxx = scipy.signal.spectrogram(vals, fs, nfft=400)
    pc = ax.pcolormesh(t, f, Sxx, norm=mpl.colors.LogNorm(vmin=Sxx.min(), vmax=Sxx.max()), cmap='inferno')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [sec]')
    fig.colorbar(pc)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    watchData = watchdata.getWatchData(watchDirectory)

    sync = getSync(ecgFile, watchDirectory)

    plotAccelerometer(sync)
    plt.show()

    plotSyncedHeart(sync)
    plt.show()

    plotSpectrum(sync.getSyncedSignals()[1])
    plt.show()

    plotAccelerometer(sync)
    plt.show()

    plotSyncedAccelerometer(sync)
    plt.show()
    
    plotSyncedHeart_twoSensors(sync)
    plt.show()

    plotSpectrum(sync.getSyncedSignals()[1])
    plt.show()

    plotSyncedHeart_twoSensors(sync)
    plt.show()
