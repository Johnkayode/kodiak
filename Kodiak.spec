# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('kodiak.icns', '.')],
    hiddenimports=['pyexcel_io.writers', 'pyexcel_io.readers', 'pyexcel_io.database.importers.django', 'pyexcel_io.database.importers.sqlalchemy', 'pyexcel_io.database.exporters.django', 'pyexcel_io.database.exporters.sqlalchemy', 'pyexcel_xlsx', 'pyexcel_xlsx.xlsxr', 'pyexcel_xlsx.xlsxw', 'pyexcel_xls', 'pyexcel_xls.xlsr', 'pyexcel_xls.xlsw'],
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
    name='Kodiak',
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
    icon=['kodiak.icns'],
)
app = BUNDLE(
    exe,
    name='Kodiak.app',
    icon='kodiak.icns',
    bundle_identifier=None,
)
