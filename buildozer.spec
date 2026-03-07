[app]
title = Zartas AI
package.name = zartasai
package.domain = org.zartas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ВАЖНО: Добавил все зависимости для интернета и управления
requirements = python3,kivy==2.3.0,requests,urllib3,chardet,idna,certifi,plyer,pyjnius

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ПРАВА: Интернет + Управление + Железо
android.permissions = INTERNET, ACCESS_NETWORK_STATE, CALL_PHONE, CAMERA, VIBRATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.sdk = 33
android.ndk = 25b
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
