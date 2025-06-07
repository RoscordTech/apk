[app]

# (str) Title of your application
title = Trayectos

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# MODIFICADO: Unificado en una sola línea y añadido setuptools para estabilidad.
requirements = python3,kivy,sqlite3,setuptools

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# MODIFICADO: Descomentado el permiso de INTERNET, casi siempre necesario.
android.permissions = android.permission.INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 25

# (str) Android build-tools version to use
android.build_tools = 31.0.0

# (bool) If True, then automatically accept SDK license
# agreements.
# MODIFICADO: Activado para automatizar el proceso y evitar que se detenga.
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

#
# Python for android (p4a) specific
#

# AÑADIDO: Corrección para problemas de red con Java en entornos como WSL.
p4a.java_args = -Djava.net.preferIPv4Stack=true


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1