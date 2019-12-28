"""
Helper functions to aid plotting of various graphs with heart data
Charlie Maclean 2019
"""
import numpy as np
import matplotlib.pyplot as plt

def plot_signal(signal, freq, colour, label):
    xs = np.arange(0, signal.size/freq, 1/freq)
    xs = xs[0:signal.size] # Splice to correct size
    plt.plot(xs, signal, color = colour, label=label)

