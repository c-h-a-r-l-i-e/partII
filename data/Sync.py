"""
Class designed to synchronize data collected from a smart watch and data collected from a portable
ECG.
"""
import pyedflib
import WatchData
import sys
import numpy as np
import matplotlib.pyplot as plt


class Sync:
    """
    Initialize synchronization class, provided the EDF file from the portable ECG and the directory
    containing the data from a smart watch.
    """
    def __init__(self, ecgFile, watchDirectory):
        self.ecgFile = pyedflib.EdfReader(ecgFile)
        self.watchData = WatchData.WatchData(watchDirectory)


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

    def getWatch_y(self):
        # Get a pandas dataframe
        df = self.watchData.getAcceleration()
        y = df['y']
        return y

    def getWatch_freq(self):
        df = self.watchData.getAcceleration()
        time = df['time']
        size = len(time)

        # Calculate start and end time in seconds
        startTime = time[0] / 1000
        endTime = time[size - 1] / 1000
        freq = size / (endTime - startTime)
        return freq


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
    The two methods below return a numpy array containing acceleration along the appropriate up axis, sampled at the same rate (the ECG rate).
    """
    def getWatchAccelUp(self):
        watchFreq = self.getWatch_freq()
        ecgFreq = self.getECG_freq()
        watchY = self.getWatch_y().to_numpy()
        watchY = self.resample(watchY, watchFreq, ecgFreq)
        watchY = -self.normalize(watchY)
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
    """
    def getSyncedSignals(self):
        # Get ECG signal and frequency
        labels = self.ecgFile.getSignalLabels()
        pos = labels.index("ECG")
        ecgFreq = self.ecgFile.getSampleFrequency(pos)
        print(ecgFreq)
        ecgSignal = self.ecgFile.readSignal(pos)

        # Get PPG signal resampled at the ECG signal's rate
        ppg = self.watchData.getPPG()
        ppgSignal = ppg['value'].to_numpy()
        time = ppg['time'].to_numpy()
        ppgFreq = (time[time.size-1] - time[0]) / time.size / 2
        ppgSignal = self.resample(ppgSignal, ppgFreq, ecgFreq)

        ppgSignal = self.normalize(ppgSignal)
        ecgSignal = self.normalize(ecgSignal)

        timeDiff = self.getTimeDifference()
        delta = int(timeDiff * ecgFreq)

        # timeDiff > 0 means ecg started sooner
        if timeDiff > 0:
            ecgSignal = ecgSignal[delta:]
        else:
            ppgSignal = ppgSignal[delta:]
        
        return ecgSignal, ppgSignal, ecgFreq


    def plotCrossCorrelation(self):
        watchCorrelation = (self.getCrossCorrelation(watchFirst=True))
        ecgCorrelation = (self.getCrossCorrelation(watchFirst=False))

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

    def plotSyncedAccelerometer(self):
        delta = int(self.getTimeDifference() * self.getFrequency())
        watch = self.getWatchAccelUp()
        ecg = self.getECGAccelUp()
        if delta > 0:
            ecg = ecg[delta:]
        else:
            watch = watch[-delta:]

        xs = np.arange(0,watch.size/self.getFrequency(),1/self.getFrequency())
        plt.plot(xs, watch, label="Watch")
        xs = np.arange(0,ecg.size/self.getFrequency(),1/self.getFrequency())
        plt.plot(xs, ecg, label="ECG", color='orange')
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration")
        plt.title("Acceleration after syncing")
        plt.legend()


    def plotSyncedHeart(self):
        ecg, ppg, freq = self.getSyncedSignals()

        xs = np.arange(0, ppg.size/freq, 1/freq)
        plt.plot(xs, ppg, label="Watch PPG")
        xs = np.arange(0, ecg.size/freq, 1/freq)
        plt.plot(xs, ecg, label="ECG", color='orange')
        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.title("Heart-rate sensors after syncing")
        plt.legend()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    sync = Sync(ecgFile, watchDirectory)
    sync.plotSyncedAccelerometer()
    plt.show()
    sync.plotSyncedHeart()
    plt.show()

