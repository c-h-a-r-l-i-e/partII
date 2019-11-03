package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import java.io.File
import com.opencsv.CSVWriter
import java.util.*

class RotationListener : SensorListener {
    private var recording : ArrayList<Pair<Long, Triple<Float,Float,Float>>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(), Triple(event.values[0],event.values[1],event.values[2])))
    }

    // TODO: finish documentation
    /**
     * Save the PPG recording as [filename] in the directory of the app given by [context]
     */
    override fun save(directory: File) {
        // Find a filename that doesn't already exist
        var file = File(directory, "rotation.csv")
        var i = 0
        while (file.exists()) {
            file = File(directory, "rotation($i).csv")
            i++
        }
        val csvWriter = CSVWriter(file.writer())

        // For each recorded PPG value, write a pair (time, value) to the CSV.
        recording.iterator().forEach {
            val entry = arrayOf(it.first.toString(), it.second.toString())
            csvWriter.writeNext(entry)
        }
        csvWriter.close()
    }
}