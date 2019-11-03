#!/usr/bin/python3

import matplotlib.pyplot as plt
import csv
import sys

x = []
y = []

if len(sys.argv) == 2:
    print("Usage: graph.py filename")
    filename = sys.argv[1]

with open("{}".format(filename), 'r') as csvfile:
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
plt.show()


