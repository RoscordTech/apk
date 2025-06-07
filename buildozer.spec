[app]

# (requerido) Título de tu aplicación
title = Trayectos

# (requerido) Nombre del paquete, sin espacios ni caracteres especiales
package.name = trayectos

# (requerido) Dominio del paquete, en orden inverso
# Cámbialo por tu propio dominio, por ejemplo, com.miempresa
package.domain = org.test

# (requerido) Directorio donde está tu main.py
source.dir = .

# (requerido) Lista de extensiones de archivo a incluir
source.include_exts = py,png,jpg,kv,atlas,json

# (opcional) Versión de tu aplicación
version = 1.0

# (requerido) Lista de dependencias de tu aplicación
# Buildozer se encarga de instalar Kivy. KivyMD es la principal que debemos añadir.
requirements = python3,kivymd

# (opcional) Orientación de la pantalla ('portrait', 'landscape', 'all')
orientation = portrait

# (opcional) Icono de la aplicación. Debes crear un archivo 'icon.png' de 1024x1024
icon.filename = %(source.dir)s/icon.png

# (opcional) Imagen de bienvenida (splash screen)
presplash.filename = %(source.dir)s/presplash.png

# (requerido) Lista de permisos que necesitará tu app en Android
# INTERNET es necesario para que webbrowser.open() funcione y abra los enlaces.
android.permissions = INTERNET

# (opcional) Arquitecturas a compilar. arm64-v8a es estándar para móviles modernos.
android.archs = arm64-v8a

# (opcional) Nivel de API mínimo y objetivo.
# api 31 es un buen objetivo para Google Play en 2024/2025.
android.api = 31
android.minapi = 21

# (opcional) Versiones del SDK y NDK de Android. Déjalas como están si no estás seguro.
# android.sdk = 28
# android.ndk = 25b

# (opcional) Permite que la app se pueda mover a la tarjeta SD
android.install_location = auto

# (opcional) Evita que la pantalla se apague mientras la app está activa
android.wakelock = False

[buildozer]

# Nivel de verbosidad de los logs (0, 1, o 2)
log_level = 2

# Muestra una advertencia si se usa el archivo spec por defecto (0 o 1)
warn_on_root = 1
