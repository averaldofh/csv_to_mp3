# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['E:/Documentos/Eletronica/Python/csv_to_mp3/csv_to_mp3_gui.py'],
             pathex=['E:\\Documentos\\Eletronica\\Python\\csv_to_mp3'],
             binaries=[],
             datas=[('E:/Documentos/Eletronica/Python/csv_to_mp3/ico.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='csv_to_mp3_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='E:\\Documentos\\Eletronica\\Python\\csv_to_mp3\\ico.ico')
