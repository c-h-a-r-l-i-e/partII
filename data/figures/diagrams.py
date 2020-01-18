"""
A collection of functions designed to draw variation graphs and diagrams
for use in the dissertation.
"""


from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import math

def plotChebyFreqResponse(fs, lowcut, highcut, label, order=2, version=1, rp=10):
    # Plot the chebyshev frequency response graph
    nyquist = fs / 2
    
    if version == 1:
        b, a = signal.cheby1(order, rp, (lowcut/nyquist, highcut/nyquist), 
            btype='band')
    else:
        b, a = signal.cheby2(order, rp, (lowcut/nyquist, highcut/nyquist), 
            btype='band')
    w,h=signal.freqz(b,a,worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label=label)

def compareChebyOrder(version=1):
    fs = 20
    lowcut = 0.4
    highcut = 4
    for order in [2,4,6]:
        label = "order = {}".format(order)
        plotChebyFreqResponse(fs, lowcut, highcut, label, version=version, order=order)

    plt.vlines([lowcut,highcut], 0, 1.2, label="Critical frequencies")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()

def compareChebyRp(version=1):
    fs = 20
    lowcut = 0.4
    highcut = 4
    for rp in [1,2,3,4]:
        label = "rp = {}".format(rp)
        plotChebyFreqResponse(fs, lowcut, highcut, label, version=version, rp=rp)

    plt.vlines([lowcut,highcut], 0, 1.2, label="Critical frequencies")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


def plotButterFreqResponse(fs, lowcut, highcut, order=2):
    nyquist = fs / 2

    b, a = signal.butter(order, (lowcut/nyquist, highcut/nyquist), 
            btype='band')
    w, h = signal.freqz(b, a, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = {}".format(order))


def compareButterOrders():
    fs = 20
    lowcut = 0.4
    highcut = 4
    for order in [2,4,6,8]:
        plotButterFreqResponse(fs, lowcut, highcut, order)
    plt.vlines([lowcut,highcut], 0, 1.2, label="Critical frequencies")

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


compareChebyOrder()
compareChebyOrder(version=2)

compareChebyRp()
compareChebyRp(version=2)
compareButterOrders()

