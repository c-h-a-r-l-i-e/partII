import pyedflib
import data
import heartpy as hp

def getEcgData(ecgFilePath):
    return EcgData(ecgFilePath)


class EcgData:
    def __init__(self, ecgFilePath):
        self.ecgFile = pyedflib.EdfReader(ecgFilePath)
        self.labels = self.ecgFile.getSignalLabels()

    def getAcceleration(self, axis):
        if not axis.upper() in ['X','Y','Z']:
            raise ValueError("Argument axis must be one of x, y or z.")

        pos = self.labels.index("Accelerometer_{}".format(axis.upper()))
        freq = self.ecgFile.getSampleFrequency(pos)
        signal = self.ecgFile.readSignal(pos)
        ecg = signal.getSignal(signal, freq)
        return ecg


    def getECG(self):
        pos = self.labels.index("ECG")
        freq = self.ecgFile.getSampleFrequency(pos)
        signal = self.ecgFile.readSignal(pos)
        ecg = data.getSignal(signal, freq)
        return ecg

    # Calculate the heartrate from the ECG. Algorithm works by splitting the
    # signal into windows (of length window seconds) and calculating the HR
    # in each window. Returns a numpy array, of HR values.

            









