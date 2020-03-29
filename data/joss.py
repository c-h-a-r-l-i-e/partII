import scipy
import numpy as np
import matplotlib.pyplot as plt
import sys
import heartrate
from sync import Sync

DEBUG = True

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

    hr = []

    loc = -1
    bpm = -1
    trap_count = 0

    # Iterate through windows
    start = 0
    while start + (8 * freq) < ppg.size:
        window = np.arange(start * freq, (start+window_size) * freq, 1)

        spectrum = joss_ssr(ppg[window], accel_x[window], accel_y[window], accel_z[window])

        if DEBUG:
            print("At start={}, loc={} bpm={} trap_count={} spectrum_shape={}".format(start/freq, 
                loc, bpm, trap_count, spectrum.shape))

        loc, bpm, trap_count = joss_spt(spectrum, freq, loc, bpm, trap_count)


        hr.append(bpm)

        start += shift * freq





def joss_ssr(ppg, accel_x, accel_y, accel_z):
    """
    Run sparse spectrum reconstruction on the MMV model.

    Inputs
    -----------------
     - ppg : ppg as numpy array
     - accel_x : x acceleration as numpy array
     - accel_y : y acceleration as numpy array
     - accel_z : z acceleration as numpy array

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

    spectra = np.zeros((N,L))
    
    for i in range(0, L):
        spectra_i = ssr(Y[:,i], freq, N)

        spectra_i = spectra_i / np.max(spectra_i)
        spectra[:,i] = spectra_i


    # BPM axis
    bpm = 60 * freq / N * np.arange(N)

    aggression = 0.99
    accel_max = np.zeros((N))
    signal_ssr = spectra[:,0]
    print("signal_ssr shape {}".format(signal_ssr.shape))

    # Modify the SSR signal by subtracting the maximum acceleration in each bin
    for i in range(0, bpm.size):
        # Max of acceleration at this frequency
        accel_max[i] = np.amax([spectra[i,1], spectra[i,2], spectra[i,3]])

        signal_ssr[i] = signal_ssr[i] - aggression * accel_max[i]

    # Set all SSR bins lower than the maximum divided by 5 to 0
    max_bin = np.max(signal_ssr)
    signal_ssr[signal_ssr < max_bin / 5] = 0

    return signal_ssr
    

def ssr(y, freq, N):
    M = np.max(y.shape)

    # Make the Fourier matrix
    Phi = np.zeros((M, N), dtype=complex)
    complex_factor = 1j * 2 * np.pi / N
    for m in range(0, M):
        for n in range(0, N):
            Phi[m,n] = np.exp(complex_factor * m * n)

    sparse_spectrum = focuss(y, Phi)

    # band pass the spectrum between 40 and 220 BPM

    low = 40 / 60 
    high = 220 / 60
    sparse_spectrum[:int(np.floor(low / freq * N))] = 0
    sparse_spectrum[int(np.ceil(high / freq * N)):] = 0

    return sparse_spectrum


def focuss(y, Phi):
    iters = 2
    N = Phi.shape[1]
    x = np.ones((N, 1))

    for i in range(0, iters):
        W_pk = np.diagflat(x)

        # Moore-Penrose inverse of Phi * W_pk
        m = np.linalg.pinv(np.matmul(Phi, W_pk))

        q_k = np.matmul(m, y)
        x = np.matmul(W_pk, q_k)

    s = np.abs(x) ** 2

    return s

    
def joss_spt(spectrum, freq, prev_loc, prev_bpm, trap_count):
    deltas = [15, 25]

    N = spectrum.size

    # If initialising
    if prev_loc == -1 and prev_bpm == -1:
        loc = np.argmax(spectrum)
        bpm = 60 * loc / N * freq

    else:
        for delta in deltas:
            print(prev_loc)
            rng = np.arange(prev_loc - delta, prev_loc + delta)

            # find peaks in range
            mask = np.zeros((N,1))
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

    else:
        trap_count = 0

    return loc, bpm, trap_count


def discover_peak(spectrum, prev_loc):
    rng = np.arange(40, 220)
    N = spectrum.shape[0]

    # find peaks in range
    mask = np.zeros((N,1))
    mask[rng] = 1
    filtered = (spectrum * mask).flatten()
    locs, _ = scipy.signal.find_peaks(filtered)

    # find closest peak to prev_loc
    dist = np.abs(prev_loc - locs)
    index = np.argmin(dist)
    loc = locs[index]

    return loc

def plot_joss_and_ecg(sync):
    hr = joss(sync)
    xs = np.arange(0, hr.size * 2, 2)
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
    



