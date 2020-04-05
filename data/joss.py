import scipy
import numpy as np
import matplotlib.pyplot as plt
import sys
import heartrate
import filtering
from sync import Sync
import heartpy as hp
import matlab.engine

DEBUG = False

def get_ecg_bpm(ecg, start, window_size = 8, shift=2):
    freq = ecg.frequency
    vals = ecg.values
    window = vals[freq*start:(start+window_size)*freq]
    filtered = hp.remove_baseline_wander(window, freq)
    wd, m = hp.process(hp.scale_data(filtered), freq, bpmmax=220)
    return m['bpm']


def joss(sync, freq = 20, window_size = 8, shift = 2):
    """
    Run the JOSS algorithm to calculate heart-rate.

    Inputs
    -------------
     - sync : the running data sync object

    Returns
    ------------
     - hr : the estimated heart-rate, an array, with each heart-rate
            estimation 2 s apart.
    """

    freq = 20

    ppg = sync.getSyncedPPG().resample(freq)
    accel_x = sync.getSyncedAcceleration('x').resample(freq)[:ppg.size]
    accel_y = sync.getSyncedAcceleration('y').resample(freq)[:ppg.size]
    accel_z = sync.getSyncedAcceleration('z').resample(freq)[:ppg.size]
    ecg = sync.getSyncedECG()

    
    ppg = filtering.butter_bandpass_filter(ppg, 0.4, 4, 3)
    accel_x = filtering.butter_bandpass_filter(accel_x, 0.4, 4, 5)
    accel_y = filtering.butter_bandpass_filter(accel_y, 0.4, 4, 5)
    accel_z = filtering.butter_bandpass_filter(accel_z, 0.4, 4, 5)

    hr = []

    eng = matlab.engine.start_matlab()

    loc = 121
    bpm = 121
    trap_count = 0

    # Iterate through windows
    start = 0
    while (start + window_size) * freq < ppg.size:
        window = np.arange(start * freq, (start+window_size) * freq, 1)

        spectrum, accel_max = joss_ssr(ppg[window].normalize(), accel_x[window].normalize(), 
                accel_y[window].normalize(), accel_z[window].normalize(), eng)

        if DEBUG:
            print("At start={}, loc={} bpm={} trap_count={} spectrum_shape={}".format(start, 
                loc, bpm, trap_count, spectrum.shape))
            ecg_bpm = get_ecg_bpm(ecg, start, window_size)
            print("ECG bpm = {}".format(ecg_bpm))
            plt.plot(spectrum)
            plt.gca().axvline(x=ecg_bpm, color='r')
            plt.show()

        loc, bpm, trap_count = joss_spt(spectrum, freq, loc, bpm, trap_count)


        hr.append(bpm)

        start += shift 

    eng.quit()

    return np.array(hr)





def joss_ssr(ppg, accel_x, accel_y, accel_z, eng):
    """
    Run sparse spectrum reconstruction on the MMV model.

    Inputs
    -----------------
     - ppg : ppg as signal
     - accel_x : x acceleration as signal
     - accel_y : y acceleration as signal
     - accel_z : z acceleration as signal

     Returns
     ----------------
      - ssr_spectrum : the cleaned sparse spectrum of the ppg

    """

    freq = ppg.frequency

    N = 60 * freq # Resolution is 1 BPM

    Y = np.array((ppg.values, accel_x.values, accel_y.values, 
            accel_z.values))

    Y = np.transpose(Y)

    L = Y.shape[1]

    spectra = ssr(Y, freq, N, eng)
    
    for i in range(0, L):
        spectra_i = spectra[:,i]

        spectra_i[:20] = 0
        spectra_i[220:] = 0

        spectra_i = spectra_i / np.max(spectra_i)
        spectra[:,i] = spectra_i


    # BPM axis
    bpm = 60 * freq / N * np.arange(N)

    aggression = 0.99
    accel_max = np.zeros((N))
    signal_ssr = spectra[:,0]

    # Modify the SSR signal by subtracting the maximum acceleration in each bin
    for i in range(0, bpm.size):
        # Max of acceleration at this frequency
        accel_max[i] = np.max([spectra[i,1], spectra[i,2], spectra[i,3]])

        signal_ssr[i] = signal_ssr[i] - aggression * accel_max[i]

    # Set all SSR bins lower than the maximum divided by 5 to 0
    max_bin = np.max(signal_ssr)
    signal_ssr[signal_ssr < max_bin / 4] = 0


    return signal_ssr, accel_max
    

def ssr(y, freq, N, eng):
    M = np.max(y.shape)

    # Make the Fourier matrix
    phi = np.zeros((M, N), dtype=complex)
    complex_factor = 1j * 2 * np.pi / N
    for m in range(0, M):
        for n in range(0, N):
            phi[m,n] = np.exp(complex_factor * m * n)

    Phi = matlab.double(phi.tolist(), is_complex=True)
    Y = matlab.double(y.tolist())

    X = eng.MFOCUSS(Phi, Y, 1e-10, 'MAX_ITERS', 4)
    x = np.array(X)
    x = np.abs(x) ** 2

    
    return x

    
def joss_spt(spectrum, freq, prev_loc, prev_bpm, trap_count):
    deltas = [15, 25]

    N = spectrum.size

    # If initialising
    if prev_loc == -1 and prev_bpm == -1:
        loc = np.argmax(spectrum)
        bpm = 60 * loc / N * freq

    else:
        for delta in deltas:
            rng = np.arange(prev_loc - delta, prev_loc + delta)

            # find peaks in range
            mask = np.zeros((N,))
            mask[rng[rng>0]] = 1
            filtered = (spectrum * mask).flatten()
            locs, _ = scipy.signal.find_peaks(filtered)
            vals = filtered[locs]

            num_peaks = locs.size
            if num_peaks > 0:
                max_index = np.argmax(vals)
                loc = locs[max_index]
                bpm = 60 * loc / N * freq
                if DEBUG:
                    print("Found peak at location {}".format(loc))
                break

        else:
            loc = prev_loc
            bpm = prev_bpm

    # validate results
    if loc == prev_loc:
        trap_count += 1
        if trap_count > 2:
            loc = discover_peak(spectrum, prev_loc)
            bpm = 60 * loc / N * freq

            if DEBUG:
                print("Validated results to find peak at {}".format(bpm))

    else:
        trap_count = 0

    return loc, bpm, trap_count


def discover_peak(spectrum, prev_loc):
    rng = np.arange(40, 220)
    N = spectrum.shape[0]

    # find peaks in range
    mask = np.zeros((N,))
    mask[rng] = 1
    filtered = (spectrum * mask).flatten()
    locs, _ = scipy.signal.find_peaks(filtered)

    if locs.size == 0:
        return prev_loc

    # find closest peak to prev_loc
    dist = np.abs(prev_loc - locs)
    index = np.argmin(dist)
    loc = locs[index]

    return loc

def plot_joss_and_ecg(sync):
    hr = joss(sync)
    xs = np.arange(0, hr.size*2, 2)
    plt.plot(xs, hr, label="JOSS on PPG")

    ecg_hr = heartrate.get_ecg_hr(sync.getSyncedECG())
    plt.plot(ecg_hr, label="ECG")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: sync.py ecgFile watchDir")

    ecgfile = sys.argv[1]
    watchdir= sys.argv[2]
    sync = Sync(ecgfile, watchdir)

    plot_joss_and_ecg(sync)
    plt.legend()
    plt.show()
    



