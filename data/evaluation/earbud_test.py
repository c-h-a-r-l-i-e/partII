import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import timeit
import testsyncs
import heartpy as hp

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import filtering
import kalmanfilter
import data
import motionfilter
import peakfind
import csv
import earbuds
import heartrate


valid_data = [
        {'ecg': 'ecg-files/DATA/20200413/12-13-29.EDF', 'watch': 'files/recordings/2020-04-13/12.36.35.034/'},
        {'ecg': 'ecg-files/DATA/20200415/10-33-10.EDF', 'watch': 'files/recordings/2020-04-15/10.48.22.416/'},
        {'ecg': 'ecg-files/DATA/20200415/10-47-33.EDF', 'watch': 'files/recordings/2020-04-15/10.53.47.058/'}]

def get_earbud_syncs():
    syncs = []
    parent = sys.path[0] + "/../"
    for data in valid_data:
        sync = earbuds.Sync(parent+data['ecg'], parent+data['watch'])
        syncs.append(sync)

    return syncs

def test_ear(ax1, ax2):
    syncs = get_earbud_syncs()

    average_error = 0
    errors = np.zeros(0)

    for sync in syncs:
        ecg = sync.ecg
        ecg_hr = heartrate.get_ecg_hr(ecg, ave_size=30)[20:]
        ear_hr = sync.ear.values[20:]

        if ear_hr.size > ecg_hr.size:
            ear_hr = ear_hr[:ecg_hr.size]
        else:
            ecg_hr = ecg_hr[:ear_hr.size]

        errors = np.append(errors, ear_hr - ecg_hr)

    # plot cdf
    xs = np.sort(errors)
    ys = np.arange(1, len(errors) + 1, 1) / len(errors)
    label = "Earbuds"

    ax1.plot(xs, ys, label=label)

    xs = np.sort(np.abs(errors))
    ax2.plot(xs, ys, label=label)

def test_wrist(ax1, ax2):
    syncs = get_earbud_syncs()

    average_error = 0
    errors = np.zeros(0)

    for sync in syncs:
        ecg = sync.ecg
        ecg_hr = heartrate.get_ecg_hr(ecg, ave_size=15)[20:]
        watch_hr = sync.hr.values[20:]

        if watch_hr.size > ecg_hr.size:
            watch_hr = watch_hr[:ecg_hr.size]
        else:
            ecg_hr = ecg_hr[:watch_hr.size]

        errors = np.append(errors, watch_hr - ecg_hr)

    # plot cdf
    xs = np.sort(errors)
    ys = np.arange(1, len(errors) + 1, 1) / len(errors)
    label = "Watch"

    ax1.plot(xs, ys, label=label)

    xs = np.sort(np.abs(errors))
    ax2.plot(xs, ys, label=label)

def test_kalman(ax1, ax2):
    syncs = get_earbud_syncs()

    average_error = 0
    errors = np.zeros(0)

    for sync in syncs:
        ecg = sync.ecg
        ecg_hr = heartrate.get_ecg_hr(ecg, ave_size=30)[20:]

        f = kalmanfilter.Filter(sync.ear, sync.hr)
        filtered_hr = f.filter().values[20:]

        if filtered_hr.size > ecg_hr.size:
            filtered_hr = filtered_hr[:ecg_hr.size]
        else:
            ecg_hr = ecg_hr[:filtered_hr.size]

        errors = np.append(errors, filtered_hr - ecg_hr)

    # plot cdf
    xs = np.sort(errors)
    ys = np.arange(1, len(errors) + 1, 1) / len(errors)
    label = "Sensor Fusion"

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


def plot_errors():
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)

    # Test both with optimal parameters
    test_kalman(ax1, ax2)
    test_ear(ax1, ax2)
    test_wrist(ax1, ax2)

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


def plot_all():
    for sync in get_earbud_syncs():
        f = kalmanfilter.Filter(sync.ear, sync.hr)
        filtered = f.filter()
        filtered.plot("Kalman Filtered")

        earbuds.plot_ecg(sync.ecg)
        sync.ear.plot("Earbud")
        sync.hr.plot("Watch HR")

        plt.legend()
        plt.show()

if __name__ == "__main__":
    # plot_all()
    plot_errors()
    plt.show()

