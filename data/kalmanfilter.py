import numpy as np

class Filter():
    def __init__(self, peaks, freq, mean=60, var=100, step=1):
        """
        Initiate class

        Params
        ---------
        peaks : ndarray
            A list of peak positions, in terms of which sample the peak is at

        freq : ndarray
            Frequency of the signal
        """
        self.peaks = peaks
        self.freq = freq

        # Assume heartbeat = 60 bpm with low confidence initially
        self.mean = mean
        self.var = var
        self.step = step
        self.t = 0

    def sim_time_step():
        if self.peaks.size > self.freq * (self.time + self.step):

    def update(self, mean, var):
        self.mean = (var * self.mean + self.var * mean) / (self.var + var)
        self.var = 1/(1/self.var + 1/var)


    def predict(self, mean, var):
        self.mean += mean
        self.var += var


    def filter():
        mean = 60
        var = 100

        for i in :
            mean, var = predict(mean, var, 0, 2)

            if hb available:
                mean, var = update(mean, var, hb, 3)


