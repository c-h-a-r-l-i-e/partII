import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import sync
import matplotlib.pyplot as plt
import data

NOISE_LOW = 0 # 6kph or below
NOISE_MEDIUM = 1 # 10 kph or below
NOISE_HIGH = 2 # above 10kph


validData = [
        {'ecg': 'ecg-files/DATA/20191218/11-28-26.EDF', 'watch': 'files/recordings/2019-12-18/12.07.36.487/', 'noise':NOISE_HIGH},
        {'ecg': 'ecg-files/DATA/20191219/12-59-49.EDF', 'watch': 'files/recordings/2019-12-19/13.22.33.826/', 'noise':NOISE_HIGH}, 
        {'ecg': 'ecg-files/DATA/20191222/16-04-00.EDF', 'watch': 'files/recordings/2019-12-22/16.49.28.247/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20191223/12-26-37.EDF', 'watch': 'files/recordings/2019-12-23/12.48.14.208/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20191226/13-16-47.EDF', 'watch': 'files/recordings/2019-12-26/13.44.43.071/', 'noise':NOISE_HIGH},
        {'ecg': 'ecg-files/DATA/20191228/08-56-14.EDF', 'watch': 'files/recordings/2019-12-28/09.25.16.549/', 'noise':NOISE_HIGH},
        {'ecg': 'ecg-files/DATA/20191230/13-12-12.EDF', 'watch': 'files/recordings/2019-12-30/13.28.09.688/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20191230/13-29-27.EDF', 'watch': 'files/recordings/2019-12-30/13.47.11.833/', 'noise':NOISE_HIGH},
        {'ecg': 'ecg-files/DATA/20200104/09-08-06.EDF', 'watch': 'files/recordings/2020-01-04/09.36.13.589/', 'noise':NOISE_HIGH},
        {'ecg': 'ecg-files/DATA/20200115/15-14-52.EDF', 'watch': 'files/recordings/2020-01-15/15.31.07.931/', 'noise':NOISE_HIGH}, 
        #boundary ^
        {'ecg': 'ecg-files/DATA/20200118/13-55-42.EDF', 'watch': 'files/recordings/2020-01-18/14.07.45.306/', 'noise':NOISE_LOW},
        {'ecg': 'ecg-files/DATA/20200118/14-11-26.EDF', 'watch': 'files/recordings/2020-01-18/14.23.58.924/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20200228/18-13-02.EDF', 'watch': 'files/recordings/2020-02-28/18.20.12.094/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20200228/18-25-25.EDF', 'watch': 'files/recordings/2020-02-28/18.33.06.101/', 'noise':NOISE_MEDIUM},
        {'ecg': 'ecg-files/DATA/20200228/18-36-47.EDF', 'watch': 'files/recordings/2020-02-28/18.44.02.330/', 'noise':NOISE_HIGH}
        ]


def getSyncs():
    """
    Get a list of all the Sync objects which can be used for testing.

    Returns
    ----------
    syncs : list of Sync
        The list of Sync objects.
    """

    parent = sys.path[0] + "/../"
    syncs = []
    for data in validData:
        
        s = sync.getSync(parent+data['ecg'], parent+data['watch'])
        syncs.append(s)

    return syncs


def getSyncsAtNoise(noise):
    if noise not in (NOISE_LOW, NOISE_MEDIUM, NOISE_HIGH):
        raise ValueError("Noise must be one of NOISE_LOW, NOISE_MEDIUM or NOISE_HIGH")

    parent = sys.path[0] + "/../"
    syncs = []
    for data in validData:
        if data['noise'] == noise:
            s = sync.getSync(parent+data['ecg'], parent+data['watch'])
            syncs.append(s)

    return syncs

def getSegmentsAtNoise(noise, seglength=30):
    """
    Get data split into segments

    Params
    ----------
     - noise : 
        Noise category of data

     - seglength : float
        Length of segments in seconds

    Returns
    --------
     - ppgsegments : list of data.Signal 
     - ecgsegments : list of data.Signal 
     - accelxsegments : list of data.Signal 
     - accelysegments : list of data.Signal
     - accelzsegments : list of data.Signal
        
    """
    ppgsegments = []
    ecgsegments = []
    accelxsegments = []
    accelysegments = []
    accelzsegments = []

    syncs = getSyncsAtNoise(noise)
    for sync in syncs:
        ecg, ppg = sync.getSyncedSignals()
        ppgfreq = ppg.getFrequency()
        ecgfreq = ecg.getFrequency()
        
        accelx = sync.getSyncedAcceleration('x')
        accely = sync.getSyncedAcceleration('y')
        accelz = sync.getSyncedAcceleration('z')
        accelfreq = accelx.getFrequency()

        ppgsize = int(seglength * ppgfreq)
        ecgsize = int(seglength * ecgfreq)
        accelsize = int(seglength * accelfreq)

        while(ppg.size >= ppgsize and ecg.size >= ecgsize and accelx.size >= accelsize):
            ppgsegments.append(ppg[:ppgsize])
            ppg = ppg[ppgsize:]

            ecgsegments.append(ecg[:ecgsize])
            ecg = ecg[ecgsize:]

            accelxsegments.append(accelx[:accelsize])
            accelx = accelx[accelsize:]

            accelysegments.append(accely[:accelsize])
            accely = accely[accelsize:]

            accelzsegments.append(accelz[:accelsize])
            accelz = accelz[accelsize:]

            #plt.figure()
            #ppgsegments[-1].plot()

            #plt.figure()
            #ecgsegments[-1].plot()

            #plt.figure()
            #accelxsegments[-1].plot()
            #plt.show()

    return ppgsegments, ecgsegments, accelxsegments, accelysegments, accelzsegments


def printTotalDataAvailable():
    lowtime = 0

    for sync in getSyncsAtNoise(NOISE_LOW):
        lowtime += sync.getPPGLength()
    print("Low noise time : {}".format(lowtime))

    mediumtime = 0
    for sync in getSyncsAtNoise(NOISE_MEDIUM):
        mediumtime += sync.getPPGLength()
    print("Medium noise time : {}".format(mediumtime))
        
    hightime = 0
    for sync in getSyncsAtNoise(NOISE_HIGH):
        hightime += sync.getPPGLength()
    print("Low noise time : {}".format(hightime))

if __name__ == "__main__":

    printTotalDataAvailable()

    getSegmentsAtNoise(NOISE_LOW)

    for s in getSyncs():
        sync.plotSyncedAccelerometer(s)
        plt.show()

