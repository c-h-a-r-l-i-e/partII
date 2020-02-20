read -p 'Insert Watch IP: ' ip
adb connect $ip
adb pull /sdcard/Android/data/com.charliemaclean.ppgrecorder/
