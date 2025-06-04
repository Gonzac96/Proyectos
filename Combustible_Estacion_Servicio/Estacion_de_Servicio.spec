# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules

# Si tu script principal se llama “Estacion_de_Servicio.py”, dejá ese nombre aquí:
script_name = 'Estacion_de_Servicio.py'

a = Analysis(
    [script_name],
    pathex=[],
    binaries=[],
    # 1. Incluimos toda la carpeta iconos/
    # 2. Agregamos también el archivo impuestos.db en la raíz
    datas=[
        ('iconos/*', 'iconos'),
        ('impuestos.db', '.')  
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Estacion de Servicio',            # Nombre del ejecutable (sin .exe)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                           # False = ventana sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='iconos/Fuel_station.ico',         # Ruta al icono principal
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Estacion de Servicio',
)
