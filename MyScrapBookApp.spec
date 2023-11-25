from kivy_deps import sdl2, glew
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MyScrapBookApp.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
a.datas += [('code\myscrapbookapp.kv', 'C:\\Users\\joshm\\PycharmProjects\\Reminiscence_Project\myscrapbookapp.kv', 'DATA')]
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyScrapBookApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe, Tree('C:\\Users\\joshm\\PycharmProjects\\Reminiscence_Project\\'),
    a.binaries,
    a.datas, *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyScrapBookApp',
)
