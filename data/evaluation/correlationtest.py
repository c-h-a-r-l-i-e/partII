import testsyncs
import sys
import os
import timeit
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import sync

GAP = 1



def crosscorrelationTest():
    syncs = testsyncs.getSyncs()

    totalError = 0
    
    for s in syncs:
        
        freq = s.getECG_freq()

        f = s._getWatchAccelUp()

        g = s._getECGAccelUp()

        first_samples = 120 * freq
        second_samples = 240 * freq
        
        gap = 1


        #print("Watch First")
        #print("normal: {}".format(sync.correlate(f[:second_samples], g[:first_samples])))
        #print("fast  : {}".format(sync.fastCorrelate(f[:second_samples], g[:first_samples], freq, initTimeGap=gap)))
        watchnk, watchnv = sync.correlate(f[:second_samples], g[:first_samples])
        watchfk, watchfv = sync.fastCorrelate(f[:second_samples], g[:first_samples], freq, initTimeGap=GAP)

        #print("ECG First")
        #print("normal: {}".format(sync.correlate(g[:second_samples], f[:first_samples])))
        #print("fast  : {}".format(sync.fastCorrelate(g[:second_samples], f[:first_samples], freq, initTimeGap=gap)))
        ecgnk, ecgnv = sync.correlate(g[:second_samples], f[:first_samples])
        ecgfk, ecgfv = sync.fastCorrelate(g[:second_samples], f[:first_samples], freq, initTimeGap=GAP)

        # watch was first
        if watchnv > ecgnv:
            timeDiff = (watchnk - watchfk)/freq

        else:
            timeDiff = (ecgnk - ecgfk)/freq

        totalError += np.abs(timeDiff)

    print("Average absolute error {}".format(totalError/len(syncs)))

def correlate(f, g):
    sync.correlate(f, g)

def fastCorrelate(f, g, freq):
    sync.fastCorrelate(f, g, freq, initTimeGap=GAP)

def crosscorrelationTimeTest():
    setup = """import testsyncs
from __main__ import correlate
from __main__ import fastCorrelate
syncs = testsyncs.getSyncs()
s = syncs[0]
freq = s.getECG_freq()
f = s._getWatchAccelUp()
g = s._getECGAccelUp()
first_samples = 120 * freq
second_samples = 240 * freq"""

    test_old = """correlate(f[:second_samples], g[:first_samples])"""
    test_fast = """fastCorrelate(f[:second_samples], g[:first_samples], freq)"""

    #time_old = timeit.timeit(setup=setup, stmt=test_old, number=20)
    time_fast = timeit.timeit(setup=setup, stmt=test_fast, number=500)

    #print("time old : {}".format(time_old))
    print("time fast: {}".format(time_fast))


if __name__ == "__main__":
    crosscorrelationTimeTest()
    crosscorrelationTest()
    

