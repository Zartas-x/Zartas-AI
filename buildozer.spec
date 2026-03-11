[app]

# (str) Title of your application
title = Zartas AI Ultra

# (str) Package name
package.name = zartasai

# (str) Package domain (needed for android packaging)
package.domain = org.zartas

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's keep it simple)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 19.1

# (list) Application requirements
# ВАЖНО: Мы добавили все библиотеки для работы сети и SSL
requirements = python3,kivy==2.3.0,requests,urllib3,chardet,certifi,idna

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
# Разрешаем интернет, иначе Gemini не ответит
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
android.sdk = 33

# (str) Android build tools version to use
android.build_tools_version = 33.0.0

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Android NDK directory to use
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be signed for caching
android.debug = True

# (str) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
