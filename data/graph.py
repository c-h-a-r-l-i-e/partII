#!/usr/bin/python3

from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import ast
import WatchData

def plotPPG(foldername):
    x = []
    y = []
    with open("{}/ppg.csv".format(foldername), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        starting = True
        startTime = 0
        for row in plots:
            if starting:
                starting = False
                startTime = int(row[0])

            # Use time since recording started, in seconds
            x.append((int(row[0])-startTime) / 1000)
            y.append(float(row[1]))



    plt.plot(x,y, label="PPG Readings")
    plt.xlabel("Time (s)")
    plt.ylabel("PPG Reading")
    plt.title("Plot of heartbeat sensors")
    plt.legend()


def plotAcceleration(foldername):
    wd = WatchData.WatchData(foldername)
    accel = wd.getAcceleration()
    t = accel['time']
    x = accel['x']
    y = accel['y']
    z = accel['z']
    plt.plot(t, x, label="x")
    plt.plot(t, y, label="y")
    plt.plot(t, z, label="z")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration")

    plt.title("Plot of accelerometer sensors")
    plt.legend()

"""        
    with open("{}/accelerometer.csv".format(foldername), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        starting = True
        startTime = 0
        for row in plots:
            if starting:
                starting = False
                startTime = int(row[0])

            # Use time since recording started, in seconds
            t.append((int(row[0])-startTime) / 1000)
            accelerationData = ast.literal_eval(row[1])
            x.append(accelerationData[0])
            y.append(accelerationData[1])
            z.append(accelerationData[2])
"""
def plotRotation(foldername):
    t = []
    x = []
    y = []
    z = []
    with open("{}/rotation.csv".format(foldername), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        starting = True
        startTime = 0
        for row in plots:
            if starting:
                starting = False
                startTime = int(row[0])

            # Use time since recording started, in seconds
            t.append((int(row[0])-startTime) / 1000)
            accelerationData = ast.literal_eval(row[1])
            x.append(accelerationData[0])
            y.append(accelerationData[1])
            z.append(accelerationData[2])
    plt.plot(t, x, label="x")
    plt.plot(t, y, label="y")
    plt.plot(t, z, label="z")
    plt.xlabel("Time (s)")
    plt.ylabel("Rotation")
    plt.title("Plot of rotation sensors")
    plt.legend()


# TODO: use pandas csv reader!!!
def plotPowerSpectrum(foldername):
    x = []
    y = []
    with open("{}/ppg.csv".format(foldername), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        starting = True
        startTime = 0
        for row in plots:
            if starting:
                starting = False
                startTime = int(row[0])
                startVal = float(row[1])

            # Use time since recording started, in seconds
            x.append((int(row[0])-startTime) / 1000)
            y.append(float(row[1]) - startVal)

    average = sum(y) / len(y)
    y = [i - average for i in y]
    data = np.array(y)

    fs = len(x) / (x[-1] - x[0])
    f, Pxx_den = signal.welch(y, fs)

    plt.semilogy(f, Pxx_den)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')

def plotPPGAtZero(foldername, label="PPG Readings", color="blue"):
    x = []
    y = []
    with open("{}/ppg.csv".format(foldername), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        starting = True
        startTime = 0
        for row in plots:
            if starting:
                starting = False
                startTime = int(row[0])

            # Use time since recording started, in seconds
            x.append((int(row[0])-startTime) / 1000)
            y.append(float(row[1]))

    average = sum(y) / len(y)
    y = [i - average for i in y]

    plt.plot(x,y, label=label, color=color)
    plt.xlabel("Time (s)")
    plt.ylabel("PPG Reading")
    plt.title("Plot of heartbeat sensors")
    plt.legend()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: graph.py foldername")
    else:

        folder = sys.argv[1]
        plotAcceleration(folder)
        plt.show()

        plt.subplot(2,2,1)
        plotPPG(folder)
        plt.subplot(2,2,2)
        plotAcceleration(folder)
        plt.subplot(2,2,3)
        plotPowerSpectrum(folder)
        plt.subplot(2,2,4)
        plotRotation(folder)

        plt.show()
        plotAcceleration(folder)
        plt.show()

        #plotPPGAtZero("files/recording_2019-11-07T14:30:12.018_trimmed/", label="Resting")

        plotPPGAtZero("files/recording_2019-11-06T11:09:28.241/", label="Running", color="orange")
        #plotPowerSpectrum(folder)


        plt.show()


