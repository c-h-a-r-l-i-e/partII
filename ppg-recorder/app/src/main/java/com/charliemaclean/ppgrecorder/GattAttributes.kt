package com.charliemaclean.ppgrecorder

import java.util.*

class GattAttributes {
    companion object {
        private val attributes: HashMap<String, String> = HashMap()
        const val HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
        const val HEART_RATE_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
        const val CLIENT_CHARACTERISTIC_CONFIG = "00002902-0000-1000-8000-00805f9b34fb"

        init {
            attributes.put("0000180d-0000-1000-8000-00805f9b34fb", "Heart Rate Service")
            attributes.put("00002a37-0000-1000-8000-00805f9b34fb", "Heart Rate Measurement")
        }
    }
}
