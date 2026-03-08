[app]
# (str) Title of your application
title = Zartas AI

# (str) Package name
package.name = zartasai

# (str) Package domain (needed for android packaging)
package.domain = org.zartas

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# ВАЖНО: Здесь я добавил requests и все его зависимости
requirements = python3,kivy,requests,urllib3,chardet,certifi,idna

# (str) Custom source folders for requirements
# садят зависимости прямо в APK
# requirements.source.kivy = ../kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
# ВАЖНО: Разрешение на интернет, чтобы Gemini мог отвечать
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 33

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) Use architectures
android.archs = arm64-v8a, armeabi-v7a

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Для эмуляторов типа LDPlayer важны x86 или v7a
# android.archs = arm64-v8a

# (bool) indicates if the application should be etched in debug mode
android.debug = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
