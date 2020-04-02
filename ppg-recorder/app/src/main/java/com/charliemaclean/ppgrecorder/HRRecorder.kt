package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import java.io.File
import com.opencsv.CSVWriter
import java.util.*
import kotlin.concurrent.thread

class PpgRecorder : SensorRecorder {
    private var recording : ArrayList<Pair<Long, Triple<Float,Float,Float>>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event : SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(),
            Triple(event.values[0],event.values[1],event.values[2])))
    }

    /**
     * Save the PPG recording as ppg.csv in [directory].
     */
    override fun save(directory: File, listener: SaveListener) {
        thread {
            // Find a filename that doesn't already exist
            var file = File(directory, "ppg.csv")
            var i = 1
            while (file.exists()) {
                file = File(directory, "ppg($i).csv")
                i++
            }
            val csvWriter = CSVWriter(
                file.writer(),
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END
            )

            // Write header to CSV
            csvWriter.writeNext(arrayOf("time", "value", "value2", "value3"))

            // For each recorded PPG value, write (time, value, value2, value3) to the CSV.
            recording.iterator().forEach {
                val values = it.second
                val entry = arrayOf(
                    it.first.toString(), values.first.toString(),
                    values.second.toString(), values.third.toString()
                )
                csvWriter.writeNext(entry)
            }
            csvWriter.close()
            listener.onSave()
        }
    }
}