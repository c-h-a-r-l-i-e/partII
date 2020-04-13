import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import timeit
import testsyncs
import heartpy as hp

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import filtering
import data
import motionfilter
import peakfind
import csv


def test_validity(ax1, ax2, method, label, step=0.1, nlms=True, filterx=False, filtery=False, filterz=False, taps=20, noise=testsyncs.NOISE_LOW):
    """
    Method is one of 'sd' or 'naive'.
    """
    segmentsize = 20
    ppgs, ecgs, accxs, accys, acczs = testsyncs.getSegmentsAtNoise(noise, segmentsize)

    average_error = 0
    errors = np.zeros(len(ppgs))
    for i in range(len(ppgs)):
        # Remove unrelated noise
        ppg = filtering.butter_bandpass_filter(ppgs[i], 0.4, 4, order=2)

        # Apply motion filter to each axis dependant on filter parameters
        filtered = ppg
        if filterx:
            accx = filtering.butter_bandpass_filter(accxs[i], 0.4, 4, order=2)
            filtered = motionfilter.adaptiveFilter(filtered, accx, step, nlms, M=taps)
        if filtery:
            accy = filtering.butter_bandpass_filter(accys[i], 0.4, 4, order=2)
            filtered = motionfilter.adaptiveFilter(filtered, accy, step, nlms, M=taps)
        if filterz:
            accz = filtering.butter_bandpass_filter(acczs[i], 0.4, 4, order=2)
            filtered = motionfilter.adaptiveFilter(filtered, accz, step, nlms, M=taps)
        
        # Calculate heart-rate from filtered signal, and compare to ECG heart-rate
        if method == 'sd':
            filteredpeaks = peakfind.find_peaks_min_sd(filtered)
        elif method == 'naive':
            filteredpeaks = peakfind.find_peaks(filtered)
        else:
            raise ValueError("Invalid method")
        filteredrate = filteredpeaks.size / segmentsize * 60

        ecgvals = ecgs[i].getValues()
        filtered_ecg = hp.remove_baseline_wander(ecgvals, ecgs[i].getFrequency())
        wd, m = hp.process(hp.scale_data(filtered_ecg), ecgs[i].getFrequency())
        ecgrate = m["bpm"]

        errors[i] = filteredrate - ecgrate
        average_error += np.abs(ecgrate - filteredrate) / len(ppgs)

        #print("filtered PPG : {}, ecg : {}".format(filteredrate, ecgrate))

    # plot cdf
    xs = np.sort(errors)
    ys = np.arange(1, len(ppgs) + 1, 1) / len(ppgs)

    print("{} --> average error = {}".format(label, average_error/len(ppgs))) 

    #plt.figure(num="step={},nlms={},taps={}".format(step, nlms, taps))
    ax1.plot(xs, ys, label=label)

    xs = np.sort(np.abs(errors))
    
    ax2.plot(xs, ys, label=label)


def test_time(method):
    setup = """import testsyncs
syncs = testsyncs.getSyncs()
import os
s = syncs[0]
ecg, ppg = s.getSyncedSignals()
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import peakfind"""

    if method == "sd":
        test = """peakfind.find_peaks_min_sd(ppg)"""
    elif method == "naive":
        test = """peakfind.find_peaks(ppg)"""
    time = timeit.timeit(setup=setup, stmt=test, number=1000)
    print("time with method {}, is {}".format(method, time))


def plot_validity():
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    for method in ['sd', 'naive']:
        if method == 'sd':
            label = 'Standard Deviation Minimization'
        if method == 'naive':
            label = 'Local Maxima'
        test_validity(ax1, ax2, method, label)

    ax1.legend()
    ax1.set_title("Error")
    ax1.set_xlabel("Error (bpm)")
    ax1.set_ylabel("Cumulative probability")
    ax1.set_ylim(0,1)
    #ax1.set_xlim(-100,100)

    ax2.legend()
    ax2.set_title("Absolute Error")
    ax2.set_xlabel("Absolute Error (bpm)")
    ax2.set_ylabel("Cumulative probability")
    ax2.set_ylim(0,1)
    #ax2.set_xlim(0,200)

if __name__ == "__main__":
    test_time('sd')
    test_time('naive')
    plot_validity()
    plt.show()

