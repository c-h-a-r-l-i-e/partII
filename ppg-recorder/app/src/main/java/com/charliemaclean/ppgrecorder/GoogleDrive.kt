package com.charliemaclean.ppgrecorder

import android.os.Environment
import android.util.Log
import com.google.api.client.auth.oauth2.Credential
import com.google.api.client.json.jackson2.JacksonFactory
import com.google.api.services.drive.DriveScopes
import java.util.*
import java.util.Collections.singletonList
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver
import com.google.api.client.util.store.FileDataStoreFactory
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
import com.google.api.client.http.javanet.NetHttpTransport
import com.google.api.services.drive.Drive
import com.google.api.services.drive.model.File
import com.google.api.services.drive.model.FileList
import java.io.FileNotFoundException
import java.io.IOException
import java.io.InputStreamReader


class GoogleDrive {
    private val APPLICATION_NAME = "Google Drive API Java Quickstart"
    private val JSON_FACTORY = JacksonFactory.getDefaultInstance()
    private val TOKENS_DIRECTORY_PATH = "tokens"


    /**
     * Global instance of the scopes required by this quickstart.
     * If modifying these scopes, delete your previously saved tokens/ folder.
     */
    private val SCOPES = Collections.singletonList(DriveScopes.DRIVE_METADATA_READONLY)
    private var CREDENTIALS_FILE_PATH = "/sdcard/com.charliemaclean.ppgrecorder/files/credentials.json"


    private fun getCredentials(HTTP_TRANSPORT: NetHttpTransport): Credential {
        // Load client secrets.
        val inp = GoogleDrive::class.java.getResourceAsStream(CREDENTIALS_FILE_PATH)
            ?: throw FileNotFoundException("Resource not found: $CREDENTIALS_FILE_PATH")
        val clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, InputStreamReader(inp))

        // Build flow and trigger user authorization request.
        val flow = (GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT,
                JSON_FACTORY, clientSecrets, SCOPES)
            .setDataStoreFactory(FileDataStoreFactory(java.io.File(TOKENS_DIRECTORY_PATH)))
            .setAccessType("offline")).build()
        val receiver = (LocalServerReceiver.Builder().setPort(8888)).build()
        return AuthorizationCodeInstalledApp(flow, receiver).authorize("user")
    }


    fun uploadFile(file: java.io.File) {
        // Build a new authorized API client service
        val HTTP_TRANSPORT : NetHttpTransport = NetHttpTransport()
        var service : Drive = Drive.Builder(HTTP_TRANSPORT, JSON_FACTORY, getCredentials(HTTP_TRANSPORT))
            .setApplicationName(APPLICATION_NAME)
            .build()

        var result : FileList = service.files().list().setPageSize(10).setFields("nextPageToken, files(id,name)").execute()
        var files : List<File> = result.getFiles()

        if (files == null || files.isEmpty()) {
            Log.d("Files", "No files found.")
        }
        else {
            for (gfile in files) {
                Log.d("Files", gfile.name)
            }
        }
    }
}
