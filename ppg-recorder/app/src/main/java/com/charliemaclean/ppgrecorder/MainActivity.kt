package com.charliemaclean.ppgrecorder

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.hardware.Sensor
import android.hardware.SensorManager
import android.os.Bundle
import android.os.PowerManager
import android.support.wearable.activity.WearableActivity
import android.view.View
import android.widget.Button
import java.time.LocalDateTime
import android.os.StrictMode
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.util.Log
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.common.api.Scope
import com.google.android.gms.tasks.Tasks
import com.google.api.client.extensions.android.http.AndroidHttp
import com.google.api.services.drive.Drive
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.googleapis.extensions.android.gms.auth.UserRecoverableAuthIOException
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.drive.DriveScopes
import com.google.api.services.drive.model.File
import java.util.*
import java.util.concurrent.Callable
import java.util.concurrent.Executors


class MainActivity : WearableActivity() {
    private lateinit var sensorManager: SensorManager
    private var recording: Boolean = false

    private lateinit var ppgListener: PpgListener
    private lateinit var accelerometerListener: AccelerometerListener
    private lateinit var rotationListener: RotationListener
    private lateinit var hrListener: HRListener

    private lateinit var ppgSensor: Sensor
    private lateinit var hrSensor: Sensor
    private lateinit var accelerometerSensor: Sensor
    private lateinit var rotationSensor: Sensor

    private lateinit var wakeLock: PowerManager.WakeLock

    private lateinit var googleDriveService : Drive
    private val REQUEST_CODE_SIGN_IN = 1
    private val executor = Executors.newSingleThreadExecutor()


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Enables Always-on
        setAmbientEnabled()

        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager

        // Find the sensors
        hrSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)
        accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)
        rotationSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)

        // Find the PPG sensor, has numerical code 65572 on Fossil gen 5.
        ppgSensor = sensorManager.getDefaultSensor(65572)

        val account : GoogleSignInAccount? = GoogleSignIn.getLastSignedInAccount(this)
        if (account == null) {
            requestSignIn()
        } else {
            setupGoogleDrive(account)
        }
    }


    /**
     * Create new listeners and set them to receive updates from the sensors.
     */
    private fun registerListeners() {
        ppgListener = PpgListener()
        accelerometerListener = AccelerometerListener()
        rotationListener = RotationListener()
        hrListener = HRListener()

        sensorManager.registerListener(ppgListener, ppgSensor, SensorManager.SENSOR_DELAY_FASTEST)
        sensorManager.registerListener(hrListener, hrSensor, SensorManager.SENSOR_DELAY_FASTEST)
        sensorManager.registerListener(rotationListener, rotationSensor, SensorManager.SENSOR_DELAY_FASTEST)
        sensorManager.registerListener(accelerometerListener, accelerometerSensor, SensorManager.SENSOR_DELAY_FASTEST)
    }


    /**
     * Stop listeners receiving updates from the sensors.
     */
    private fun unregisterListeners() {
        sensorManager.unregisterListener(ppgListener)
        sensorManager.unregisterListener(hrListener)
        sensorManager.unregisterListener(rotationListener)
        sensorManager.unregisterListener(accelerometerListener)
    }


    /**
     * Create a new directory with a name based on current data and time, then save collected data
     * there.
     */
    fun saveResults() {
        // Create a new directory with based on current time, then save the collected data there.
        val directory = java.io.File(applicationContext.getExternalFilesDir(null),
            "recording_" + LocalDateTime.now().toString())
        directory.mkdirs()


        ppgListener.save(directory)
        hrListener.save(directory)
        rotationListener.save(directory)
        accelerometerListener.save(directory)
    }


    /**
     * Called when start/stop button is pressed.
     */
    fun onStartStopClick(view: View){
        val button: Button = findViewById(R.id.button_startstop)
        saveFileToGoogleDrive(java.io.File("/"))

        // Stop recording and save the results
        if (recording) {
            recording = false
            wakeLock.release()
            unregisterListeners()
            saveResults()
            button.setText(R.string.start)
            button.setBackgroundColor(Color.GREEN)
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
            button.setBackgroundColor(Color.RED)
        }
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        // Sign in result has code 1
        if (requestCode == REQUEST_CODE_SIGN_IN && resultCode == Activity.RESULT_OK && data != null) {
            handleSignInResult(data)
        }

        super.onActivityResult(requestCode, resultCode, data)
    }


    private fun requestSignIn() {
        val signInOptions : GoogleSignInOptions = GoogleSignInOptions
            .Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail()
            .build()

        val client : GoogleSignInClient = GoogleSignIn.getClient(this, signInOptions)
        startActivityForResult(client.signInIntent, REQUEST_CODE_SIGN_IN)
    }

    private fun handleSignInResult(result : Intent) {
        GoogleSignIn.getSignedInAccountFromIntent(result)
            .addOnSuccessListener {
                setupGoogleDrive(it)
            }
            .addOnFailureListener {
                Log.e("MainActivity", "Cannot sign in", it)
            }
    }

    private fun setupGoogleDrive(googleSignInAccount: GoogleSignInAccount) {
        val credential : GoogleAccountCredential = GoogleAccountCredential.usingOAuth2(
            this, Collections.singleton(DriveScopes.DRIVE_FILE))

        credential.selectedAccount = googleSignInAccount.account

        googleDriveService = Drive.Builder(AndroidHttp.newCompatibleTransport(), GsonFactory(), credential)
            .setApplicationName("PPG Recorder")
            .build()
    }

    private fun saveFileToGoogleDrive(file: java.io.File) {
        Tasks.call(executor, Callable {
            val metadata : File = File()
                .setParents(Collections.singletonList("root"))
                .setMimeType("text/plain")
                .setName("Test File")

            val googleFile: File = googleDriveService.files().create(metadata).execute()

        }
        )  .addOnSuccessListener { Log.d("Main Activity", "Uploaded file ${file.name}") }
            .addOnFailureListener { Log.e("Main Activity", "Couldn't create file", it) }
    }
}
