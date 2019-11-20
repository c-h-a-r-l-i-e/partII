"""
Helper class to aid extraction of data from information downloaded from the watch.
"""
import pandas
import os.path

class WatchData:
    """
    Constructor, takes directory in which data files for the recording can be found.
    """
    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError("Directory {} does not exist".format(directory))
        self.directory = directory
        

    def getPPG(self):
        df = pandas.read_csv(os.path.join(self.directory, "ppg.csv"))
        return df

    def getAccelerometer(self):
        df = pandas.read_csv(os.path.join(self.directory, "accelerometer.csv"))
        return df

    def getAccelerometer(self):
        df = pandas.read_csv(os.path.join(self.directory, "rotation.csv"))
        return df

