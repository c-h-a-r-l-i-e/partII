package com.charliemaclean.heaphonerecorder

import android.app.Service
import android.bluetooth.*
import android.content.Context
import android.content.Intent
import android.os.Binder
import android.os.IBinder
import android.util.Log
import java.io.File
import java.util.*


class HeartDeviceService: Service() {
    companion object {
        val ACTION_GATT_CONNECTED = "com.charliemaclean.bluetooth.le.ACTION_GATT_CONNECTED"
        val ACTION_GATT_DISCONNECTED = "com.charliemaclean.bluetooth.le.ACTION_GATT_DISCONNECTED"
        val ACTION_SAVED = "com.charliemaclean.heartrate.ACTION_SAVED"
    }

    private val TAG: String = HeartDeviceService::class.simpleName.toString()
    private val UUID_HEART_RATE_MEASUREMENT: UUID = UUID.fromString(
        GattAttributes.HEART_RATE_MEASUREMENT)

    private var mBluetoothManager: BluetoothManager? = null
    private var mBluetoothAdapter: BluetoothAdapter? = null
    private var mBluetoothGatt: BluetoothGatt? = null

    private var mHeartRateRecorder : HeartRateRecorder? = null

    private val mGattCallback: BluetoothGattCallback = object: BluetoothGattCallback() {
        override fun onConnectionStateChange(gatt: BluetoothGatt?, status: Int, newState: Int) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.i(TAG, "Connected to GATT server.")
                broadcastUpdate(ACTION_GATT_CONNECTED)
                gatt?.discoverServices()
            }
            else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.i(TAG, "Disconnected from GATT server.")
                broadcastUpdate(ACTION_GATT_DISCONNECTED)
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt?, status: Int) {
        }

        override fun onCharacteristicChanged(
            gatt: BluetoothGatt?,
            characteristic: BluetoothGattCharacteristic?
        ) {
            if (characteristic != null) {
                characteristicUpdate(characteristic)
            }
        }
    }

    private fun broadcastUpdate(action: String) {
        val intent: Intent = Intent(action)
        sendBroadcast(intent)
    }


    private fun characteristicUpdate (characteristic: BluetoothGattCharacteristic) {
        if (UUID_HEART_RATE_MEASUREMENT == characteristic.uuid) {
            val flag: Int = characteristic.properties
            val format: Int
            format = if ((flag and 0x01) != 0) {
                BluetoothGattCharacteristic.FORMAT_UINT16
            } else {
                BluetoothGattCharacteristic.FORMAT_UINT8
            }
            val heartRate: Int = characteristic.getIntValue(format, 1)
            Log.d(TAG, "Received heart rate $heartRate")
            mHeartRateRecorder?.newReading(heartRate)
        }
    }

    /**
     * Enables or disables notification on the heart-rate characteristic
     *
     * @param enabled If true, enable notification.  False otherwise.
     */
    fun signUpHeartRate(
        enabled: Boolean
    ) {
        if (mBluetoothAdapter == null || mBluetoothGatt == null) {
            Log.w(TAG, "BluetoothAdapter not initialized")
            return
        }
        val characteristic : BluetoothGattCharacteristic = mBluetoothGatt?.
            getService(
                UUID.fromString(GattAttributes.HEART_RATE_SERVICE))?.
            getCharacteristic(UUID_HEART_RATE_MEASUREMENT)!!

        characteristic.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT

        mBluetoothGatt!!.setCharacteristicNotification(characteristic, enabled)

        if (enabled) {
            val descriptor =
                characteristic.getDescriptor(UUID.fromString(GattAttributes.CLIENT_CHARACTERISTIC_CONFIG))
            descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            mBluetoothGatt!!.writeDescriptor(descriptor)

            mBluetoothGatt!!.readCharacteristic(characteristic)
        }

    }


    inner class LocalBinder: Binder() {
        fun getService() : HeartDeviceService {
            return this@HeartDeviceService
        }
    }

    override fun onBind(intent: Intent?): IBinder? {
        return mBinder
    }

    private val mBinder: IBinder = LocalBinder()

    override fun onDestroy() {
        // Close the GattConnection when we stop the service.
        close()
        super.onDestroy()
    }


    /**
     * After using a given BLE device, the app must call this method to ensure resources are
     * released properly.
     */
    private fun close() {
        mBluetoothGatt?.close()
        mBluetoothGatt = null
    }

    fun initialize() : Boolean {
        if (mBluetoothManager == null) {
            mBluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        }

        if (mBluetoothManager == null) {
            Log.e(TAG, "Unable to initialize BluetoothManager.")
            return false
        }
        mBluetoothAdapter = mBluetoothManager!!.adapter
        if (mBluetoothAdapter == null) {
            Log.e(TAG, "Unable to obtain BluetoothAdapter.")
            return false
        }

        return true
    }

    /**
     * Attempt to connect to the given device.
     *
     * @param device we want to connect to
     * @return true if attempt began, false otherwise
     */
    fun connect(device : BluetoothDevice) : Boolean {
        if (mBluetoothAdapter == null) {
            Log.w(TAG, "BluetoothAdapter not initialized")
            return false
        }

        mBluetoothGatt = device.connectGatt(this, true, mGattCallback, BluetoothDevice.TRANSPORT_LE)
        Log.d(TAG, "Trying to create a new connection.")
        return true
    }

    /**
     * Start recording from device
     *
     * @return true if recording started, false if something went wrong
     */
    fun record(): Boolean {
        if (mBluetoothAdapter == null || mBluetoothManager?.getConnectionState(mBluetoothGatt?.device, BluetoothProfile.GATT_SERVER) != BluetoothProfile.STATE_CONNECTED) {
            Log.w(TAG, "BluetoothAdapter not initialized or device not connected")
            return false
        }

        mHeartRateRecorder = HeartRateRecorder()

        signUpHeartRate(true)
        Log.d(TAG, "Trying to start a new recording.")

        return true
    }


    /**
     * Start saving current recording from device
     *
     * @return true if saving started, false if something went wrong
     */
    fun save(directory: File): Boolean {
            if (mBluetoothAdapter == null || mBluetoothManager?.getConnectionState(mBluetoothGatt?.device, BluetoothProfile.GATT_SERVER) != BluetoothProfile.STATE_CONNECTED) {
            Log.w(TAG, "BluetoothAdapter not initialized or device not connected")
            return false
        }

        signUpHeartRate(false)
        Log.d(TAG, "Trying to save recording.")

        val listener: SaveListener = object : SaveListener() {
            override fun onSave() {
                Log.d(TAG, "Recording saved to $directory")
                broadcastUpdate(ACTION_SAVED)
            }
        }

        mHeartRateRecorder?.save(directory, listener)

        return true
    }
}


