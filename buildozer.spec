[app]
title = Zartas AI
package.name = zartas
package.domain = org.zartas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Важно: эти версии идеально подходят под сервер GitHub
requirements = python3==3.11.14,kivy==2.3.0,hostpython3==3.11.14

orientation = portrait
fullscreen = 1

# Разрешения для работы ИИ
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# Включаем подробный лог, чтобы видеть ошибки
log_level = 2

[buildozer]
log_level = 2
build_dir = ./.buildozer
bin_dir = ./bin
