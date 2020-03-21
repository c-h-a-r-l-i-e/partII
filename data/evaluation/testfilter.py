import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import timeit
import testsyncs

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import filtering
import data


def sim_unit_heartbeat(a1, b1, c1, a2, b2, c2, freq=200, length=0.5):
    """
    Produce a PPG heartbeat with systolic peak modelled by a Gaussian with parameters
    a1, b1, c1 and a diastolic peak modelled by a Gaussian with parameters a2, b2
    and c2. The heartbeat will be given at frequency freq, and will be 0.5s long.

    Parameters
    --------------
    a1, b1, c1 : Float
        Constants to describe the shape of the systolic peak Gaussian.

    a2, b2, c2 : Float
        Constants to describe the shape of the diastolic peak Gaussian.

    freq : Float
        Frequency to sample the hearbeat at.

    length : Float
        The time the heartbeat should take.

    Returns
    -------------
    hb : numpy array
        The heartbeat
    """
    xs = np.arange(0., length, 1/freq)
    systolic = a1 * np.exp(- (((xs - b1) ** 2) / (2 * (c1 ** 2))))

    diastolic = a2 * np.exp(- (((xs - b2) ** 2) / (2 * (c2 ** 2))))

    hb = systolic + diastolic

    #plt.plot(xs, systolic, label="systolic")
    #plt.plot(xs, diastolic, label="diastolic")
    #plt.plot(xs, hb, label="heartbeat")
    #plt.legend()
    #plt.show()

    return hb

def sim_heartbeat(freq, length, heart_rate, systolic_variation, diastolic_variation):
    """
    Simulate a heartbeat over several beats, adding a random variation to the systolic 
    and diastolic amplitude.

    Parameters
    --------------
    freq : Float
        Frequency to sample the heartbeat at.

    length : Integer
        The length of the heartbeat, given as a number of beats.

    heart_rate : Float
        The heart-rate to simulate

    systolic_variation, diastolic_variation : Float
        Multiplicative random noise to add to the peaks


    Returns
    -------------
    hb : numpy array
        The heartbeat
    """

    beat_length = 60 / heart_rate
    hb = np.array([])
    for i in range(length):
        a1 = 1 * np.random.normal(1, systolic_variation)
        a2 = 0.5 * np.random.normal(1, diastolic_variation)
        unit = sim_unit_heartbeat(a1, 0.18, 0.045, a2, 0.31, 0.06, freq=freq, length=beat_length)

        hb = np.concatenate((hb, unit))

    #xs = np.arange(0, length * beat_length, 1/freq)
    #plt.plot(xs, hb)
    #plt.show()
    #plt.plot()

    return hb


def sim_heartbeat_noise(freq, size, noise_freq, noise_amp):
    """
    Simulate noise to be added to a PPG simulation.

    Parameters
    -------------
    freq : Float
        Frequency of the signal we want to add noise to.

    size : Integer
        Number of samples in the signal we want to add noise to.

    noise_freq : Flaot
        Frequency of the noise we want to add.

    noise_amp : Float
        Amplitude of the noise we add.

    Returns
    --------------
    n : numpy array
        The noise.
    """

    xs = np.arange(0, size/freq, 1/freq)
    n = noise_amp * np.sin(noise_freq * 2 * np.pi * xs)

    #plt.plot(xs, n)
    #plt.show()
    
    return n[:size]

def sim_heartbeat_noisy(freq, size, heart_rate):
    """
    Simulate a heartbeat over several beats, adding a random variation to the systolic 
    and diastolic amplitude.

    Parameters
    --------------
    freq : Float
        Frequency to sample the heartbeat at.

    length : Integer
        The length of the heartbeat, given as a number of beats.

    heart_rate : Integer
        The heart-rate in beats per minute.

    Returns
    --------------
    hb : numpy array
        The heartbeat signal

    hb_noisy : numpy array
        The noisy heartbeat signal
    """
    
    hb = sim_heartbeat(freq, size, heart_rate, 0.1, 0.1)

    # Low frequency
    hb_noisy = hb + sim_heartbeat_noise(freq, hb.size, 0.3, 0.5)
    hb_noisy = hb + sim_heartbeat_noise(freq, hb.size, 0.2, 0.3)

    # High frequency
    # hb_noisy += sim_heartbeat_noise(freq, hb.size, 4 + 0.05, 0.5)
    hb_noisy += np.random.normal(0, 3, hb.size)

    #xs = np.arange(0, hb.size / freq, 1/freq)
    #plt.plot(xs, hb_noisy)
    #plt.show()
    
    return (hb, hb_noisy)

def test_time_butter(order):
    setup = """import testsyncs
syncs = testsyncs.getSyncs()
import os
s = syncs[0]
ecg, ppg = s.getSyncedSignals()
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import filtering
order = {}""".format(order)

    test = """filtering.butter_bandpass_filter(ppg, 0.4, 4, order=order)"""
    time = timeit.timeit(setup=setup, stmt=test, number=1000)
    print("time at order {}, is {}".format(order, time))

def test_time_cheby(order):
    setup = """import testsyncs
syncs = testsyncs.getSyncs()
import os
s = syncs[0]
ecg, ppg = s.getSyncedSignals()
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import filtering
order = {}""".format(order)

    test = """filtering.chebyshev2_filter(ppg, 0.4, 4, order=order)"""
    time = timeit.timeit(setup=setup, stmt=test, number=1000)
    print("time at order {}, is {}".format(order, time))


def plot_power_spectrum(samples, freq):
    ps = np.abs(np.fft.rfft(samples)) ** 2

    xs = np.linspace(0, freq/2, ps.size)
    plt.xlabel("Frequency (hz)")
    plt.ylabel("Power")

    plt.plot(xs, ps)


def plot_validity_filter(butterworth):
    """
    Plot the power spectrum of the simulated hearbeat before and after at various different orders.
    """
    freq = 100
    size = 120
    heart_rate = 120
    lowcut = 0.4
    highcut = 4
    iters = 1

    hb, hb_noisy = sim_heartbeat_noisy(freq, size, heart_rate)

    plt.subplot(4,2,1)
    plt.title("Clean Power Spectrum")
    plot_power_spectrum(hb, freq)
    plt.xlim(0,10)
    plt.ylim(0,2400000)

    plt.subplot(4,2,2)
    plt.title("Noisy Power Spectrum")
    plot_power_spectrum(hb_noisy, freq)
    plt.xlim(0,10)
    plt.ylim(0,2400000)

    hb_noisy_signal = data.getSignal(hb_noisy, freq)
    for order in range(1, 7, 1):
        plt.subplot(4,2,2+order)
        plt.title("Order {} Spectrum".format(order))
        if butterworth:
            filtered = filtering.butter_bandpass_filter(hb_noisy_signal, lowcut, highcut, order=order)
        else:
            filtered = filtering.chebyshev2_filter(hb_noisy_signal, lowcut, highcut, order=order)
        plot_power_spectrum(filtered.getValues(), freq)
        plt.xlim(0,10)
        plt.ylim(0,2400000)





def test_validity_butter(order):
    freq = 100
    size = 480
    heart_rate = 180
    lowcut = 0.4
    highcut = 4
    iters = 1

    total_product = 0
    
    for i in range(iters):
        hb, hb_noisy = sim_heartbeat_noisy(freq, size, heart_rate)

        xs = np.arange(0, hb.size / freq, 1/freq)

        hb_noisy_signal = data.getSignal(hb_noisy, freq)

        filtered = filtering.butter_bandpass_filter(hb_noisy_signal, lowcut, highcut, order=order)

        filtered.plot("filtered")
        plt.legend()
        plt.show()

        total_product += np.max(np.correlate(filtered.getValues() / np.linalg.norm(filtered.getValues()), 
            hb / np.linalg.norm(hb), mode='same'))

    average_product = total_product / iters
    print("average product : {}".format(average_product))

if __name__ == "__main__":
    plot_validity_filter(False)
    plt.show()
    plot_validity_filter(True)
    plt.show()
    for i in range(1, 7, 1):
        print("order {}".format(i))
