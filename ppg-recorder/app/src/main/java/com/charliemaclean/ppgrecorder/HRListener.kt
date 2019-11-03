package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import java.io.File
import com.opencsv.CSVWriter
import java.util.*

class HRListener : SensorListener {
    private var recording : ArrayList<Pair<Long, Float>> = arrayListOf()

    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(), event.values[0]))
    }

    // TODO: finish documentation
    /**
     * Save the PPG recording as heart-rate.csv in [directory]
     */
    override fun save(directory : File) {
        // Find a filename that doesn't already exist
        var file = File(directory, "heart-rate.csv")
        var i = 1
        while (file.exists()) {
            file = File(directory, "heart-rate($i).csv")
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