import numpy as np
import matplotlib.pyplot as plt

def getSignal(values, frequency):
    return Signal(values, frequency)


class Signal():
    def __init__(self, values, frequency):
        self.vals = values.copy()
        self.freq = frequency

    def getValues(self):
        return self.vals.copy()

    def getFrequency(self):
        return self.freq

    def plot(self, label=""):
        xs = np.arange(0, self.vals.size/self.freq, 1/self.freq)[:self.size]
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
            return getSignal(resampled, freq)

        else:
            raise ValueError("Unknown resampling method {}".format(method))


    def crop(self, length):
        values = self.getValues()[:length]
        newSignal = getSignal(values, self.freq)
        return newSignal

    def __getitem__(self, key):
        item = self.vals[key] 

        if item.size == 1:
            return item

        return getSignal(item, self.freq)


    def __setitem__(self, key, item):
        self.vals[key] = item

    def __delitem__(self, key):
        self.vals.__delitem__(key)

    @property
    def size(self):
        return self.vals.size

    @property
    def frequency(self):
        return self.freq

    @property
    def values(self):
        return self.vals.copy()
