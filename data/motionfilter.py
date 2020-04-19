import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import sys
import sync
import filtering
import data
from scipy import signal


def nlms_filter(ppg, accel, K=15, step=1):
  """
  Run a normalised least mean squares adaptive filter to remove noise from the signal
  that we know is correlated to the reference signal.

  Parameters
  ------------
   - ppg - the signal we want to remove noise from
   - accel - a signal we think is correlated with the noise
   - K - number of taps to use in the filter
   - step - step size to use

  Returns
  ------------
   - filtered - the signal with noise removed
  """

  N = ppg.size          # Size of PPG signal

  # Preprocessing
  freq = ppg.getFrequency()
  accel = accel.resample(freq)
  accel = accel.crop(N)

  accel = accel.getValues()
  ppg = ppg.getValues()

  w = np.zeros(K)      # Initial filter
  e = np.zeros(N-K)    # Initial error

  for n in range(0, N-K):
    accel_n = accel[n+K:n:-1]
    e_n = ppg[n+K] - np.dot(accel_n, w)          

    norm_factor = 1 / (np.dot(accel_n, accel_n) + 0.001)
    w = w + step * e_n * accel_n * norm_factor

    e[n] = e_n

  return data.getSignal(e, freq)

def lms_filter(ppg, accel, K=15, step=1):
  """
  Run a least mean squares adaptive filter to remove noise from the signal
  that we know is correlation to the reference signal.

  Parameters
  ------------
   - ppg - the signal we want to remove noise from
   - accel - a signal we think is correlated with the noise
   - K - number of taps to use in the filter
   - step - step size to use

  Returns
  ------------
   - filtered - the signal with noise removed
  """

  N = ppg.size          # Size of PPG signal

  # Preprocessing
  freq = ppg.getFrequency()
  accel = accel.resample(freq)
  accel = accel.crop(N)

  accel = accel.getValues()
  ppg = ppg.getValues()

  w = np.zeros(K)      # Initial filter
  e = np.zeros(N-K)    # Initial error

  for n in range(0, N-K):
    accel_n = accel[n+K:n:-1]
    e_n = ppg[n+K] - np.dot(accel_n, w)          
    w = w + step * e_n * accel_n

    e[n] = e_n

  return data.getSignal(e_n, freq)



  plt.figure()
  plt.title("Estimated heart rate against actual heart rate")
  plt.plot(estimatedHeart, label="estimated")
  plt.legend()
  plt.show()


  # t = ppg
  # x = accel
  # noise = heart

  """
  fig = plt.figure()
  plt.title('Unknown filter')
  plt.stem(h)
  """

  """
  plt.figure()
  plt.title('Estimated filter')
  plt.stem(w)

  plt.figure()
  plt.title('Error signal')
  plt.stem(e)
  plt.figure()
  plt.title('Noise signal')
  plt.stem(noise)
  """


"""
Use an adaptive filter to remove noise caused by (and hence correlating
with) referenceMotion, from signal.
"""
def adaptiveFilter(signal, referenceMotion, step=1, nlms=True, M = 20):
    # Sample referenceMotion at signal's frequency
    freq = signal.getFrequency()
    referenceMotion = referenceMotion.resample(freq)
    referenceMotion = referenceMotion.crop(signal.size)



    if nlms:
        filtered = nlms_filter(signal, referenceMotion, step=step, K=M)
    else:
        filtered = lms_filter(signal, referenceMotion, step=step, K=M)

    return filtered



def adaptiveFilterWindowed(signal, referenceMotion, windowSize = 1000):
    # Sample referenceMotion at signal's frequency
    freq = signal.getFrequency()
    referenceMotion = referenceMotion.resample(freq)
    referenceMotion = referenceMotion.crop(signal.size)

    ppgVals = signal.getValues()
    accelVals = referenceMotion.getValues()

    M = 20 # Num of filter taps
    step = 1 # Step size
    output = np.array([])

    while ppgVals.size > 0:
        y, e, w = adf.nlms(accelVals[:windowSize], ppgVals[:windowSize],
                M, step, returnCoeffs=True)
        output = np.concatenate((output, e))
        accelVals = accelVals[windowSize:]
        ppgVals = ppgVals[windowSize:]

    filtered = data.getSignal(output, freq)
    return filtered


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected usage: motionfilter.py ecgFile " +
                "watchDataDirectory")

    ecgFile = sys.argv[1]
    watchDirectory = sys.argv[2]

    synced = sync.getSync(ecgFile, watchDirectory)

    ecg, ppg = synced.getSyncedSignals()

    lowerBPM = 40
    upperBPM = 220
    butterFiltered = filtering.butter_bandpass_filter(
        ppg,lowerBPM/60, upperBPM/60).normalize()

    accelerationX = synced.getSyncedAcceleration('x')
    accelerationY = synced.getSyncedAcceleration('y')
    accelerationZ = synced.getSyncedAcceleration('z')

    accelerationX = filtering.butter_bandpass_filter(
	    accelerationX, lowerBPM/60, upperBPM/60).normalize()
    accelerationY = filtering.butter_bandpass_filter(
	    accelerationY, lowerBPM/60, upperBPM/60).normalize()
    accelerationZ = filtering.butter_bandpass_filter(
            accelerationZ, lowerBPM/60, upperBPM/60).normalize()

    motionFiltered = butterFiltered

    motionFiltered = adaptiveFilter(motionFiltered, accelerationX).normalize()
    motionFiltered = adaptiveFilter(motionFiltered, accelerationY).normalize()
    motionFiltered = adaptiveFilter(motionFiltered, accelerationZ).normalize()

    ecg.plot("ECG")
    motionFiltered.plot("PPG Motion Filtered")
    butterFiltered.plot("PPG Standard Filtering")
    plt.legend()
    plt.show()
