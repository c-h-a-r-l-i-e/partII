package com.charliemaclean.ppgrecorder

import java.io.File
import com.opencsv.CSVWriter
import kotlin.concurrent.thread

class EarHRRecorder() {
    private var recording: ArrayList<Pair<Long, Int>> = arrayListOf()

    /**
     * Add a new reading to the recording
     *
     * @param reading the new reading.
     */
    fun newReading(reading: Int) {
        recording.add(Pair(System.currentTimeMillis(), reading))
    }

    /**
     * Run save in a seperate thread so we are not doing work on the UI thread.
     *
     * @param directory where we want to save the hr.csv file.
     * @param listener to be called when the files is saved.
     */
    fun save(directory: File, listener: SaveListener) {
        thread {
            var file = File(directory, "ear.csv")
            var i = 1
            while (file.exists()) {
                file = File(directory, "ear($i).csv")
                i++
            }
            val csvWriter = CSVWriter(file.writer(),
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END)

            // Write header to CSV
            csvWriter.writeNext(arrayOf("time", "value"))

            // For each recorded PPG value, write (time, value) to the CSV.
            recording.iterator().forEach {
                val value: Int = it.second
                val entry = arrayOf(it.first.toString(), value.toString())
                csvWriter.writeNext(entry)
            }
            csvWriter.close()
            listener.onSave()
        }
    }
}