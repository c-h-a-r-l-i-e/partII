package com.charliemaclean.ppgrecorder

import android.bluetooth.BluetoothDevice

abstract class HeartDeviceScanListener {
    abstract fun onDeviceFound(device: BluetoothDevice)
}