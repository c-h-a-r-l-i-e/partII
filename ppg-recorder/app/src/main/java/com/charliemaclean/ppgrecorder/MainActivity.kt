package com.charliemaclean.ppgrecorder

import android.content.Context
import android.graphics.Color
import android.hardware.Sensor
import android.hardware.SensorManager
import android.os.Bundle
import android.os.PowerManager
import android.support.wearable.activity.WearableActivity
import android.view.View
import android.widget.Button
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class MainActivity : WearableActivity() {
    private lateinit var sensorManager: SensorManager
    private var recording: Boolean = false

    private lateinit var ppgListener: PpgListener
    private lateinit var accelerometerListener: AccelerometerListener
    private lateinit var rotationListener: RotationListener

    private lateinit var ppgSensor: Sensor
    private lateinit var accelerometerSensor: Sensor
    private lateinit var rotationSensor: Sensor

    private lateinit var wakeLock: PowerManager.WakeLock

    // Set up the formatters used to store the data. The data will be stored under directory
    // recordings/[date]/[time]
    private val dateFormatter = DateTimeFormatter.ISO_LOCAL_DATE
    private val timeFormatter = DateTimeFormatter.ofPattern("HH.mm.ss.SSS")


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Enables Always-on
        setAmbientEnabled()

        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager

        // Find the sensors
        accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)
        rotationSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)

        // Find the PPG sensor, has numerical code 65572 on Fossil gen 5.
        ppgSensor = sensorManager.getDefaultSensor(65572)
    }


    /**
     * Create new listeners and set them to receive updates from the sensors.
     */
    private fun registerListeners() {
        ppgListener = PpgListener()
        accelerometerListener = AccelerometerListener()
        rotationListener = RotationListener()

        sensorManager.registerListener(
            ppgListener,
            ppgSensor,
            SensorManager.SENSOR_DELAY_FASTEST
        )
        sensorManager.registerListener(
            rotationListener,
            rotationSensor,
            SensorManager.SENSOR_DELAY_FASTEST
        )
        sensorManager.registerListener(
            accelerometerListener,
            accelerometerSensor,
            SensorManager.SENSOR_DELAY_FASTEST
        )
    }


    /**
     * Stop listeners receiving updates from the sensors.
     */
    private fun unregisterListeners() {
        sensorManager.unregisterListener(ppgListener)
        sensorManager.unregisterListener(rotationListener)
        sensorManager.unregisterListener(accelerometerListener)
    }


    /**
     * Create a new directory with a name based on current data and time, then save collected data
     * there.
     */
    private fun saveResults() {
        // Create a new directory with based on current time, then save the collected data there.
        val date: String = LocalDateTime.now().format(dateFormatter)
        val time: String = LocalDateTime.now().format(timeFormatter)
        val directory = java.io.File(
            applicationContext.getExternalFilesDir(null), "recordings/$date/$time"
        )
        directory.mkdirs()

        ppgListener.save(directory)
        rotationListener.save(directory)
        accelerometerListener.save(directory)
    }


    /**
     * Called when start/stop button is pressed.
     */
    fun onStartStopClick(view: View) {
        val button: Button = findViewById(R.id.button_startstop)

        // Stop recording and save the results
        if (recording) {
            recording = false

            button.setText(R.string.saving)
            button.setBackgroundColor(Color.BLACK)
            button.isEnabled = false
            button.setTextColor(Color.WHITE)

            wakeLock.release()
            unregisterListeners()
            saveResults()

            button.setText(R.string.start)
            button.setBackgroundColor(Color.LTGRAY)
            button.isEnabled = true
            button.setTextColor(Color.BLACK)
        }

        // Start the recording
        else {
            recording = true

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
}
