"""
Helper class to aid extraction of data from information downloaded from 
the watch.
"""
import pandas
import os.path
import data

def getWatchData(directory):
    return WatchData(directory)


class WatchData:
    """
    Constructor, takes directory in which data files for the recording can be
    found.
    """
    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError("Directory {} does not exist".format(directory))
        self.directory = directory
        
    
    """
    Return the PPG signal as a numpy array, along with its frequency (hz)
    """
    def getPPG(self, sensor=1):
        df = pandas.read_csv(os.path.join(self.directory, "ppg.csv"))
        sensor = "" if sensor==1 else str(sensor)
        ppg = df['value'+sensor].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = time.size / ((time[time.size-1] - time[0]) / 1000)
        return data.getSignal(ppg, freq)

    """
    Return the PPG signal as a numpy array, along with its frequency (hz)
    """
    @property
    def times(self):
        df = pandas.read_csv(os.path.join(self.directory, "ppg.csv"))
        time = df['time'].to_numpy()
        return time


    """
    Return an acceletation signal axis (x, y or z) as a signal object
    """
    def getAcceleration(self, axis):
        if not axis in ['x','y','z']:
            raise ValueError("Argument axis must be one of x, y or z.")

        df = pandas.read_csv(os.path.join(self.directory, 
            "accelerometer.csv"))
        signal = df[axis].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = time.size / ((time[time.size-1] - time[0]) / 1000)
        return data.getSignal(signal, freq)


    """
    Return the rotation signal axis (x, y or z) as a signal object 
    """
    def getRotation(self, axis):
        if not axis in ['x','y','z']:
            raise ValueError("Argument axis must be one of x, y or z.")

        df = pandas.read_csv(os.path.join(self.directory, "rotation.csv"))
        signal = df[axis].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = time.size / ((time[time.size-1] - time[0]) / 1000)
        return data.getSignal(signal, freq)

    """
    Return the heart-rate signal as a signal object
    also return the accuracy integers as a signal object
    """
    def getHR(self):
        df = pandas.read_csv(os.path.join(self.directory, "hr.csv"))
        hr = df['value'].to_numpy()
        accuracy = df['accuracy'].to_numpy()
        time = df['time'].to_numpy()

        # Calculate frequency in hz
        freq = 1
        return data.getSignal(hr, freq), data.getSignal(accuracy, freq)

