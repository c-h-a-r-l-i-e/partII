package com.charliemaclean.heaphonerecorder

import android.bluetooth.BluetoothAdapter
import android.bluetooth.le.*
import android.os.ParcelUuid
import android.util.Log
import java.util.*

val UUID_HEART_RATE_SERVICE = ParcelUuid(UUID.fromString(GattAttributes.HEART_RATE_SERVICE))


class HeartDeviceScan(
    bluetoothAdapter: BluetoothAdapter
){
    private val mScanner: BluetoothLeScanner = bluetoothAdapter.bluetoothLeScanner

    fun startScan(listener: HeartDeviceScanListener) {
        val scanCallback = object: ScanCallback() {
            override fun onScanResult(callbackType: Int, result: ScanResult?) {
                Log.d("HeartDeviceScan", "onScanResult: $callbackType")
                if (result != null) {
                    listener.onDeviceFound(result.device)
                }
            }
        }

        val filters = listOf<ScanFilter>(
            ScanFilter.Builder()
                .build())


        val settings = ScanSettings.Builder()
            .setMatchMode(ScanSettings.CALLBACK_TYPE_FIRST_MATCH).build()
        mScanner.startScan(scanCallback)

        //mScanner.startScan(filters, settings, scanCallback)
    }
}