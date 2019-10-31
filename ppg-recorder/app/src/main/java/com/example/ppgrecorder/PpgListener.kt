package com.example.ppgrecorder

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import java.io.File
import com.opencsv.CSVWriter
import java.util.*

class PpgListener : SensorEventListener {
    private var recording : ArrayList<Pair<Long, Float>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(), event.values[0]))
    }

    // TODO: finish documentation
    /**
     * Save the PPG recording as [filename] in the directory of the app given by [context]
     * The data is stored as a csv,
     */
    fun save(filename: String, context: Context) {
        // Find a filename that doesn't already exist
        var file = File(context.getExternalFilesDir(null), "$filename.csv")
        var i = 0
        while (file.exists()) {
            file = File(context.getExternalFilesDir(null), "$filename($i).csv")
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