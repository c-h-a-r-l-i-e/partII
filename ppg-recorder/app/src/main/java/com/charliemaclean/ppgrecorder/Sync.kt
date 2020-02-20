package com.charliemaclean.ppgrecorder

import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.IOException
import java.net.URL
import java.nio.file.Files


class Sync {
    private val BASE: String = "http://192.168.0.1:5000/upload/"
    private val client = OkHttpClient()


    /**#
     * Sync all files within a given directory
     */
    fun syncFiles(directory: File) {
        Log.d("Sync", "Sync starting for directory" + directory.name)
        syncFilesRecursive(directory, "")
    }

    /**
     * Sync files recursively, using relativePath describes path from the base directory
     */
    private fun syncFilesRecursive(file: File, relativePath: String) {
        if (file.isFile) {
            syncFile(file, relativePath)
        }
        else if (file.isDirectory) {
            for ( child : File in file.listFiles() ) {
                Log.d("Sync", "Looking at child" + child.name)
                syncFilesRecursive(child, relativePath + file.name + "/")
            }
        }
    }

    /**
     * Sync the file to the server using a HTTP POST
     */
    private fun syncFile(file: File, relativePath: String) {
        Log.d("Sync", "syncing file" + file.name)
        val url = URL(BASE + relativePath + file.name)
        val mimeType: String = Files.probeContentType(file.toPath())
        val mediaType: MediaType = mimeType.toMediaType()
        val body: RequestBody = file.asRequestBody(mediaType)
        val request: Request = Request.Builder().url(url).put(body).build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
            }

            override fun onResponse(call: Call, response: Response) {
            }
        })
    }
}