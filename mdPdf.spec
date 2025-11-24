# -*- mode: python ; coding: utf-8 -*-
"""
Archivo de configuración de PyInstaller para mdPdf
"""

import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'weasyprint',
        'markdown2',
        'pygments',
        'PyQt6',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mdPdf',  # Nombre del ejecutable (se mantiene mdPdf.exe por compatibilidad)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No mostrar consola en Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Para macOS, crear un bundle .app
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Padlef.app',
        icon='assets/icon.icns',
        bundle_identifier='com.padlef.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )

