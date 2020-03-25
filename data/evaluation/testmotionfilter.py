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


def write_validity_table(filename, nlms=True):
    segmentsize = 10
    ppgs, ecgs, accxs, accys, acczs = testsyncs.getSegmentsAtNoise(testsyncs.NOISE_MEDIUM, segmentsize)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        def booltxt(d):
            if d:
                return 'Y'
            else:
                return 'N'

        orders = {}
        for x in [True, False]:
            for y in [True, False]:
                for z in [True, False]:
                    orders["{}{}{}".format(booltxt(x), booltxt(y), booltxt(z))] = 0

        k = 0 

        for taps in [1,2,3,4,5,6,7,8]:
            for step in [0.01,0.1,0.5,1,2]:
                abs_errors = {}
                for x in [True, False]:
                    for y in [True, False]:
                        for z in [True, False]:
                            average_error = 0
                            for i in range(len(ppgs)):
                                # Remove unrelated noise
                                ppg = filtering.butter_bandpass_filter(ppgs[i], 0.4, 4, order=2)
                                accx = filtering.butter_bandpass_filter(accxs[i], 0.4, 4, order=2)
                                accy = filtering.butter_bandpass_filter(accys[i], 0.4, 4, order=2)
                                accz = filtering.butter_bandpass_filter(acczs[i], 0.4, 4, order=2)

                                # Apply motion filter to each axis dependant on filter parameters
                                filtered = ppg
                                if x:
                                    filtered = motionfilter.adaptiveFilter(filtered, accx, step, nlms, M=taps)
                                if y:
                                    filtered = motionfilter.adaptiveFilter(filtered, accy, step, nlms, M=taps)
                                if z:
                                    filtered = motionfilter.adaptiveFilter(filtered, accz, step, nlms, M=taps)
                                
                                # Calculate heart-rate from filtered signal, and compare to ECG heart-rate
                                filteredpeaks = peakfind.find_peaks_min_sd(filtered)
                                filteredrate = filteredpeaks.size / segmentsize * 60

                                ecgvals = ecgs[i].getValues()
                                filtered_ecg = hp.remove_baseline_wander(ecgvals, ecgs[i].getFrequency())
                                wd, m = hp.process(hp.scale_data(filtered_ecg), ecgs[i].getFrequency())
                                ecgrate = m["bpm"]

                                average_error += np.abs(ecgrate - filteredrate) / len(ppgs)


                            abs_errors["{}{}{}".format(booltxt(x), booltxt(y), booltxt(z))] = average_error

                            writer.writerow([taps, step, booltxt(x), booltxt(y), booltxt(z), round(average_error, 3)])

                            print("step={},nlms={},x={},y={},z={},taps={} --> average error = {}".format(step, 
                                nlms, x, y, z, taps, average_error))

                
                print("This iterations errors {}".format(abs_errors))
                abs_errors.pop("NNN")

                j = 1
                for error in sorted(abs_errors.items(), key=lambda x: x[1]):
                    orders[error[0]] += j
                    j+=1

                print("Total orders {}".format(orders))
                print("k : {}".format(k))
                k += 1

        print("Total orders {}".format(orders))
        print("k : {}".format(k))


                        



def test_validity(ax1, ax2, step, nlms=True, filterx=True, filtery=False, filterz=False, taps=20, noise=testsyncs.NOISE_MEDIUM):
    segmentsize = 10
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
    ax1.plot(xs, ys, label="{} taps".format(taps))

    xs = np.sort(np.abs(errors))
    
    ax2.plot(xs, ys, label="{} taps".format(taps))


        


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





def plot_adaptive_validity(nlms, noise):
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    for taps in [1,5,10,15,20]:
        for step in [1]: 
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
    #write_validity_table("lms_validity.csv", nlms=False)
    plt.figure("nlms, medium")
    plot_adaptive_validity(True, testsyncs.NOISE_MEDIUM)

    plt.figure("nlms, high")
    plot_adaptive_validity(True, testsyncs.NOISE_HIGH)

    plt.figure("lms, medium")
    plot_adaptive_validity(False, testsyncs.NOISE_MEDIUM)

    plt.figure("lms, high")
    plot_adaptive_validity(False, testsyncs.NOISE_HIGH)

    plt.show()


#    for i in (0.1,0.2,0.5,1,2,5):
#        test_validity(i)

