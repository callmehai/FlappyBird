# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['flappybird.py'],
    pathex=[],
    binaries=[],
    datas=[('background-night.png', '.'), ('floor.png', '.'), ('yellowbird-downflap.png', '.'), ('yellowbird-midflap.png', '.'), ('yellowbird-upflap.png', '.'), ('pipe-green.png', '.'), ('message.png', '.'), ('meteo34x34.png', '.'), ('laser.png', '.'), ('04B_19.TTF', '.'), ('sfx_wing.wav', '.'), ('sfx_hit.wav', '.'), ('sfx_point.wav', '.'), ('sfx_die.wav', '.'), ('sfx_swooshing.wav', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='flappybird',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='flappybird.app',
    icon=None,
    bundle_identifier=None,
)
