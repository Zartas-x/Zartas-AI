[app]
title = Zartas AI
package.name = zartasai
package.domain = org.zartas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ВАЖНО: Убрал лишние пробелы и добавил только нужные зависимости
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna,plyer,pyjnius

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ПРАВА (Минимум для работы связи и базы)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, VIBRATE

# ТЕХНИЧЕСКИЕ ПРАВКИ ДЛЯ ГИТХАБА:
android.sdk = 33
android.ndk = 25b
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1
