package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import java.io.File
import com.opencsv.CSVWriter
import java.util.*
import kotlin.concurrent.thread

class RotationListener : SensorListener {
    private var recording : ArrayList<Pair<Long, Triple<Float,Float,Float>>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(),
            Triple(event.values[0],event.values[1],event.values[2])))
    }

    /**
     * Save the PPG recording as ppg.csv in [directory].
     */
    override fun save(directory: File, listener: SaveListener) {
        thread {
            // Find a filename that doesn't already exist
            var file = File(directory, "rotation.csv")
            var i = 0
            while (file.exists()) {
                file = File(directory, "rotation($i).csv")
                i++
            }
            val csvWriter = CSVWriter(
                file.writer(),
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END
            )

            // Write a header to the CSV
            csvWriter.writeNext(arrayOf("time", "x", "y", "z"))

            // For each recorded PPG value, write 'time, x, y, z' to the CSV.
            recording.iterator().forEach {
                val rotation = it.second
                val entry = arrayOf(
                    it.first.toString(), rotation.first.toString(),
                    rotation.second.toString(), rotation.third.toString()
                )

                csvWriter.writeNext(entry)
            }
            csvWriter.close()
            listener.onSave()
        }
    }
}