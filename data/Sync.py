"""
Class designed to synchronize data collected from a smart watch and data collected from a portable
ECG.
"""
import pyedflib
import WatchData
import sys

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
        print(data)

    def test(self):
        print(self.watchData.getPPG())
        print(self.ecgFile.getSignalLabels())



if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    sync = Sync(ecgFile, watchDirectory)
    sync.test()
    sync.getECG_x()


