package com.charliemaclean.heaphonerecorder

import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.*
import android.os.Bundle
import android.os.IBinder
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.Button
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import android.content.IntentFilter
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.R.attr.name




class MainActivity : Activity() {
    private val TAG : String = MainActivity::class.java.simpleName

    private var mBluetoothAdapter: BluetoothAdapter? = null
    private var mDevice: BluetoothDevice? = null
    private var mHeartDeviceService: HeartDeviceService? = null
    private var mIsBound: Boolean = false
    private var mServiceStarted: Boolean = false
    private var mRecordingStarted: Boolean = false
    private var mConnected: Boolean = false

    // Set up the formatters used to store the data. The data will be stored under directory
    // recordings/[date]/[time]
    private val dateFormatter: DateTimeFormatter = DateTimeFormatter.ISO_LOCAL_DATE
    private val timeFormatter: DateTimeFormatter = DateTimeFormatter.ofPattern("HH.mm.ss.SSS")

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
                    findViewById<Button>(R.id.start).text = getString(R.string.start)
                    findViewById<Button>(R.id.start).isEnabled = true
                    mRecordingStarted = false

                }
            }

        }
    }

    fun showConnected(connected: Boolean) {
        if (connected) {
            Toast.makeText(this, "Connected to HR device", Toast.LENGTH_SHORT).show()
            findViewById<Button>(R.id.connect).isEnabled = false
            findViewById<Button>(R.id.start).isEnabled = true
        }
        else {
            Toast.makeText(this, "Disconnected from HR device", Toast.LENGTH_SHORT).show()
            findViewById<Button>(R.id.connect).isEnabled = true
            findViewById<Button>(R.id.start).isEnabled = false
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.connect).setOnClickListener { scan() }
        findViewById<Button>(R.id.start).setOnClickListener { startClick() }

        val bluetoothManager: BluetoothManager  = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        mBluetoothAdapter = bluetoothManager.adapter
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


    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }


    private fun startClick() {
        // Stop recording and save
        if (mRecordingStarted) {
            val date: String = LocalDateTime.now().format(dateFormatter)
            val time: String = LocalDateTime.now().format(timeFormatter)
            val directory = File(
                applicationContext.getExternalFilesDir(null), "recordings/$date/$time"
            )
            directory.mkdirs()
            mHeartDeviceService?.save(directory)
            // Don't allow clicks whilst saving!
            findViewById<Button>(R.id.start).isEnabled = false
        }
        // Start recording
        else {
            mHeartDeviceService?.record()
            findViewById<Button>(R.id.start).text = getString(R.string.stop)
            mRecordingStarted = true
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
