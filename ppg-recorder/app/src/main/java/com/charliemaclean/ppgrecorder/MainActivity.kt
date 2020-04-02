package com.charliemaclean.ppgrecorder

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.*
import android.graphics.Color
import android.hardware.Sensor
import android.hardware.SensorManager
import android.os.Bundle
import android.os.IBinder
import android.os.PowerManager
import android.support.wearable.activity.WearableActivity
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class MainActivity : WearableActivity(){
    private val TAG : String = MainActivity::class.java.simpleName

    private lateinit var sensorManager: SensorManager

    private val PPG = false // false for HR, true for PPG
    private val EARBUD = true // record the earbud's HR?

    private lateinit var ppgRecorder: PpgRecorder
    private lateinit var accelerometerRecorder: AccelerometerRecorder
    private lateinit var rotationRecorder: RotationRecorder
    private lateinit var hrRecorder: HRRecorder

    private lateinit var ppgSensor: Sensor
    private lateinit var accelerometerSensor: Sensor
    private lateinit var rotationSensor: Sensor
    private lateinit var hrSensor: Sensor

    private lateinit var wakeLock: PowerManager.WakeLock

    // Set up the formatters used to store the data. The data will be stored under directory
    // recordings/[date]/[time]
    private val dateFormatter = DateTimeFormatter.ISO_LOCAL_DATE
    private val timeFormatter = DateTimeFormatter.ofPattern("HH.mm.ss.SSS")

    private val sync: Sync = Sync()

    private var mBluetoothAdapter: BluetoothAdapter? = null
    private var mDevice: BluetoothDevice? = null
    private var mHeartDeviceService: HeartDeviceService? = null
    private var mIsBound: Boolean = false
    private var mServiceStarted: Boolean = false
    private var mRecordingStarted: Boolean = false
    private var mConnected: Boolean = false
    private var mSavingCount: Int = 0

    private val mServiceConnection: ServiceConnection = object: ServiceConnection {
        override fun onServiceConnected(componentName: ComponentName, service: IBinder) {
            mHeartDeviceService = (service as HeartDeviceService.LocalBinder).getService()
            if (!mHeartDeviceService!!.initialize()) {
                Log.e(TAG, "Unable to initialize Bluetooth")
                finish()
            }

            mDevice?.let { mHeartDeviceService!!.connect(it) }
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            mHeartDeviceService = null
        }
    }

    // Handles various events fired by the Service.
    // ACTION_GATT_CONNECTED: connected to a GATT server.
    // ACTION_GATT_DISCONNECTED: disconnected from a GATT server.
    // ACTION_RECORDING_STARTED: heart-rate data is currently being recorded.
    // ACTION_SAVED: heart-rate data has been saved
    private val mGattUpdateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            val action = intent.action
            when {
                HeartDeviceService.ACTION_GATT_CONNECTED.equals(action) -> {
                    mConnected = true
                    showConnected(mConnected)
                }
                HeartDeviceService.ACTION_GATT_DISCONNECTED.equals(action) -> {
                    mConnected = false
                    showConnected(mConnected)
                }
                HeartDeviceService.ACTION_SAVED.equals(action) -> {
                    mRecordingStarted = false
                    saveListener.onSave()
                }
            }

        }
    }

    fun showConnected(connected: Boolean) {
        if (connected) {
            Toast.makeText(this, "Connected to HR device", Toast.LENGTH_SHORT).show()
            findViewById<TextView>(R.id.ear_status).text = getString(R.string.ear_connected)
        }
        else {
            Toast.makeText(this, "Disconnected from HR device", Toast.LENGTH_SHORT).show()
            findViewById<TextView>(R.id.ear_status).text = getString(R.string.ear_disconnected)
        }
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Enables Always-on
        setAmbientEnabled()

        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager

        // Find the sensors
        hrSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE )

        // Find the PPG sensor, has numerical code 65572 on Fossil gen 5.
        if (PPG) {
//            ppgSensor = sensorManager.getDefaultSensor(65572)
//            rotationSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)
        }
        accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)

        // Initialise the earbud HR sensor
        val ear_status: TextView = findViewById(R.id.ear_status)
        if (EARBUD) {
            ear_status.text = getText(R.string.ear_disconnected)
            val bluetoothManager: BluetoothManager = getSystemService(
                Context.BLUETOOTH_SERVICE
            ) as BluetoothManager
            mBluetoothAdapter = bluetoothManager.adapter
            scan()
        }
        else {
            ear_status.text = getText(R.string.ear_disabled)
        }
    }


    /**
     * Create new listeners and set them to receive updates from the sensors.
     */
    private fun registerListeners() {
        if (PPG) {
//            ppgRecorder = PpgRecorder()
//            sensorManager.registerListener(
//                ppgRecorder,
//                ppgSensor,
//                SensorManager.SENSOR_DELAY_FASTEST
//            )
//            rotationRecorder = RotationRecorder()
//            sensorManager.registerListener(
//                rotationRecorder,
//                rotationSensor,
//                SensorManager.SENSOR_DELAY_FASTEST
//            )
//
        } else {
            Log.d(TAG, "Registering heart-rate recorder")
            hrRecorder = HRRecorder()
            sensorManager.registerListener(
                hrRecorder,
                hrSensor,
                SensorManager.SENSOR_DELAY_FASTEST
            )

        }

        accelerometerRecorder = AccelerometerRecorder()
        sensorManager.registerListener(
            accelerometerRecorder,
            accelerometerSensor,
            SensorManager.SENSOR_DELAY_FASTEST
        )



        if (EARBUD) {
            mHeartDeviceService?.record()
        }
    }


    /**
     * Stop listeners receiving updates from the sensors.
     */
    private fun unregisterListeners() {
        if (PPG) {
            sensorManager.unregisterListener(ppgRecorder)
            sensorManager.unregisterListener(rotationRecorder)
        } else {
            sensorManager.unregisterListener(hrRecorder)
        }
        sensorManager.unregisterListener(accelerometerRecorder)
    }




    /**
     * Create a new directory with a name based on current data and time, then save collected data
     * there.
     */
    private fun saveResults() {
        // Create a new directory with based on current time, then save the collected data there.
        val date: String = LocalDateTime.now().format(dateFormatter)
        val time: String = LocalDateTime.now().format(timeFormatter)
        val directory = File(
            applicationContext.getExternalFilesDir(null), "recordings/$date/$time"
        )
        directory.mkdirs()

        if (PPG) {
            ppgRecorder.save(directory, saveListener)
            rotationRecorder.save(directory, saveListener)
            mSavingCount = 3
        } else {
            hrRecorder.save(directory, saveListener)
            mSavingCount = 2
        }
        accelerometerRecorder.save(directory, saveListener)

        if (EARBUD) {
            mSavingCount ++
            mHeartDeviceService?.save(directory)
        }
    }


    /**
     * Called when start/stop button is pressed.
     */
    fun onStartStopClick(view: View) {
        val button: Button = findViewById(R.id.button_startstop)

        // Stop recording and save the results
        if (mRecordingStarted) {
            mRecordingStarted = false

            button.setText(R.string.saving)
            button.setBackgroundColor(Color.BLACK)
            button.isEnabled = false
            button.setTextColor(Color.WHITE)

            unregisterListeners()
            saveResults()
        }

        // Start the recording
        else {
            mRecordingStarted = true

            // Obtain a wakelock to ensure the listeners are active while updates are being provided
            wakeLock = (getSystemService(Context.POWER_SERVICE) as PowerManager).run {
                newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ppgrecorder:ListenerLock").apply {
                    acquire()
                }
            }

            registerListeners()
            button.setText(R.string.stop)
            button.setBackgroundColor(Color.DKGRAY)
        }
    }

    /**
     * Called when a Recorder object has finished saving.
     */
    private val saveListener: SaveListener = object: SaveListener() {
        @Synchronized
        override fun onSave() {
            mSavingCount -= 1

            // All are saved!
            if (mSavingCount == 0) {
                runOnUiThread{
                    val button: Button = findViewById(R.id.button_startstop)

                    button.setText(R.string.start)
                    button.setBackgroundColor(Color.LTGRAY)
                    button.isEnabled = true
                    button.setTextColor(Color.BLACK)

                    wakeLock.release()
                }
            }
        }
    }



    /**
     * Called when sync button is pressed. Moves all the files in the recordings folder to the
     * server.
     */
    fun onSyncClick(view: View) {
        val directory = File(applicationContext.getExternalFilesDir(null), "recordings")
        sync.syncFiles(directory)
    }


    /**
     * Log a list of all sensors available on the device.
     */
    fun logSensors(){
        val sensorManager : SensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        val sensors : List<Sensor> = sensorManager.getSensorList(Sensor.TYPE_ALL)
        for (sensor in sensors) {
            Log.d("SensorList", sensor.toString())

        }
    }
    override fun onDestroy() {
        doDestroyService()
        super.onDestroy()
    }

    override fun onStart() {
        doBindService()
        super.onStart()
    }

    override fun onStop() {
        doUnbindService()
        super.onStop()
    }

    override fun onResume() {
        super.onResume()
        registerReceiver(mGattUpdateReceiver, makeGattUpdateIntentFilter())
    }

    override fun onPause() {
        super.onPause()
        unregisterReceiver(mGattUpdateReceiver)
    }

    private fun doStartService() {
        if (!mServiceStarted) {
            Intent(this, HeartDeviceService::class.java).also { intent ->
                startService(intent)
            }
            mServiceStarted = true
        }
    }

    private fun doDestroyService() {
        if (mServiceStarted) {
            Intent(this, HeartDeviceService::class.java).also { intent ->
                stopService(intent)
            }
            mServiceStarted = false
        }
    }

    private fun doBindService() {
        if (mServiceStarted) {
            Intent(this, HeartDeviceService::class.java).also { intent ->
                bindService(intent, mServiceConnection, Context.BIND_AUTO_CREATE)
            }
            mIsBound = true
        }
    }

    private fun doUnbindService() {
        if (mIsBound) {
            unbindService(mServiceConnection)
            mIsBound = false
        }
    }


    private fun scan() {
        var found = false
        mBluetoothAdapter?.bondedDevices?.iterator()?.forEach {
            if (it.name == "Jabra Elite [SMART]") {
                mDevice = it
                deviceFound()
                found = true
            }
        }

        if (!found) {
            Log.d(TAG, "Device not found")
        }
    }

    fun deviceFound() {
        Log.d(TAG, "Device found")

        doStartService()
        doBindService()
    }

    private fun makeGattUpdateIntentFilter(): IntentFilter {
        val intentFilter = IntentFilter()
        intentFilter.addAction(HeartDeviceService.ACTION_GATT_CONNECTED)
        intentFilter.addAction(HeartDeviceService.ACTION_GATT_DISCONNECTED)
        intentFilter.addAction(HeartDeviceService.ACTION_SAVED)
        return intentFilter
    }
}

