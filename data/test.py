import numpy as np

ear_times = np.arange(0, 10, 1)
ppg_times = np.arange(1, 10, 0.25)

ppg_start = ppg_times[0]
ear_start = ear_times[0]


if ear_start < ppg_start:
    # Find first ear_time which is over the start time of the ppg, then find the closest ppg
    # time to that. Crop all signals.
    crop_ear = None
    crop_ppg = None
    for i, t in enumerate(ear_times):
        if t > ppg_start:
            crop_ear = i

            # Find the amount to crop the PPG by looking at where the start times are closest
            print(np.abs(ppg_times[:6] - t))
            crop_ppg = np.argmin(np.abs(ppg_times[:int(6)] - t))
            break

    if crop_ppg is None:
        raise ValueError("Couldn't sync, ensure recordings happened at the same time.")

    print("crop PPG by {}".format(crop_ppg))
    print("crop ear by {}".format(crop_ear))

else:
    # Find smaple number in ppg which is closest to ear_start, and crop both ppg and ecg
    crop = None

    for i, t in enumerate(ppg_times):
        if t > ear_start:
            crop = i
            print(crop)
            break

    if crop is None:
        raise ValueError("Couldn't sync, ensure recordings happened at the same time.")

    ppg_crop = crop
    print("crop PPG by {}".format(crop))

