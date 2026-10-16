[app]

# (str) Title of your application
title = My Python App

# (str) Package name
package.name = mypythonapp

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source files where the let (let me know if you have other folders)
source.dir = .

# (list) Source files to include (let me know if you have assets)
source.exts = py,png,jpg,kv,atlas

# (list) Application version
version = 0.1

# (list) Application requirements
# Обязательно только python3 и графический движок (например, kivy). 
# Важно: tkinter сюда писать нельзя, он на Android не работает!
requirements = python3,kivy

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.min_api = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 23b

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
