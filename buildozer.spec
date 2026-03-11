[app]
title = Zartas AI
package.name = zartasai
package.domain = org.zartas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,hostpython3,requests,urllib3,chardet,certifi,idna
# ВАЖНО: Если сборка упадет на tkinter, заменим на Kivy позже, 
# но пока пробуем оживить твой код 19.1

orientation = portrait
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# ФИКСИРУЕМ ВСЁ
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools_version = 33.0.0
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1
