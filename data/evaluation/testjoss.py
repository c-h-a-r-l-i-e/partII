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
import joss


def test_nlms_validity(ax1, ax2, step=1, nlms=True, 
        filterx=True, filtery=False, filterz=False, taps=15, noise=testsyncs.NOISE_MEDIUM):
    segmentsize = 20
    ppgs, ecgs, accxs, accys, acczs = testsyncs.getSegmentsAtNoise(noise, segmentsize)

    average_error = 0
    errors = np.zeros(len(ppgs))
    for i in range(len(ppgs)):
        # Remove unrelated noise
        ppg = filtering.butter_bandpass_filter(ppgs[i], 0.4, 4, order=2)
        accx = filtering.butter_bandpass_filter(accxs[i], 0.4, 4, order=2)
        accy = filtering.butter_bandpass_filter(accys[i], 0.4, 4, order=2)
        accz = filtering.butter_bandpass_filter(acczs[i], 0.4, 4, order=2)

        # Apply motion filter to each axis dependant on filter parameters
        filtered = ppg
        if filterx:
            filtered = motionfilter.adaptiveFilter(filtered, accx, step, nlms, M=taps)
        if filtery:
            filtered = motionfilter.adaptiveFilter(filtered, accy, step, nlms, M=taps)
        if filterz:
            filtered = motionfilter.adaptiveFilter(filtered, accz, step, nlms, M=taps)
        
        # Calculate heart-rate from filtered signal, and compare to ECG heart-rate
        filteredpeaks = peakfind.find_peaks_min_sd(filtered)
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

    print("step={},nlms={},x={},y={},z={},taps={} --> average error = {}".format(step, 
        nlms, filterx, filtery, filterz, taps, average_error))

    #plt.figure(num="step={},nlms={},taps={}".format(step, nlms, taps))

    label = "{} Taps".format(taps)
    label = "Step {}".format(step)
    label = "NLMS" if nlms else "LMS"

    ax1.plot(xs, ys, label=label)

    xs = np.sort(np.abs(errors))
    
    ax2.plot(xs, ys, label=label)

def test_joss_validity(ax1, ax2, noise):
    syncs = testsyncs.getSyncsAtNoise(noise)
    errors = []

    for sync in syncs:
        error = joss.joss(sync, errors=True)
        errors.extend(error)

    errors = np.array(errors)

    # plot cdf
    xs = np.sort(errors)
    ys = np.arange(1, len(errors) + 1, 1) / len(errors)

    label = "JOSS"

    ax1.plot(xs, ys, label=label)

    xs = np.sort(np.abs(errors))
    
    ax2.plot(xs, ys, label=label)


def test_time_motion_filter(nlms):
    setup = """import testsyncs
ppgs, ecgs, accxs, accys, acczs = testsyncs.getSegmentsAtNoise(testsyncs.NOISE_MEDIUM, 30)
ppg, acc = ppgs[0], accxs[0]

import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import filtering
import motionfilter
taps = 15
step = 1
nlms = {}""".format(nlms)

    test = """motionfilter.adaptiveFilter(ppg, acc, step, nlms, M=taps)"""
    time = timeit.timeit(setup=setup, stmt=test, number=1000)
    print("time with nlms {}, is {}".format(nlms, time))


def plot_joss_nlms(nlms, noise):
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    taps = 15

    # Test both with optimal parameters
    test_joss_validity(ax1, ax2, noise=noise)
    test_nlms_validity(ax1, ax2, noise=noise)

    if False:
        for taps in [15]:
            for step in [0.1, 0.5, 1, 1.5, 2]: 
                print("########   taps = {}, steps = {}  ############".format(taps, step))
                for x in [True]:
                    for y in [False]:
                        for z in [False]:
                            test_validity(ax1, ax2, step, nlms, x, y, z, taps=taps, noise=noise)

    ax1.legend()
    ax1.set_title("Error")
    ax1.set_xlabel("Error (bpm)")
    ax1.set_ylabel("Cumulative probability")
    ax1.set_ylim(0,1)
    ax1.set_xlim(-100,100)

    ax2.legend()
    ax2.set_title("Absolute Error")
    ax2.set_xlabel("Absolute Error (bpm)")
    ax2.set_ylabel("Cumulative probability")
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,200)

if __name__ == "__main__":
    plot_joss_nlms(True, testsyncs.NOISE_MEDIUM)
    plt.show()

