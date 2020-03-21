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



def test_validity(step, nlms=True, filterx=True, filtery=False, filterz=True):
    segmentsize = 30
    ppgs, ecgs, accxs, accys, acczs = testsyncs.getSegmentsAtNoise(testsyncs.NOISE_MEDIUM, segmentsize)

    average_error = 0
    for i in range(len(ppgs)):
        # Remove unrelated noise
        ppg = filtering.butter_bandpass_filter(ppgs[i], 0.4, 4, order=2)
        accx = filtering.butter_bandpass_filter(accxs[i], 0.4, 4, order=2)
        accy = filtering.butter_bandpass_filter(accys[i], 0.4, 4, order=2)
        accz = filtering.butter_bandpass_filter(acczs[i], 0.4, 4, order=2)

        # Apply motion filter to each axis dependant on filter parameters
        filtered = ppg
        if filterx:
            filtered = motionfilter.adaptiveFilter(filtered, accx, step, nlms)
        if filtery:
            filtered = motionfilter.adaptiveFilter(filtered, accy, step, nlms)
        if filterz:
            filtered = motionfilter.adaptiveFilter(filtered, accz, step, nlms)
        
        # Calculate heart-rate from filtered signal, and compare to ECG heart-rate
        filteredpeaks = peakfind.find_peaks_min_sd(filtered)
        filteredrate = filteredpeaks.size / segmentsize * 60

        ecgvals = ecgs[i].getValues()
        filtered_ecg = hp.remove_baseline_wander(ecgvals, ecgs[i].getFrequency())
        wd, m = hp.process(hp.scale_data(filtered_ecg), ecgs[i].getFrequency())
        ecgrate = m["bpm"]

        average_error += np.abs(ecgrate - filteredrate)

        #print("filtered PPG : {}, ecg : {}".format(filteredrate, ecgrate))

    print("step = {} --> error = {}".format(step, average_error))

        


def test_time_butter(order):
    setup = """import testsyncs
syncs = testsyncs.getSyncs()
import os
s = syncs[0]
ecg, ppg = s.getSyncedSignals()
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import filtering
order = {}""".format(order)

    test = """filtering.chebyshev2_filter(ppg, 0.4, 4, order=order)"""
    time = timeit.timeit(setup=setup, stmt=test, number=10000)
    print("time at order {}, is {}".format(order, time))

def test_validity_butter(order):
    freq = 100
    size = 120
    heart_rate = 120
    lowcut = 0.4
    highcut = 4
    iters = 1000

    total_product = 0
    
    for i in range(iters):
        hb, hb_noisy = sim_heartbeat_noisy(freq, size, heart_rate)

        xs = np.arange(0, hb.size / freq, 1/freq)

        hb_noisy_signal = data.getSignal(hb_noisy, freq)

        filtered = filtering.butter_bandpass_filter(hb_noisy_signal, lowcut, highcut, order=order)

        total_product += np.max(np.correlate(filtered.getValues() / np.linalg.norm(filtered.getValues()), 
            hb / np.linalg.norm(hb), mode='same'))

    average_product = total_product / iters
    print("average product : {}".format(average_product))

if __name__ == "__main__":
    for i in (0.1,0.2,0.5,1,2,5):
        test_validity(i)

