package com.charliemaclean.ppgrecorder

import android.hardware.Sensor
import android.hardware.SensorEvent
import java.io.File
import com.opencsv.CSVWriter
import java.util.*
import kotlin.concurrent.thread

class AccelerometerRecorder : SensorRecorder{
    private var recording : ArrayList<Pair<Long, Triple<Float,Float,Float>>> = arrayListOf()
    override fun onAccuracyChanged(sensor: Sensor, value: Int) {
    }

    override fun onSensorChanged(event: SensorEvent) {
        recording.add(Pair(System.currentTimeMillis(), Triple(event.values[0],
            event.values[1],event.values[2])))
    }

    /**
     * Save the PPG recording as [filename] in the directory of the app given by [context].
     * The data is stored as a csv of floating point values, with a column for linear acceleration
     * in the x, y and z directions.
     */
    override fun save(directory: File, listener: SaveListener) {
        thread {
            // Find a filename that doesn't already exist
            var file = File(directory, "accelerometer.csv")
            var i = 1
            while (file.exists()) {
                file = File(directory, "accelerometer($i).csv")
                i++
            }
            val csvWriter = CSVWriter(
                file.writer(),
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END
            )

            //Write header
            csvWriter.writeNext(arrayOf("time", "x", "y", "z"))

            // For each recorded accelerometer value, write (time, x, y, z) to the CSV.
            recording.iterator().forEach {
                val acceleration = it.second
                val entry = arrayOf(
                    it.first.toString(),
                    acceleration.first.toString(),
                    acceleration.second.toString(),
                    acceleration.third.toString()
                )

                csvWriter.writeNext(entry)
            }
            csvWriter.close()
            listener.onSave()
        }
    }
}