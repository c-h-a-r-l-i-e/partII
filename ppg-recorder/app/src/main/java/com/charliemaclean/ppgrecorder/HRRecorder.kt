package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import android.util.Log
import java.io.File
import com.opencsv.CSVWriter
import java.util.*
import kotlin.concurrent.thread

class HRRecorder : SensorRecorder {
    private val TAG: String = HRRecorder::class.simpleName.toString()

    private var recording : ArrayList<Pair<Long, Pair<Float, Int>>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event : SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(), Pair(event.values[0], event.accuracy)))
    }

    /**
     * Save the PPG recording as ppg.csv in [directory].
     */
    override fun save(directory: File, listener: SaveListener) {
        thread {
            // Find a filename that doesn't already exist
            var file = File(directory, "hr.csv")
            var i = 1
            while (file.exists()) {
                file = File(directory, "hr($i).csv")
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
            csvWriter.writeNext(arrayOf("time", "value", "accuracy"))

            // For each recorded PPG value, write (time, value, value2, value3) to the CSV.
            recording.iterator().forEach {
                val values = it.second
                val entry = arrayOf(
                    it.first.toString(), values.first.toString(), values.second.toString()
                )
                csvWriter.writeNext(entry)
            }
            csvWriter.close()
            listener.onSave()
        }
    }
}