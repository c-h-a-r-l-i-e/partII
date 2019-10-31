package com.example.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.util.Log
import java.time.LocalDateTime

class PpgListener : SensorEventListener {

    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        Log.d("PPGval", event.values[0].toString())
        Log.d("TIME", LocalDateTime.now().toString())
    }

    fun save(filename: String) {

    }
}