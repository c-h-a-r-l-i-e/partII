package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import java.io.File

interface SensorRecorder : SensorEventListener{
    override fun onAccuracyChanged(sensor: Sensor, value: Int)
    override fun onSensorChanged(event: SensorEvent)
    fun save(directory : File, listener:SaveListener)
}