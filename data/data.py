import numpy as np
import matplotlib.pyplot as plt

def getSignal(values, frequency):
    return Signal(values, frequency)


class Signal:
    def __init__(self, values, frequency):
        self.vals = values
        self.size = values.size
        self.freq = frequency

    def getValues(self):
        return self.vals.copy()

    def getFrequency(self):
        return self.freq

    def plot(self, label=""):
        xs = np.arange(0, self.vals.size/self.freq, 1/self.freq)
        plt.plot(xs, self.vals, label=label)

    def normalize(self):
        newVals = self.vals
        mean = np.mean(newVals)
        newVals -= mean
        amplitude = np.absolute(newVals).max()
        newVals /= amplitude
        return getSignal(newVals, self.freq)

    def resample(self, freq, method="linear"):
        if method == "linear":
            resampled = np.interp(
                    np.arange(0, self.vals.size, self.freq/freq),
                    np.arange(0, self.vals.size, 1),
                    self.vals)
            return getSignal(resampled, self.freq)

        else:
            raise ValueError("Unknown resampling method {}".format(method))


    def crop(self, length):
        values = self.getValues()[:length]
        newSignal = getSignal(values, self.freq)
        return newSignal
