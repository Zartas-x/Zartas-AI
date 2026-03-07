[app]
title = Zartas AI Ultra
package.name = zartasai
package.domain = org.zartas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# БИБЛИОТЕКИ (Добавляем Plyer и Pyjnius для управления железом)
requirements = python3,kivy==2.3.0,plyer,pyjnius,requests,urllib3

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ПРАВА (Разрешаем звонить, снимать и лезть в файлы)
android.permissions = INTERNET, CALL_PHONE, SEND_SMS, READ_CONTACTS, WRITE_CONTACTS, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE

android.sdk = 33
android.ndk = 25b
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
