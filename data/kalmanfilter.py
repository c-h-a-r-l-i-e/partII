import numpy as np
import data
import earbuds
import matplotlib.pyplot as plt
import sys

class Filter():
    def __init__(self, ear, watch, predict_var=0.1, ear_noise=0.01):
        """
        Initiate class

        Params
        ---------
         - ear : the hr signal recorded within the ear

         - watch : the hr signal recorded on the wrist

         - predict_var : the amount of additive variance to add for the prediction step

         - ear_noise : the amount of additive variance to add for the ear correct step
        """

        self.ear = ear
        self.watch = watch
        self.predict_var = predict_var
        self.size = min(ear.size, watch.size)
        self.ear_noise = ear_noise


    def predict(self, t, old_hr, old_var):
        if t < 1:
            raise ValueError("Predict step must start at time t > 0")

        # calculate hr difference between t-1 and t on the watch
        diff = self.watch[t] - self.watch[t-1]

        hr = old_hr + diff
        var = old_var + self.predict_var

        return hr, var


    def correct(self, t, predicted_hr, predicted_var):
        # Calculate Kalman gain
        k = predicted_var  / (predicted_var + self.ear_noise)

        # Calculate new hr and variance
        hr = predicted_hr + k * (self.ear[t] - predicted_hr)
        var = (1 - k) * predicted_var

        return hr, var


    def filter(self):
        hrs = np.zeros(self.size)

        # Initial step, wait until we get some data from the ear sensor before starting the filter
        t_min = 1
        while self.ear[t_min] == 0:
            t_min += 1

        hr = self.ear[t_min]
        var = self.ear_noise

        # Run the Kalman filter
        for t in range(t_min, self.size):
            hr, var = self.predict(t, hr, var)

            if self.ear[t] != 0:
                hr, var = self.correct(t, hr, var)

            hrs[t] = hr

        return data.Signal(hrs, 1)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        earbud_dir = sys.argv[3]
    elif len(sys.argv) == 3:
        earbud_dir = None
    else:
        raise ValueError("Expected usage: kalmanfilter.py ecgFile watchDir (earbudDir)")

    ecgfile = sys.argv[1]
    watchdir= sys.argv[2]
    sync = earbuds.Sync(ecgfile, watchdir, earbud_dir)

    f = Filter(sync.ear, sync.hr)
    filtered = f.filter()
    filtered.plot("Kalman Filtered")

    earbuds.plot_ecg(sync.ecg)
    sync.ear.plot("Earbud")
    sync.hr.plot("Watch HR")


    plt.legend()
    plt.show()

    
