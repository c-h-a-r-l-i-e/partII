package com.charliemaclean.heaphonerecorder

import android.bluetooth.BluetoothDevice

abstract class HeartDeviceScanListener {
    abstract fun onDeviceFound(device: BluetoothDevice)
}