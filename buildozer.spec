[app]
# (str) Title of your application
title = Zartas AI

# (str) Package name
package.name = zartasai

# (str) Package domain (needed for android packaging)
package.domain = org.zartas

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# ВАЖНО: Все библиотеки для работы сети
requirements = python3,kivy,requests,urllib3,chardet,certifi,idna

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android build-tools version to use
# ВАЖНО: Фиксируем стабильную версию, чтобы не было ошибки лицензии
android.build_tools_version = 33.0.0

# (bool) Use architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be etched in debug mode
android.debug = True

[buildozer]
# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
